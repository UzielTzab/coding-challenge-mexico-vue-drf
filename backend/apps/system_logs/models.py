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

from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=SystemLog)
def emit_system_log(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                "dashboard_updates",
                {
                    "type": "dashboard_message",
                    "payload": {
                        "type": "system_log_created",
                        "level": instance.level,
                        "source": instance.source,
                        "message": instance.message,
                        "created_at": instance.created_at.isoformat()
                    }
                }
            )
