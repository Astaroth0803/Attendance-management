"""
Módulo Organizations: Modelos
Define Organization (tenant) y TenantModel (base abstracta para aislamiento multi-tenant).
"""
from django.db import models


class Organization(models.Model):
    """Represents a tenant (e.g., a community center, library, etc.)"""
    name = models.CharField("Nombre", max_length=200)
    slug = models.SlugField("Slug", unique=True, max_length=100,
                            help_text="Identificador URL-safe único (ej: las-mananitas)")
    client_first_name = models.CharField("Nombre Cliente", max_length=100, blank=True, null=True)
    client_last_name = models.CharField("Apellido Cliente", max_length=100, blank=True, null=True)
    client_email = models.EmailField("Email Cliente", max_length=200, blank=True, null=True)
    client_phone = models.CharField("Teléfono Cliente", max_length=50, blank=True, null=True)
    country = models.CharField("País", max_length=100, default='Panamá')
    logo = models.TextField("Logo (base64)", blank=True, null=True)
    is_active = models.BooleanField("Activo", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Organización"
        verbose_name_plural = "Organizaciones"

    def __str__(self):
        return self.name


class TenantModel(models.Model):
    """
    Abstract base model for all tenant-scoped data.
    Every model that contains tenant-specific data MUST inherit from this.
    """
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="%(class)s_set",
        verbose_name="Organización",
        db_index=True,
    )

    class Meta:
        abstract = True
