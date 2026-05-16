from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import SuperAdminOrganizationViewSet, toggle_organization_status, generate_support_user, get_org_admins

router = DefaultRouter()
router.register(r'organizations', SuperAdminOrganizationViewSet, basename='superadmin-organization')

urlpatterns = [
    path('', include(router.urls)),
    path('organizations/<int:pk>/toggle_status/', toggle_organization_status, name='org-toggle-status'),
    path('organizations/<int:pk>/generate_support_user/', generate_support_user, name='org-generate-support'),
    path('organizations/<int:pk>/admin_users/', get_org_admins, name='org-admin-users'),
]
