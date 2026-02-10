"""
Serializers for alert APIs.
"""
from rest_framework import serializers

from django.contrib.auth import get_user_model

from alerts.model import Alert, Acknowledgement

class AlertSerializer(serializers.ModelSerializer):
    """Serializer for alerts."""

    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Alert
        fields = [
            'id',
            'title',
            'description',
            'severity',
            'status',
            'created_by',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_by', 'created_at']

class AcknowledgementSerializer(serializers.ModelSerializer):
    """Serializer for acknowledging alerts."""

    class Meta:
        model = Acknowledgement
        fields = [
            'id',
            'alert',
            'acknowledged_at'
        ]
        read_only_fields = ['id', 'acknowledged_at']