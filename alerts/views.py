"""
Views for alert APIs.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from alerts.models import Alert, Acknowledgement
from alerts.serializers import AlertSerializer, AcknowledgementSerializer
from alerts.permissions import IsAdminOrReadOnly

class AlertViewSet(viewsets.ModelViewSet):
    """View for managing alerts."""

    serializer_class = AlertSerializer
    queryset = Alert.objects.all()
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [p() for p in permission_classes]

    def perform_create(self, serializer):
        """Set the creator of the alert."""
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def ack(self, request, pk=None):
        """Acknowledge an alert."""
        alert = self.get_object()

        ack, created = Acknowledgement.objects.get_or_create(
            user = request.user,
            alert = alert
        )

        if not created:
            return Response(
                {"detail": "Already acknowledged."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        serializer = AcknowledgementSerializer(ack)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        """Returm alerts for the current user."""
        user = self.request.user

        if user.role == 'ADMIN':
            return Alert.objects.all().order_by('-created_at')
        
        return Alert.objects.filter(status='ACTIVE').order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Return only active alerts."""
        alerts = self.queryset.filter(status='ACTIVE')
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        """Only admin can resolve alerts."""
        user = self.request.user

        if 'status' in serializer.validated_data:
            if serializer.validated_data['status'] == 'RESOLVED' and user.role != 'ADMIN':
                raise PermissionDenied("Only admins can resolve alerts.")

        serializer.save()