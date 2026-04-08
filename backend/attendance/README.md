# Attendance Module

## Descripción
El módulo `attendance` gestiona el seguimiento del registro de asistencia de los beneficiarios a diversos eventos regulares y excursiones. Permite llevar un control detallado de las presencias.

## Casos de Uso
1. **Asistencia Regular**: Registro de asistencias para los beneficiarios en `Event`.
2. **Excursiones**: Control de los requisitos, inscripción, el límite por edades y asistencia a eventos de tipo `Excursion`.

## Archivos Principales
- **models.py**: Contiene los modelos `AttendanceRecord`, `Excursion` y `RegistroExcursion`.
- **services.py**: Lógica de negocio encapsulada para procesar registros de asistencia o inscripciones.
- **views.py / api_views.py**: Controladores de endpoints para interactuar con la asistencia.
