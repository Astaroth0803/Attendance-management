from datetime import date, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Max
from django.shortcuts import get_object_or_404
from core.models import Beneficiary, Activity
from .models import AttendanceRecord, Excursion
from organizations.security import get_tenant_or_deny

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    org = get_tenant_or_deny(request)
    today = date.today()
    
    # Basic Stats — filtered by organization
    attendances_today = AttendanceRecord.objects.filter(date=today, organization=org).count()
    active_users = Beneficiary.objects.filter(is_active=True, organization=org).count()
    
    # Calculate Trends (Today vs Yesterday for attendances, and overall growth for users)
    yesterday_date = today - timedelta(days=1)
    attendances_yesterday = AttendanceRecord.objects.filter(date=yesterday_date, organization=org).count()
    
    # Simple percentage difference. Safe against zero division.
    if attendances_yesterday == 0:
        attendances_trend = 100 if attendances_today > 0 else 0
    else:
        attendances_trend = round(((attendances_today - attendances_yesterday) / attendances_yesterday) * 100)
    
    # Basic growth trend for active users. Compare users created before this week.
    last_week_date = today - timedelta(days=7)
    users_last_week = Beneficiary.objects.filter(is_active=True, organization=org, created_at__lt=last_week_date).count()
    if users_last_week == 0:
        users_trend = 100 if active_users > 0 else 0
    else:
        users_trend = round(((active_users - users_last_week) / users_last_week) * 100)

    # Top Activity
    top_activity = Activity.objects.filter(organization=org).annotate(
        attendance_count=Count('events__attendances')
    ).order_by('-attendance_count').first()
    
    from django.db.models.functions import ExtractYear, ExtractMonth
    
    # Chart Data (Annual comparison, last 3 years)
    current_year = today.year
    years = [current_year, current_year - 1, current_year - 2]
    
    annual_data = {
        y: [0]*12 for y in years
    }
    
    qs = AttendanceRecord.objects.filter(
        date__year__in=years, organization=org
    ).annotate(
        year=ExtractYear('date'),
        month=ExtractMonth('date')
    ).values('year', 'month').annotate(count=Count('id'))
    
    for row in qs:
        annual_data[row['year']][row['month'] - 1] = row['count']
        
    chart_series = [
        {'name': str(y), 'data': annual_data[y]} for y in years
    ]

    # Top 5 Attendees
    top_attendees_qs = Beneficiary.objects.filter(organization=org).annotate(
        attendance_count=Count('attendances')
    ).filter(attendance_count__gt=0).order_by('-attendance_count')[:5]
    
    top_attendees = [
        {
            'id': b.id,
            'name': f"{b.first_name} {b.last_name}",
            'ci': b.ci,
            'attendance_count': b.attendance_count
        } for b in top_attendees_qs
    ]

    return Response({
        'attendances_today': attendances_today,
        'attendances_trend': attendances_trend,
        'active_users': active_users,
        'users_trend': users_trend,
        'top_activity_name': top_activity.name if top_activity else 'N/A',
        'chart_data': chart_series,
        'top_attendees': top_attendees
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_report(request):
    org = get_tenant_or_deny(request)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    start_time = request.GET.get('start_time')  # format HH:MM
    end_time = request.GET.get('end_time')       # format HH:MM
    
    qs = AttendanceRecord.objects.filter(organization=org).select_related('beneficiary', 'event__activity')
    
    if start_date:
        qs = qs.filter(date__gte=start_date)
    if end_date:
        qs = qs.filter(date__lte=end_date)
    if start_time:
        qs = qs.filter(time__gte=start_time)
    if end_time:
        qs = qs.filter(time__lte=end_time)
        
    qs = qs.order_by('-date', '-time')
    
    data = []
    for r in qs:
        data.append({
            'id': r.id,
            'date': r.date.strftime('%Y-%m-%d'),
            'time': r.time.strftime('%H:%M') if r.time else '',
            'beneficiary_name': f"{r.beneficiary.first_name} {r.beneficiary.last_name}",
            'beneficiary_ci': r.beneficiary.ci,
            'activity_name': r.event.activity.name,
            'event_name': r.event.name,
        })
        
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_attendance_report(request):
    org = get_tenant_or_deny(request)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    qs = AttendanceRecord.objects.filter(organization=org).select_related('event__activity')
    
    if start_date:
        qs = qs.filter(date__gte=start_date)
    if end_date:
        qs = qs.filter(date__lte=end_date)
        
    # Group by Event (and Activity by string relation context in rendering)
    report_data = qs.values(
        'event__activity__name', 
        'event__name'
    ).annotate(
        attendees=Count('beneficiary', distinct=True)
    ).order_by('-attendees')
    
    data = []
    for r in report_data:
        data.append({
            'activity_name': r['event__activity__name'],
            'event_name': r['event__name'],
            'attendees': r['attendees']
        })
        
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_report(request):
    """
    Returns attendance count grouped by event (with event date), for the 'Por Evento' report.
    Query params: start_date, end_date
    """
    org = get_tenant_or_deny(request)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    qs = AttendanceRecord.objects.filter(organization=org).select_related('event__activity')

    if start_date:
        qs = qs.filter(date__gte=start_date)
    if end_date:
        qs = qs.filter(date__lte=end_date)

    report_data = qs.values(
        'event__id',
        'event__name',
        'event__date',
        'event__activity__name',
    ).annotate(
        attendees=Count('beneficiary', distinct=True)
    ).order_by('-attendees', 'event__activity__name')

    data = []
    for r in report_data:
        data.append({
            'event_id': r['event__id'],
            'event_name': r['event__name'],
            'event_date': r['event__date'].strftime('%Y-%m-%d') if r['event__date'] else '-',
            'activity_name': r['event__activity__name'],
            'attendees': r['attendees'],
        })

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def beneficiary_profile_report(request, pk):
    org = get_tenant_or_deny(request)
    b = get_object_or_404(Beneficiary, pk=pk, organization=org)
    
    total_attendance = AttendanceRecord.objects.filter(beneficiary=b, organization=org).count()
    
    # Breakdown by activity/event
    activities_data = AttendanceRecord.objects.filter(beneficiary=b, organization=org).values(
        'event__activity__name', 'event__name'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    recent_attendances = AttendanceRecord.objects.filter(
        beneficiary=b, organization=org
    ).select_related('event__activity').order_by('-date')[:5]
    
    recent_list = []
    for r in recent_attendances:
        recent_list.append({
            'date': r.date.strftime('%Y-%m-%d'),
            'activity': r.event.activity.name,
            'event': r.event.name
        })
        
    activity_list = []
    for a in activities_data:
        activity_list.append({
            'activity_name': a['event__activity__name'],
            'event_name': a['event__name'],
            'count': a['count']
        })
    
    profile_data = {
        'id': b.id,
        'first_name': b.first_name,
        'last_name': b.last_name,
        'ci': b.ci,
        'dob': b.dob.strftime('%Y-%m-%d') if b.dob else None,
        'sex': b.get_sex_display(),
        'sector': b.sector,
        'is_active': b.is_active,
        'created_at': b.created_at.strftime('%Y-%m-%d'),
        
        'stats': {
            'total_attendance': total_attendance,
            'top_activities': activity_list,
            'recent_history': recent_list
        }
    }
    
    return Response(profile_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_profile_report(request, pk):
    org = get_tenant_or_deny(request)
    act = get_object_or_404(Activity, pk=pk, organization=org)
    
    events_qs = act.events.annotate(attendance_count=Count('attendances')).order_by('-id')
    events_list = []
    
    total_attendance = 0
    for e in events_qs:
        events_list.append({
            'id': e.id,
            'name': e.name,
            'date': e.date.strftime('%Y-%m-%d') if e.date else None,
            'attendance_count': e.attendance_count
        })
        total_attendance += e.attendance_count

    profile_data = {
        'id': act.id,
        'name': act.name,
        'category': act.category,
        'deadline_date': act.deadline_date.strftime('%Y-%m-%d') if act.deadline_date else None,
        'description': act.description,
        'is_active': act.is_active,
        'image': act.image,
        'events': events_list,
        'total_attendance': total_attendance
    }
    
    return Response(profile_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_attendees_detail(request):
    """
    Returns the list of unique attendees for a given activity+event within a date range.
    Query params: activity_name, event_name, start_date, end_date
    """
    org = get_tenant_or_deny(request)
    activity_name = request.GET.get('activity_name', '')
    event_name = request.GET.get('event_name', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    qs = AttendanceRecord.objects.filter(organization=org).select_related('beneficiary', 'event__activity')

    if activity_name:
        qs = qs.filter(event__activity__name=activity_name)
    if event_name:
        qs = qs.filter(event__name=event_name)
    if start_date:
        qs = qs.filter(date__gte=start_date)
    if end_date:
        qs = qs.filter(date__lte=end_date)

    qs = qs.order_by('beneficiary__first_name', 'beneficiary__last_name')

    # Unique attendees: one row per beneficiary (most recent attendance date shown)
    seen = {}
    for r in qs:
        bid = r.beneficiary.id
        if bid not in seen:
            seen[bid] = {
                'nombre': f"{r.beneficiary.first_name} {r.beneficiary.last_name}",
                'cedula': r.beneficiary.ci or '-',
                'sector': r.beneficiary.sector or '-',
                'ultima_asistencia': r.date.strftime('%Y-%m-%d'),
                'ultima_hora': r.time.strftime('%H:%M') if r.time else '',
                'total_visitas': 0,
            }
        seen[bid]['total_visitas'] += 1
        # keep the most recent date
        if r.date.strftime('%Y-%m-%d') > seen[bid]['ultima_asistencia']:
            seen[bid]['ultima_asistencia'] = r.date.strftime('%Y-%m-%d')
            seen[bid]['ultima_hora'] = r.time.strftime('%H:%M') if r.time else ''

    return Response(list(seen.values()))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_chart_data(request):
    """
    Returns daily attendance counts for the given date range.
    Query params: start_date, end_date
    """
    org = get_tenant_or_deny(request)
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if not start_date_str or not end_date_str:
        # Default: last 7 days
        end_dt = date.today()
        start_dt = end_dt - timedelta(days=6)
    else:
        from datetime import datetime
        start_dt = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_dt = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Build list of all days in range
    delta = (end_dt - start_dt).days + 1
    days = [start_dt + timedelta(days=i) for i in range(delta)]

    # Aggregate attendance per day
    qs = AttendanceRecord.objects.filter(
        date__gte=start_dt, date__lte=end_dt, organization=org
    ).values('date').annotate(count=Count('id')).order_by('date')

    counts_by_date = {r['date']: r['count'] for r in qs}

    labels = [d.strftime('%d %b') for d in days]
    data = [counts_by_date.get(d, 0) for d in days]

    return Response({'labels': labels, 'data': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def system_notifications(request):
    """
    Returns a unified list of system alerts/notifications:
    - Birthdays (Today and next 7 days)
    - Activities close to deadline
    - Excursions that are past their date but not marked as finished
    """
    org = get_tenant_or_deny(request)
    today = date.today()
    notifications = []
    
    from django.db.models.functions import ExtractMonth, ExtractDay
    upcoming_limit = today + timedelta(days=7)
    
    active_bens = Beneficiary.objects.filter(
        is_active=True, dob__isnull=False, organization=org
    ).annotate(
        birth_month=ExtractMonth('dob'),
        birth_day=ExtractDay('dob')
    )
    
    for b in active_bens:
        try:
            bday_this_year = date(today.year, b.birth_month, b.birth_day)
        except ValueError:
            bday_this_year = date(today.year, 2, 28)
            
        if today <= bday_this_year <= upcoming_limit:
            if bday_this_year == today:
                msg = f"¡Hoy es el cumpleaños de {b.first_name} {b.last_name}!"
            else:
                msg = f"{b.first_name} {b.last_name} cumple años el {bday_this_year.strftime('%d/%m')}."
                
            notifications.append({
                'id': f'bday_{b.id}',
                'type': 'birthday',
                'title': 'Cumpleaños',
                'message': msg,
                'date': bday_this_year.strftime('%Y-%m-%d'),
                'is_urgent': bday_this_year == today
            })
            
    # 2. Expiring Activities
    expiring_acts = Activity.objects.filter(
        is_active=True, 
        deadline_date__isnull=False,
        deadline_date__gte=today,
        deadline_date__lte=upcoming_limit,
        organization=org
    )
    for act in expiring_acts:
        notifications.append({
            'id': f'act_{act.id}',
            'type': 'activity',
            'title': 'Actividad por expirar',
            'message': f"La actividad '{act.name}' expira el {act.deadline_date.strftime('%d/%m')}.",
            'date': act.deadline_date.strftime('%Y-%m-%d'),
            'is_urgent': act.deadline_date == today
        })
        
    # 3. Expired Excursions (Not finalized)
    expired_excursions = Excursion.objects.filter(
        fecha_evento__lt=today, organization=org
    ).exclude(estado='finalizado').exclude(estado='cancelado')
    
    for exc in expired_excursions:
        notifications.append({
            'id': f'exc_{exc.id}',
            'type': 'warning',
            'title': 'Excursión Pendiente',
            'message': f"La excursión '{exc.nombre}' ya pasó ({exc.fecha_evento.strftime('%d/%m')}) y sigue en estado '{exc.get_estado_display()}'.",
            'date': exc.fecha_evento.strftime('%Y-%m-%d'),
            'is_urgent': True
        })
        
        # Sort notifications by urgency and date
    notifications.sort(key=lambda x: (not x['is_urgent'], x['date']))
    
    return Response(notifications)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard(request):
    """
    Devuelve los 3/5 mayores asistentes del mes en curso, con insignia calculada.
    """
    org = get_tenant_or_deny(request)
    today = date.today()
    start_of_month = date(today.year, today.month, 1)

    qs = Beneficiary.objects.filter(organization=org, is_active=True).annotate(
        monthly_attendances=Count('attendances', filter=models.Q(attendances__date__gte=start_of_month))
    ).filter(monthly_attendances__gt=0).order_by('-monthly_attendances')[:5]

    data = []
    medals = ['oro', 'plata', 'bronce']
    
    for i, b in enumerate(qs):
        badge = medals[i] if i < len(medals) else 'destacado'
        data.append({
            'id': b.id,
            'name': f"{b.first_name} {b.last_name}",
            'ci': b.ci,
            'attendances': b.monthly_attendances,
            'badge': badge,
            'rank': i + 1
        })
        
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retention_risk_report(request):
    """
    Encuentra usuarios que asistían pero han dejado de venir en los últimos 15 días.
    Criterio base: Vinieron al menos 3 veces el mes pasado, pero 0 veces en los últimos 15 días.
    """
    org = get_tenant_or_deny(request)
    today = date.today()
    
    from dateutil.relativedelta import relativedelta
    first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day_last_month = today.replace(day=1) - timedelta(days=1)
    
    risk_threshold_date = today - timedelta(days=15)

    # Buscar usuarios con >= 3 visitas el mes pasado
    old_active_users = AttendanceRecord.objects.filter(
        organization=org,
        date__gte=first_day_last_month,
        date__lte=last_day_last_month
    ).values('beneficiary').annotate(
        count=Count('id')
    ).filter(count__gte=3)
    
    candidate_bids = [u['beneficiary'] for u in old_active_users]

    # Averiguar cuántos de estos NO han venido en los últimos 15 días
    # Se obtienen las visitas recientes de estos candidatos
    recent_attendances = AttendanceRecord.objects.filter(
        organization=org,
        beneficiary_id__in=candidate_bids,
        date__gte=risk_threshold_date
    ).values_list('beneficiary_id', flat=True).distinct()
    
    at_risk_bids = set(candidate_bids) - set(recent_attendances)

    at_risk_users = Beneficiary.objects.filter(id__in=at_risk_bids).order_by('first_name', 'last_name')
    
    data = []
    for b in at_risk_users:
        # Get exact last attendance
        last_rec = AttendanceRecord.objects.filter(beneficiary=b).order_by('-date').first()
        data.append({
            'id': b.id,
            'name': f"{b.first_name} {b.last_name}",
            'ci': b.ci,
            'phone': getattr(b, 'phone', 'No registrado'), # Assuming phone might not exist but placeholder
            'sector': b.sector,
            'last_attendance': last_rec.date.strftime('%Y-%m-%d') if last_rec else '-',
            'days_since': (today - last_rec.date).days if last_rec else 0
        })

    # Sort descending by risk (days since last attendance)
    data.sort(key=lambda x: x['days_since'], reverse=True)
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_attendance_chart(request, pk):
    """
    Returns daily attendance data for a specific activity over the last 30 days.
    """
    org = get_tenant_or_deny(request)
    activity = get_object_or_404(Activity, pk=pk, organization=org)
    
    today = date.today()
    start_date = today - timedelta(days=30)
    
    qs = AttendanceRecord.objects.filter(
        organization=org,
        event__activity=activity,
        date__gte=start_date
    ).values('date').annotate(total=Count('id')).order_by('date')
    
    date_dict = {str(start_date + timedelta(days=i)): 0 for i in range(31)}
    for r in qs:
        date_dict[str(r['date'])] = r['total']
        
    dates = list(date_dict.keys())
    totals = list(date_dict.values())
    
    return Response({
        'categories': dates,
        'series': [{'name': 'Asistencias', 'data': totals}]
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_unique_attendees(request, pk):
    """
    Returns unique attendees for a specific activity, counting how many times they attended.
    """
    org = get_tenant_or_deny(request)
    activity = get_object_or_404(Activity, pk=pk, organization=org)
    
    attendees_qs = AttendanceRecord.objects.filter(
        organization=org,
        event__activity=activity
    ).values(
        'beneficiary__id', 
        'beneficiary__first_name', 
        'beneficiary__last_name', 
        'beneficiary__ci'
    ).annotate(
        total_visits=Count('id'),
        last_visit=Max('date')
    ).order_by('-total_visits')
    
    data = []
    for a in attendees_qs:
        data.append({
            'id': a['beneficiary__id'],
            'name': f"{a['beneficiary__first_name']} {a['beneficiary__last_name']}",
            'ci': a['beneficiary__ci'],
            'total_visits': a['total_visits'],
            'last_visit': str(a['last_visit'])
        })
        
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def beneficiary_attendances(request, pk):
    org = get_tenant_or_deny(request)
    beneficiary = get_object_or_404(Beneficiary, pk=pk, organization=org)
    
    # Get all historical attendances for this beneficiary
    attendances = AttendanceRecord.objects.filter(
        organization=org,
        beneficiary=beneficiary
    ).select_related('event__activity').order_by('-date')
    
    data = []
    for a in attendances:
        data.append({
            'id': a.id,
            'date': str(a.date),
            'activity_name': a.event.activity.name if a.event and a.event.activity else 'General',
            'event_name': a.event.name if a.event else 'Sin Evento',
        })
        
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def beneficiary_chart(request, pk):
    """
    Returns the attendance count grouped by month for the last 6 months 
    for a specific beneficiary.
    """
    org = get_tenant_or_deny(request)
    beneficiary = get_object_or_404(Beneficiary, pk=pk, organization=org)
    
    today = date.today()
    six_months_ago = today - timedelta(days=180)
    
    # Group by year-month
    attendances_qs = AttendanceRecord.objects.filter(
        organization=org,
        beneficiary=beneficiary,
        date__gte=six_months_ago
    ).values('date__year', 'date__month').annotate(total=Count('id')).order_by('date__year', 'date__month')
    
    # Fill missing months safely without complex DB functions
    months_map = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun', 
                 7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
    
    results = {}
    for i in range(5, -1, -1):
        target_date = today - timedelta(days=i*30)
        key = f"{target_date.year}-{target_date.month}"
        results[key] = {
            'label': f"{months_map[target_date.month]} {target_date.year}",
            'total': 0
        }
        
    for a in attendances_qs:
        key = f"{a['date__year']}-{a['date__month']}"
        if key in results:
            results[key]['total'] = a['total']
            
    categories = []
    series_data = []
    
    # Extract in order
    for v in results.values():
        categories.append(v['label'])
        series_data.append(v['total'])
        
    # Remove early zeros if they never attended before the middle
    return Response({
        'categories': categories,
        'series': [{'name': 'Asistencias', 'data': series_data}]
    })
