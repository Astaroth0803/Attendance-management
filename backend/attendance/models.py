"""
Módulo Attendance: Modelos
Contiene los modelos relacionados con el registro de asistencia a eventos
y el control de inscripciones a excursiones de los beneficiarios.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from core.models import Beneficiary, Event

class AttendanceRecord(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name="attendances")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField("Fecha de Asistencia")
    time = models.TimeField("Hora de Registro", null=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="registered_attendances")

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo al crear, no al editar
            now_local = timezone.localtime(timezone.now())
            self.date = now_local.date()
            self.time = now_local.time()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('beneficiary', 'event', 'date')
        indexes = [
            models.Index(fields=['date'], name='idx_asistencia_fecha'),
            models.Index(fields=['event', 'date'], name='idx_evento_fecha'),
        ]

    def __str__(self):
        return f"{self.beneficiary} -> {self.event} ({self.date})"

class Excursion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE_REGISTRO = 'pendiente_registro', 'Pendiente de Registro'
        REGISTRO_CERRADO = 'registro_cerrado', 'Registro Cerrado'
        DIA_EVENTO = 'dia_evento', 'Día del Evento'
        FINALIZADO = 'finalizado', 'Finalizado'
        CANCELADO = 'cancelado', 'Cancelado'

    nombre = models.CharField("Nombre de la Excursión", max_length=150)
    descripcion = models.TextField("Descripción", blank=True, null=True)
    fecha_evento = models.DateField("Fecha del Evento")
    edad_min = models.IntegerField("Edad Mínima", default=0)
    edad_max = models.IntegerField("Edad Máxima", default=99)
    min_asistencias = models.IntegerField("Asistencias Mínimas Requeridas", default=0, help_text="Cantidad mínima de asistencias regulares requeridas para participar")
    estado = models.CharField(
        "Estado", 
        max_length=20, 
        choices=Estado.choices, 
        default=Estado.PENDIENTE_REGISTRO
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['fecha_evento'], name='idx_excursion_fecha'),
            models.Index(fields=['estado', 'fecha_evento'], name='idx_excursion_estado_fecha'),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.fecha_evento}) - {self.get_estado_display()}"


class RegistroExcursion(models.Model):
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE, related_name="registros")
    usuario = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name="excursiones_registradas")
    asistio = models.BooleanField("Asistió", null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('excursion', 'usuario')
        indexes = [
            models.Index(fields=['usuario', 'fecha_registro'], name='idx_reg_usuario_fecha'),
            models.Index(fields=['excursion', 'usuario'], name='idx_reg_excursion_usuario'),
        ]

    def __str__(self):
        return f"{self.usuario} -> {self.excursion}"
