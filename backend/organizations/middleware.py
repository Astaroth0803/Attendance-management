"""
Módulo Organizations: Middleware
TenantMiddleware inyecta request.organization basado en el usuario autenticado.
Para endpoints públicos, resuelve la org desde ?org=slug.
También configura la variable de sesión de PostgreSQL para RLS.
"""
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .managers import set_current_organization, clear_current_organization


class TenantMiddleware(MiddlewareMixin):
    """
    Sets the current organization for every request based on:
    1. Authenticated user → user.organization
    2. Public endpoints → ?org=<slug> query parameter
    
    Also sets PostgreSQL session variable for Row-Level Security.
    """

    # Paths that don't require tenant context
    EXEMPT_PATHS = (
        '/admin/',
        '/api/token/',
        '/api/token/refresh/',
    )

    def process_request(self, request):
        # Always clear previous request's org
        clear_current_organization()
        request.organization = None

        # Skip exempt paths
        if any(request.path.startswith(p) for p in self.EXEMPT_PATHS):
            return None

        # 1. Try authenticated user
        if hasattr(request, 'user') and request.user.is_authenticated:
            org = getattr(request.user, 'organization', None)
            if org:
                request.organization = org
                set_current_organization(org)
                from .managers import set_pg_session_var
                set_pg_session_var(org)
                return None

        # 2. Try public endpoint with ?org=slug
        if '/public/' in request.path:
            org_slug = request.GET.get('org')
            if not org_slug:
                return JsonResponse(
                    {'detail': 'Se requiere el parámetro ?org=slug.'},
                    status=400
                )
            from .models import Organization
            try:
                org = Organization.objects.get(slug=org_slug, is_active=True)
                request.organization = org
                set_current_organization(org)
                from .managers import set_pg_session_var
                set_pg_session_var(org)
            except Organization.DoesNotExist:
                return JsonResponse(
                    {'detail': 'Organización no encontrada o inactiva.'},
                    status=404
                )
            return None

        return None

    def process_response(self, request, response):
        clear_current_organization()
        return response
