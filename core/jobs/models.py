from django.db import models

class TargetRole(models.Model):
    title = models.CharField(max_length=255) # e.g., "Data Analyst", "Software Engineer"
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobDescription(models.Model):
    role = models.ForeignKey(TargetRole, on_delete=models.CASCADE, related_name='job_descriptions')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    raw_text = models.TextField(help_text="Extracted text from PDF/TXT or manual entry")
    file = models.FileField(upload_to='job_descriptions/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role.title} - {self.company_name or 'General'}"