from rest_framework import viewsets
from .models import PerformanceSnapshot
from rest_framework import serializers

class PerformanceSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceSnapshot
        fields = '__all__'

class PerformanceSnapshotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PerformanceSnapshot.objects.all().order_by('-created_at')
    serializer_class = PerformanceSnapshotSerializer
