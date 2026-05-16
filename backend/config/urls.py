from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views import (
    BeneficiaryViewSet, ActivityViewSet, EventViewSet, UserViewSet,
    PublicBeneficiaryViewSet, PublicActivityViewSet
)
from attendance.views import AttendanceRecordViewSet, PublicAttendanceViewSet, ExcursionViewSet
from attendance.api_views import (
    dashboard_stats, attendance_report, activity_attendance_report, 
    beneficiary_profile_report, activity_profile_report, 
    event_attendees_detail, event_report, attendance_chart_data,
    system_notifications, leaderboard, retention_risk_report,
    activity_attendance_chart, activity_unique_attendees,
    beneficiary_chart, beneficiary_attendances
)

router = DefaultRouter()
# Secured Endpoints
router.register(r'beneficiaries', BeneficiaryViewSet, basename='beneficiaries')
router.register(r'activities', ActivityViewSet, basename='activities')
router.register(r'events', EventViewSet, basename='events')
router.register(r'attendance', AttendanceRecordViewSet, basename='attendance')
router.register(r'excursions', ExcursionViewSet, basename='excursions')
router.register(r'users', UserViewSet, basename='users')

# Public Endpoints
router.register(r'public/beneficiaries', PublicBeneficiaryViewSet, basename='public-beneficiaries')
router.register(r'public/activities', PublicActivityViewSet, basename='public-activities')
router.register(r'public/attendance', PublicAttendanceViewSet, basename='public-attendance')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/superadmin/', include('organizations.urls')),
    path('api/dashboard-stats/', dashboard_stats, name='dashboard_stats'),
    path('api/reports/attendance/', attendance_report, name='attendance_report'),
    path('api/reports/activity-attendance/', activity_attendance_report, name='activity_attendance_report'),
    path('api/reports/beneficiary-profile/<int:pk>/', beneficiary_profile_report, name='beneficiary_profile_report'),
    path('api/reports/activity-profile/<int:pk>/', activity_profile_report, name='activity_profile_report'),
    path('api/reports/event-attendees/', event_attendees_detail, name='event_attendees_detail'),
    path('api/reports/event-report/', event_report, name='event_report'),
    path('api/reports/chart/', attendance_chart_data, name='attendance_chart_data'),
    path('api/reports/activity-chart/<int:pk>/', activity_attendance_chart, name='activity_attendance_chart'),
    path('api/reports/activity-attendees/<int:pk>/', activity_unique_attendees, name='activity_unique_attendees'),
    path('api/reports/beneficiary-chart/<int:pk>/', beneficiary_chart, name='beneficiary_chart'),
    path('api/reports/beneficiary-attendances/<int:pk>/', beneficiary_attendances, name='beneficiary_attendances'),
    path('api/dashboard/leaderboard/', leaderboard, name='leaderboard'),
    path('api/reports/retention-risk/', retention_risk_report, name='retention_risk_report'),
    path('api/notifications/', system_notifications, name='system_notifications'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
