from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, QuizQuestion, QuizResult, UserSkill
from .forms import StudentProfileForm, JobAnalyzerForm, RegisterForm
from .utils import extract_skills_from_jd, calculate_skill_match
from jobs.models import TargetRole, JobDescription

# --- Member 1: Authentication & Onboarding Views ---

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('onboarding')
    else:
        form = RegisterForm()
    return render(request, 'analyzer/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'analyzer/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'analyzer/login.html')

@login_required
def onboarding_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.target_role = request.POST.get('target_role', 'Full Stack Developer')
        profile.experience_level = request.POST.get('experience_level', 'Student / Fresher')
        profile.primary_skills = request.POST.get('primary_skills', '')
        profile.skills = request.POST.get('primary_skills', '')
        profile.save()
        return redirect('dashboard')
        
    return render(request, 'analyzer/onboarding.html')


# --- Combined Dashboard (Form Analysis + Member 2 DB Roles) ---

@login_required
def dashboard_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    user_skills = UserSkill.objects.filter(user=user)
    
    match_percentage = None
    matched_skills = []
    missing_skills = []
    extracted_skills = []

    target_roles = TargetRole.objects.all()
    selected_role_id = None
    combined_jd_text = ""

    if request.method == 'POST':
        selected_role_id = request.POST.get('role_id')
        
        if selected_role_id:
            try:
                role_obj = TargetRole.objects.get(id=selected_role_id)
                jds = JobDescription.objects.filter(role=role_obj)
                combined_jd_text = "\n".join([jd.raw_text for jd in jds if jd.raw_text])
                extracted_skills = extract_skills_from_jd(combined_jd_text)
                match_percentage, matched_skills, missing_skills = calculate_skill_match(profile.primary_skills, extracted_skills)
            except TargetRole.DoesNotExist:
                pass

    context = {
        'profile': profile,
        'user_skills': user_skills,
        'target_roles': target_roles,
        'selected_role_id': int(selected_role_id) if selected_role_id else None,
        'combined_jd_text': combined_jd_text,
        'match_percentage': match_percentage,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'extracted_skills': extracted_skills,
    }
    return render(request, 'analyzer/dashboard.html', context)


# --- Additional Feature Views ---

@login_required
def update_skills(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'analyzer/update_skills.html', {'form': form})


@login_required
def report_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    user_skills = UserSkill.objects.filter(user=user)
    
    # Fetch real quiz results specifically for the logged-in user
    quiz_results = []
    if hasattr(QuizResult, 'completed_at'):
        quiz_results = list(QuizResult.objects.filter(user=user).order_by('completed_at'))
    else:
        quiz_results = list(QuizResult.objects.filter(user=user))

    # Convert raw correct counts into percentage scores
    scores = []
    for q in quiz_results:
        if hasattr(q, 'score') and hasattr(q, 'total_questions') and q.total_questions and q.total_questions > 0:
            percentage = (q.score / q.total_questions) * 100
            scores.append(int(percentage))
        elif hasattr(q, 'score'):
            s = q.score
            if s <= 1.0:
                scores.append(int(s * 100))
            else:
                scores.append(int(s))

    avg_quiz_score = int(sum(scores) / len(scores)) if scores else 0

    # --- 1. Fetch Target Role & Extract ALL Required Skills from DB ---
    target_role_title = profile.target_role or ""
    extracted_skills = []

    if target_role_title:
        # Match user's registered target role against database TargetRole entries
        target_role_obj = TargetRole.objects.filter(title__icontains=target_role_title).first()
        
        if not target_role_obj:
            # Fallback: exact or case-insensitive match
            target_role_obj = TargetRole.objects.filter(title__iexact=target_role_title).first()

        if target_role_obj:
            # Fetch ALL job descriptions attached to this role in the database
            jds = JobDescription.objects.filter(role=target_role_obj)
            combined_jd_text = "\n".join([jd.raw_text for jd in jds if jd.raw_text])
            
            # Extract skills from combined database job descriptions
            extracted_skills = extract_skills_from_jd(combined_jd_text)

    # Calculate skill match percentage, matched skills, and missing skills
    if extracted_skills:
        match_percentage, matched_skills, missing_skills = calculate_skill_match(
            profile.primary_skills, extracted_skills
        )
    else:
        # If no database entries exist yet for this role
        match_percentage = 0
        matched_skills = []
        missing_skills = []

    # --- 2. Predictive Career Readiness Score ---
    readiness_score = int((match_percentage * 0.6) + (avg_quiz_score * 0.4)) if scores else match_percentage

    # --- 3. Personalized Learning Roadmap Suggestions ---
    suggestions = []
    
    if missing_skills:
        for skill in missing_skills:
            suggestions.append(f"Master **{skill}**: Build a project or complete targeted learning focused specifically on {skill}.")
        suggestions.append(f"Bridge your skill gaps for **{target_role_title}** by participating in open-source projects using your missing stack.")
    else:
        if extracted_skills:
            suggestions.append(f"🌟 Outstanding profile alignment! You match all extracted skills for **{target_role_title}**.")
            suggestions.append("🚀 Level up further by exploring system architecture, design patterns, and team leadership methodologies.")
        else:
            suggestions.append(f"No job description data found in database for target role **{target_role_title}**. Upload job descriptions to view detailed analytics.")
    
    suggestions.append("📈 Optimize your GitHub portfolio and resume with quantifiable achievements from your recent project builds.")
    suggestions.append("💡 Practice mock technical interviews regularly to sharpen live coding communication and problem-solving.")

    context = {
        'profile': profile,
        'user_skills': user_skills,
        'match_percentage': match_percentage,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'avg_quiz_score': avg_quiz_score,
        'readiness_score': readiness_score,
        'quiz_results': quiz_results[-5:],
        'suggestions': suggestions,
        'quiz_scores_json': scores,
    }
    return render(request, 'analyzer/report.html', context)


@login_required
def take_quiz(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    questions = QuizQuestion.objects.filter(target_role__iexact=profile.target_role)[:4]
    if not questions.exists():
        questions = QuizQuestion.objects.all()[:4]

    if request.method == 'POST':
        score = 0
        total = len(questions)
        for q in questions:
            user_answer = request.POST.get(f'question_{q.id}')
            if user_answer and user_answer.upper() == q.correct_option.upper():
                score += 1

        QuizResult.objects.create(user=request.user, score=score, total_questions=total)
        return render(request, 'analyzer/quiz_result.html', {'score': score, 'total': total})

    return render(request, 'analyzer/take_quiz.html', {'questions': questions, 'target_role': profile.target_role})