"""
Módulo Organizations: Security Mixins
Mixins de DRF para ViewSets y Serializers que garantizan aislamiento multi-tenant.
"""
from rest_framework.exceptions import PermissionDenied, ValidationError


class TenantViewMixin:
    """
    Mixin for DRF ViewSets that:
    1. Auto-filters querysets by request.organization
    2. Auto-injects organization on create
    3. Blocks access if no organization context exists
    
    Usage:
        class MyViewSet(TenantViewMixin, viewsets.ModelViewSet):
            ...
    """

    def get_queryset(self):
        qs = super().get_queryset()
        org = getattr(self.request, 'organization', None)
        if not org and self.request.user and self.request.user.is_authenticated:
            org = getattr(self.request.user, 'organization', None)
            
        if org is None:
            # No org context — return empty queryset (defense in depth)
            return qs.none()
            
        # Ensure thread local and DB session are set for this DRF request
        from .managers import set_current_organization, set_pg_session_var
        set_current_organization(org)
        set_pg_session_var(org)
        
        return qs.filter(organization=org)

    def perform_create(self, serializer):
        org = getattr(self.request, 'organization', None)
        if not org and self.request.user and self.request.user.is_authenticated:
            org = getattr(self.request.user, 'organization', None)
            
        if org is None:
            raise PermissionDenied("No se pudo determinar la organización.")
        serializer.save(organization=org)

    def perform_update(self, serializer):
        # Verify the object belongs to the current org (defense in depth)
        obj = self.get_object()
        org = getattr(self.request, 'organization', None)
        if org and hasattr(obj, 'organization_id') and obj.organization_id != org.id:
            raise PermissionDenied("No tiene permiso para modificar este recurso.")
        serializer.save()


class TenantSerializerMixin:
    """
    Mixin for DRF Serializers that validates cross-tenant references.
    Ensures that FK fields (beneficiary, event, activity, etc.) belong
    to the same organization as the request.
    
    Set `tenant_fk_fields` on the serializer to list FK field names to validate.
    
    Usage:
        class MySerializer(TenantSerializerMixin, serializers.ModelSerializer):
            tenant_fk_fields = ['beneficiary', 'event']
    """
    tenant_fk_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'organization' in self.fields:
            self.fields['organization'].read_only = True

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        if not request:
            return attrs

        org = getattr(request, 'organization', None)
        if not org and hasattr(request, 'user') and request.user.is_authenticated:
            org = getattr(request.user, 'organization', None)
            
        if not org:
            return attrs

        for field_name in self.tenant_fk_fields:
            related_obj = attrs.get(field_name)
            if related_obj and hasattr(related_obj, 'organization_id'):
                if related_obj.organization_id != org.id:
                    raise ValidationError({
                        field_name: f"El recurso referenciado no pertenece a su organización."
                    })

        return attrs


def get_tenant_or_deny(request):
    """
    Helper for @api_view functions.
    Returns the organization from request or raises PermissionDenied.
    """
    org = getattr(request, 'organization', None)
    if not org and hasattr(request, 'user') and request.user.is_authenticated:
        org = getattr(request.user, 'organization', None)
        
    if org is None:
        raise PermissionDenied("No se pudo determinar la organización.")
        
    # Ensure thread local and DB session are set for this DRF request
    from .managers import set_current_organization, set_pg_session_var
    set_current_organization(org)
    set_pg_session_var(org)
    
    return org
