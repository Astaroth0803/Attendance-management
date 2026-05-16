import string
import secrets
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Organization
from .serializers import OrganizationSerializer

User = get_user_model()

class SuperAdminOrganizationViewSet(viewsets.ModelViewSet):
    """
    CRUD for Organizations. Only accessible by superusers.
    Does NOT use TenantViewMixin because it needs to manage ALL organizations.
    """
    queryset = Organization.objects.all().order_by('-created_at')
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminUser]  # Only is_staff / is_superuser

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        org = serializer.instance
        headers = self.get_success_headers(serializer.data)
        
        # Auto-generate primary admin user for this license
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for _ in range(10))
        username = org.slug.replace('-', '')
        
        try:
            admin_user = User.objects.create_user(
                username=username,
                email=org.client_email or f"admin@{org.slug}.com",
                password=password,
                first_name=org.client_first_name or "Admin",
                last_name=org.client_last_name or "Principal",
                role=User.Role.ADMIN,
                organization=org
            )
        except Exception:
            username = f"{username}{org.id}"
            admin_user = User.objects.create_user(
                username=username,
                email=org.client_email or f"admin@{org.slug}.com",
                password=password,
                first_name=org.client_first_name or "Admin",
                last_name=org.client_last_name or "Principal",
                role=User.Role.ADMIN,
                organization=org
            )
            
        data = serializer.data
        data['admin_credentials'] = {
            'username': admin_user.username,
            'password': password
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_org_admins(request, pk):
    org = get_object_or_404(Organization, pk=pk)
    
    # Exclude system support users
    support_username = request.user.email or f"soporte_{request.user.username}"
    admins = User.objects.filter(
        organization=org, 
        role=User.Role.ADMIN
    ).exclude(username=support_username).exclude(username__startswith='soporte_')
    
    data = []
    for u in admins:
        data.append({
            'username': u.username,
            'email': u.email,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'is_active': u.is_active,
            'last_login': u.last_login.strftime('%Y-%m-%d %H:%M') if u.last_login else 'Nunca'
        })
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def toggle_organization_status(request, pk):
    org = get_object_or_404(Organization, pk=pk)
    org.is_active = not org.is_active
    org.save()
    return Response({'status': 'success', 'is_active': org.is_active, 'message': f'Organización {"Activada" if org.is_active else "Desactivada"}'})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def generate_support_user(request, pk):
    org = get_object_or_404(Organization, pk=pk)
    
    # Use the superadmin's email as the support account username
    support_username = request.user.email
    if not support_username:
        support_username = f"soporte_{request.user.username}"
        
    # Generate secure password (e.g. 10 chars)
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(10))
    
    # Auto-delete any previous support user with this username across ALL organizations
    # CRITICAL: Exclude the superadmin themselves so they don't accidentally delete their own master account
    User.objects.filter(username=support_username).exclude(id=request.user.id).delete()
    
    # Create new support user in target organization
    user = User.objects.create_user(
        username=support_username,
        email=support_username,
        password=password,
        first_name=request.user.first_name or "Soporte",
        last_name=request.user.last_name or "Técnico",
        role=User.Role.ADMIN,
        organization=org
    )
    action = "created"
        
    return Response({
        'status': 'success',
        'action': action,
        'credentials': {
            'username': support_username,
            'password': password
        }
    })
