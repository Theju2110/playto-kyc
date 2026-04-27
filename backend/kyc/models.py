from django.db import models

# Create your models here.

from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('merchant', 'Merchant'),
        ('reviewer', 'Reviewer'),
    )
    username = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class KYCSubmission(models.Model):
    STATE_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('more_info_requested', 'More Info Requested'),
    )

    merchant = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=30, choices=STATE_CHOICES, default='draft')

    personal_details = models.TextField(null=True, blank=True)
    business_details = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Document(models.Model):
    submission = models.ForeignKey(KYCSubmission, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    doc_type = models.CharField(max_length=20)

class Notification(models.Model):
    merchant = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    payload = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)