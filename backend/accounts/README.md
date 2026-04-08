# Accounts Module

## Descripción
El módulo `accounts` se encarga de la gestión de usuarios del sistema y la autenticación. Define roles de los usuarios (como Administrador y Profesor) permitiendo manejar diferentes niveles de acceso.

## Archivos Principales
- **models.py**: Define el modelo `User` que hereda de `AbstractUser` de Django, añadiendo el campo de rol (`Role.ADMIN` y `Role.PROFESSOR`).
- **views.py**: Contiene la lógica para el registro, inicio de sesión y gestión de perfiles.
- **serializers.py**: Serializadores de DRF para convertir instancias de `User` desde y hacia JSON.
