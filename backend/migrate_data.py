import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from organizations.models import Organization
from accounts.models import User
from core.models import Beneficiary, Activity, Event
from attendance.models import AttendanceRecord, Excursion, RegistroExcursion

def migrate():
    # 1. Create Default Organization
    org, created = Organization.objects.get_or_create(
        slug='las-mananitas',
        defaults={
            'name': 'Centro Juvenil Las Mañanitas'
        }
    )
    if created:
        print(f"Created organization: {org.name}")
    else:
        print(f"Found existing organization: {org.name}")

    # 2. Assign to all models
    models_to_update = [
        User, Beneficiary, Activity, Event, 
        AttendanceRecord, Excursion, RegistroExcursion
    ]

    for model in models_to_update:
        count = model.objects.filter(organization__isnull=True).update(organization=org)
        print(f"Updated {count} records in {model.__name__}")

    print("Data migration complete.")

if __name__ == '__main__':
    migrate()
