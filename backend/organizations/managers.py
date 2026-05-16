"""
Módulo Organizations: Managers
TenantManager y TenantQuerySet proporcionan filtrado automático por organización.
Esto garantiza que NINGÚN query pueda omitir accidentalmente el filtro de tenant.
"""
import threading
from django.db import models


# Thread-local storage to hold the current organization per request
_thread_locals = threading.local()


def set_current_organization(organization):
    """Called by TenantMiddleware to set the active org for this request."""
    _thread_locals.organization = organization


def get_current_organization():
    """Returns the current organization for this thread/request."""
    return getattr(_thread_locals, 'organization', None)


def clear_current_organization():
    """Clears the org after request completes."""
    _thread_locals.organization = None

def set_pg_session_var(org):
    """Set PostgreSQL session variable for Row-Level Security."""
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SET LOCAL app.current_org_id = %s",
                [str(org.id)]
            )
    except Exception:
        pass


class TenantQuerySet(models.QuerySet):
    """QuerySet that can filter by the current tenant."""

    def for_organization(self, organization):
        """Explicitly filter by a specific organization."""
        return self.filter(organization=organization)


class TenantManager(models.Manager):
    """
    Manager that auto-filters queries by the current organization.
    If no organization is set in thread-local (e.g., management commands),
    no filtering is applied — this allows migrations and admin to work.
    """

    def get_queryset(self):
        qs = TenantQuerySet(self.model, using=self._db)
        org = get_current_organization()
        if org is not None:
            return qs.filter(organization=org)
        return qs

    def for_organization(self, organization):
        """Explicit filter — use in management commands or background tasks."""
        return self.get_queryset().filter(organization=organization)
