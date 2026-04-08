"""
Módulo Core: Modelos
Provee las entidades base o maestras del sistema, como Beneficiary (Beneficiarios),
Activity (Actividades globales) y Event (Eventos específicos de una actividad).
"""
from django.db import models

class Beneficiary(models.Model):
    class Sex(models.TextChoices):
        MALE = 'M', 'Masculino'
        FEMALE = 'F', 'Femenino'
        OTHER = 'O', 'Otro'

    ci = models.CharField("Cédula o ID Local", max_length=50, unique=True, blank=True, null=True, help_text="Cédula de identidad o número de gafete QR")
    first_name = models.CharField("Nombre", max_length=100)
    last_name = models.CharField("Apellido", max_length=100)
    dob = models.DateField("Fecha de Nacimiento", help_text="Para calcular la edad automáticamente")
    sex = models.CharField("Sexo", max_length=1, choices=Sex.choices)
    sector = models.CharField("Sector", max_length=150)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.ci})"

class Activity(models.Model):
    class Category(models.TextChoices):
        PERMANENT = 'PERMANENT', 'Permanente'
        EVENTUAL = 'EVENTUAL', 'Eventual'

    name = models.CharField("Nombre de la Actividad", max_length=100)
    category = models.CharField("Categoría", max_length=20, choices=Category.choices, default=Category.PERMANENT)
    deadline_date = models.DateField("Fecha Límite", blank=True, null=True)
    description = models.TextField("Descripción", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    image = models.TextField("Imagen (base64)", blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="events")
    name = models.CharField("Nombre del Evento", max_length=150, help_text="Ej: -default- o 'Torneo de Fútbol'")
    date = models.DateField("Fecha del Evento", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.activity.name} - {self.name}"
