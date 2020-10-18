from django.db import models

class ResumeTemplates(models.Model):
    img = models.ImageField(upload_to = "resume_templates")
    jsFile = models.CharField(max_length = 100,null=True)