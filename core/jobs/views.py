from django.shortcuts import render, redirect
from .forms import TargetRoleForm, JobDescriptionForm
from .models import JobDescription, TargetRole
import PyPDF2

def upload_job(request):
    if request.method == 'POST':
        form = JobDescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            job_desc = form.save(commit=False)

            # Extract text automatically if a file is uploaded
            if 'file' in request.FILES:
                uploaded_file = request.FILES['file']
                
                # Handling TXT file
                if uploaded_file.name.endswith('.txt'):
                    job_desc.raw_text = uploaded_file.read().decode('utf-8')
                
                # Handling PDF file
                elif uploaded_file.name.endswith('.pdf'):
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    extracted_text = ""
                    for page in pdf_reader.pages:
                        extracted_text += page.extract_text() or ""
                    job_desc.raw_text = extracted_text

            job_desc.save()
            return redirect('job_list')
    else:
        form = JobDescriptionForm()

    return render(request, 'jobs/upload.html', {'form': form})


def job_list(request):
    jobs = JobDescription.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})