"""
Módulo Accounts: Modelos
Define la estructura de datos para los perfiles y usuarios del sistema.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from organizations.models import Organization

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        PROFESSOR = 'PROFESSOR', 'Profesor'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PROFESSOR
    )
    
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        related_name="users"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
