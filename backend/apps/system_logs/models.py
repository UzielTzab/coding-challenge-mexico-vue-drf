from django.db import models

class SystemLog(models.Model):
    LEVEL_CHOICES = [
        ("info", "INFO"),
        ("success", "SUCCESS"),
        ("warn", "WARN"),
        ("error", "ERROR"),
    ]

    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    source = models.CharField(max_length=80)
    message = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.level.upper()}] {self.source}: {self.message}"
