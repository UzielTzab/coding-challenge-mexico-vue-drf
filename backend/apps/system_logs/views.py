from rest_framework import viewsets, mixins
from .models import SystemLog, BotRuntimeState
from rest_framework import serializers

class SystemLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemLog
        fields = '__all__'

class BotRuntimeStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotRuntimeState
        fields = '__all__'

class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SystemLog.objects.all().order_by('-created_at')
    serializer_class = SystemLogSerializer

class BotRuntimeStateViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin):
    queryset = BotRuntimeState.objects.all()
    serializer_class = BotRuntimeStateSerializer
