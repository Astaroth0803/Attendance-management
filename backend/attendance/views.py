from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404
from core.models import Beneficiary
from .models import AttendanceRecord, Excursion, RegistroExcursion
from .serializers import AttendanceRecordSerializer, ExcursionSerializer, RegistroExcursionSerializer
from .services import add_participant, change_state, mark_attendance
from organizations.security import TenantViewMixin

class AttendanceRecordViewSet(TenantViewMixin, viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all().select_related('beneficiary', 'event')
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # We must call super().perform_create to get the organization injected by TenantViewMixin
        # but TenantViewMixin does serializer.save(organization=org).
        # We need to save with recorded_by too. Let's merge kwargs.
        org = getattr(self.request, 'organization', None)
        try:
            serializer.save(organization=org, recorded_by=self.request.user)
        except IntegrityError:
            raise ValidationError({'detail': 'El usuario ya tiene asistencia registrada para este evento hoy.'})

class PublicAttendanceViewSet(TenantViewMixin, viewsets.ModelViewSet):
    """ Allows anyone to register attendance on the public form """
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post', 'options']

    def perform_create(self, serializer):
        try:
            super().perform_create(serializer)
        except IntegrityError:
            raise ValidationError({'detail': 'Ya has registrado tu asistencia para este evento hoy.'})

class ExcursionViewSet(TenantViewMixin, viewsets.ModelViewSet):
    queryset = Excursion.objects.prefetch_related('registros__usuario').all().order_by('-created_at')
    serializer_class = ExcursionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        excursion = self.get_object()
        usuario_id = request.data.get('usuario_id')
        if not usuario_id:
            return Response({"detail": "usuario_id es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        usuario = get_object_or_404(Beneficiary, pk=usuario_id)
        
        try:
            add_participant(excursion, usuario)
            return Response({"detail": "Participante registrado exitosamente."}, status=status.HTTP_201_CREATED)
        except DjangoValidationError as e:
            return Response({"detail": list(e)[0]}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='change-state')
    def advance_state(self, request, pk=None):
        excursion = self.get_object()
        new_estado = request.data.get('estado')
        if not new_estado:
            return Response({"detail": "estado es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            change_state(excursion, new_estado)
            return Response({"detail": "Estado actualizado exitosamente."}, status=status.HTTP_200_OK)
        except DjangoValidationError as e:
            return Response({"detail": list(e)[0]}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def attendance(self, request, pk=None):
        excursion = self.get_object()
        attendance_dict = request.data.get('attendance', {})
        if not attendance_dict or not isinstance(attendance_dict, dict):
            return Response({"detail": "Se requiere dict 'attendance'."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            updates = mark_attendance(excursion, attendance_dict)
            return Response({"detail": f"Asistencia actualizada para {updates} participantes."}, status=status.HTTP_200_OK)
        except DjangoValidationError as e:
            return Response({"detail": list(e)[0]}, status=status.HTTP_400_BAD_REQUEST)
