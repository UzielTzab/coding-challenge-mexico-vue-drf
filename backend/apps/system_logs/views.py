from rest_framework import generics
from .models import SystemLog
from .serializers import SystemLogSerializer

class SystemLogListView(generics.ListAPIView):
    queryset = SystemLog.objects.all().order_by('-created_at')
    serializer_class = SystemLogSerializer
