"""
Database models for alerts.
"""
from django.conf import settings
from django.db import models

class Alert(models.Model):
    """Alert issued in the system."""

    class Severity(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        RESOLVED = "RESOLVED", "Resolved"

    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(
        max_length=10,
        choices=Severity.choices,
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="alerts_created",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Acknowledgement(models.Model):
    """User acknowledgement of an alert."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="acknowledgements",
    )
    alert = models.ForeignKey(
        Alert,
        on_delete=models.CASCADE,
        related_name="acknowledgements",
    )

    acknowledged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'alert')

    def __str__(self):
        return f"{self.user.email} - {self.alert.title}"