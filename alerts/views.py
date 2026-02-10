"""
Views for alert APIs.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from alerts.models import Alert, Acknowledgement
from alerts.serializers import AlertSerializer, AcknowledgementSerializer
from alerts.permissions import IsAdminOrReadOnly

class AlertViewSet(viewsets.ModelViewSet):
    """View for managing alerts."""

    serializer_class = AlertSerializer
    queryset = Alert.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

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
        return Response(serializer.data, status=status.HTTP_201_CREATED)