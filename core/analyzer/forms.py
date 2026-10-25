from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-slate-900/80 border border-purple-500/30 rounded-xl p-3 text-white focus:outline-none focus:border-purple-400 transition',
            'placeholder': 'Password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-slate-900/80 border border-purple-500/30 rounded-xl p-3 text-white focus:outline-none focus:border-purple-400 transition',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900/80 border border-purple-500/30 rounded-xl p-3 text-white focus:outline-none focus:border-purple-400 transition',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-slate-900/80 border border-purple-500/30 rounded-xl p-3 text-white focus:outline-none focus:border-purple-400 transition',
                'placeholder': 'Email address'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


class StudentProfileForm(forms.ModelForm):
    EXPERIENCE_CHOICES = [
        ('Beginner (0-1 Years)', 'Beginner (0-1 Years)'),
        ('Junior (1-2 Years)', 'Junior (1-2 Years)'),
        ('Mid-Level (2-5 Years)', 'Mid-Level (2-5 Years)'),
        ('Senior (5+ Years)', 'Senior (5+ Years)'),
    ]

    experience_level = forms.ChoiceField(
        choices=EXPERIENCE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full bg-slate-900/80 border border-purple-500/30 rounded-xl p-3 text-white focus:outline-none focus:border-purple-400 transition'
        })
    )

    class Meta:
        model = UserProfile
        # Removed redundant 'skills' field to prevent dual input boxes
        fields = ['target_role', 'experience_level', 'primary_skills']
        widgets = {
            'target_role': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900/80 border border-purple-500/30 rounded-xl p-3 text-white focus:outline-none focus:border-purple-400 transition',
                'placeholder': 'e.g., Data Analyst, Full Stack Developer'
            }),
            'primary_skills': forms.Textarea(attrs={
                'class': 'w-full bg-slate-900/80 border border-purple-500/30 rounded-xl p-3 text-white focus:outline-none focus:border-purple-400 transition',
                'rows': 3,
                'placeholder': 'Enter your skills separated by commas (e.g., Python, Django, MySQL)'
            }),
        }


class JobAnalyzerForm(forms.Form):
    job_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full bg-slate-900/80 border border-purple-500/30 rounded-xl p-3 text-white focus:outline-none focus:border-purple-400 transition',
            'rows': 6,
            'placeholder': 'Paste the job description text here...'
        }),
        label="Job Description Text",
        required=True
    )