from django.db import models

class SystemLog(models.Model):
    LEVEL_CHOICES = [
        ('info', 'INFO'),
        ('success', 'SUCCESS'),
        ('warn', 'WARN'),
        ('error', 'ERROR'),
    ]
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    source = models.CharField(max_length=80)
    message = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class BotRuntimeState(models.Model):
    is_running = models.BooleanField(default=False)
    mode = models.CharField(max_length=30, default='simulation')
    started_at = models.DateTimeField(blank=True, null=True)
    stopped_at = models.DateTimeField(blank=True, null=True)
    last_heartbeat_at = models.DateTimeField(blank=True, null=True)
    circuit_breaker_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
