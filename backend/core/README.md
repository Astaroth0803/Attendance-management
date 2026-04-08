# Core Module

## Descripción
El módulo `core` contiene las entidades principales y fundamentales compartidas del sistema. Gestiona los datos maestros (master data) como los Beneficiarios (`Beneficiary`), las Actividades globales (`Activity`) y sus Eventos (`Event`).

## Casos de Uso
1. **Padrón de Beneficiarios**: Registro, modificación y consulta de la información personal de los participantes.
2. **Gestión de Actividades**: Creación de actividades permanentes o eventuales.

## Archivos Principales
- **models.py**: Define `Beneficiary`, `Activity` y `Event`.
- **views.py**: ViewSets para exponer estas entidades a través de la API REST.
- **serializers.py**: Transformación de las entidades a JSON para uso del frontend.
