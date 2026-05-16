from datetime import date
from rest_framework import serializers
from django.contrib.auth import get_user_model
from organizations.security import TenantSerializerMixin
from .models import Beneficiary, Activity, Event

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    organization_name = serializers.SerializerMethodField()
    organization_slug = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_staff', 'is_active', 'organization', 'organization_name', 'organization_slug']

    def get_organization_name(self, obj):
        return obj.organization.name if obj.organization else None

    def get_organization_slug(self, obj):
        return obj.organization.slug if obj.organization else None

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class BeneficiarySerializer(TenantSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = '__all__'

    def validate_ci(self, value):
        if not value or value.strip() == "":
            return None
        return value.strip()

    def validate_dob(self, value):
        if value and value > date.today():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")
        return value

class EventSerializer(TenantSerializerMixin, serializers.ModelSerializer):
    tenant_fk_fields = ['activity']
    class Meta:
        model = Event
        fields = '__all__'

class ActivitySerializer(TenantSerializerMixin, serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'name', 'category', 'deadline_date', 'description', 'is_active', 'image', 'events']
