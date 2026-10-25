from django import forms
from .models import TargetRole, JobDescription

class TargetRoleForm(forms.ModelForm):
    class Meta:
        model = TargetRole
        fields = ['title', 'description']


class JobDescriptionForm(forms.ModelForm):
    class Meta:
        model = JobDescription
        fields = ['role', 'company_name', 'file', 'raw_text']
        widgets = {
            'raw_text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Paste job description here if not uploading a file...'}),
        }