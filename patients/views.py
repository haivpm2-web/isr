import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from functools import wraps
from .models import PatientProfile, ECGRecord, LegRecoveryRecord


# ── Decorator ─────────────────────────────────────────────────────────────────

def patient_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_patient_user():
            messages.error(request, 'Trang này chỉ dành cho bệnh nhân.')
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def _get_profile(request):
    try:
        return request.user.patient_profile
    except PatientProfile.DoesNotExist:
        return None


# ── Views ─────────────────────────────────────────────────────────────────────

@patient_required
def dashboard(request):
    profile = _get_profile(request)
    if not profile:
        messages.error(request, 'Không tìm thấy hồ sơ bệnh nhân.')
        return redirect('accounts:login')

    latest_ecg = profile.latest_ecg
    latest_recovery = profile.latest_recovery

    # HR trend – last 10 ECG records (oldest → newest for chart)
    ecg_qs = list(
        profile.ecg_records.order_by('recorded_at')
        .values('recorded_at', 'heart_rate', 'pr_interval', 'qrs_duration', 'qt_interval')[:10]
    )
    for row in ecg_qs:
        row['recorded_at'] = row['recorded_at'].strftime('%d/%m %H:%M')

    # Recovery trend – last 10 records
    rec_qs = list(
        profile.recovery_records.order_by('recorded_at')
        .values('recorded_at', 'recovery_percentage', 'muscle_strength', 'pain_level', 'heart_rate', 'spo2', 'fatigue_index', 'gait_speed', 'plantar_force')[:10]
    )
    for row in rec_qs:
        row['recorded_at'] = row['recorded_at'].strftime('%d/%m/%Y')

    alert_items = []
    if latest_ecg and latest_ecg.is_abnormal:
        alert_items.append({
            'level': 'danger',
            'icon': 'fa-heart-pulse',
            'text': f'ECG gần nhất ghi nhận {latest_ecg.get_rhythm_display().lower()}.',
        })
    if latest_recovery:
        if latest_recovery.recovery_percentage < 45:
            alert_items.append({
                'level': 'warning',
                'icon': 'fa-person-walking-with-cane',
                'text': f'Tỷ lệ phục hồi hiện ở mức {latest_recovery.recovery_percentage}%.',
            })
        if latest_recovery.pain_level >= 7:
            alert_items.append({
                'level': 'danger',
                'icon': 'fa-triangle-exclamation',
                'text': f'Mức độ đau hiện tại là {latest_recovery.pain_level}/10, cần theo dõi sát.',
            })
        if latest_recovery.fatigue_index is not None and latest_recovery.fatigue_index >= 7:
            alert_items.append({
                'level': 'warning',
                'icon': 'fa-battery-quarter',
                'text': f'Chỉ số mệt hiện là {latest_recovery.fatigue_index}/10.',
            })

    if not alert_items:
        alert_items.append({
            'level': 'success',
            'icon': 'fa-circle-check',
            'text': 'Các chỉ số gần đây đang ổn định, tiếp tục theo dõi đúng lịch.',
        })

    context = {
        'profile': profile,
        'latest_ecg': latest_ecg,
        'latest_recovery': latest_recovery,
        'ecg_count': profile.ecg_records.count(),
        'recovery_count': profile.recovery_records.count(),
        'ecg_chart_data': json.dumps(ecg_qs),
        'rec_chart_data': json.dumps(rec_qs),
        'alert_items': alert_items,
    }
    return render(request, 'patients/dashboard.html', context)


@patient_required
def ecg_list(request):
    profile = _get_profile(request)
    if not profile:
        return redirect('accounts:login')
    records = profile.ecg_records.all()
    return render(request, 'patients/ecg_list.html', {'profile': profile, 'records': records})


@patient_required
def ecg_detail(request, record_id):
    profile = _get_profile(request)
    if not profile:
        return redirect('accounts:login')
    record = get_object_or_404(ECGRecord, id=record_id, patient=profile)
    return render(request, 'patients/ecg_detail.html', {'profile': profile, 'record': record})


@patient_required
def recovery_dashboard(request):
    profile = _get_profile(request)
    if not profile:
        return redirect('accounts:login')

    records = profile.recovery_records.all()
    latest = records.first()

    # Chart trend data (oldest → newest)
    chart_qs = list(
        profile.recovery_records.order_by('recorded_at')
        .values('recorded_at', 'recovery_percentage', 'muscle_strength', 'pain_level', 'range_of_motion', 'heart_rate', 'spo2', 'fatigue_index', 'gait_speed', 'plantar_force')[:20]
    )
    for row in chart_qs:
        row['recorded_at'] = row['recorded_at'].strftime('%d/%m/%Y')

    return render(request, 'patients/recovery.html', {
        'profile': profile,
        'records': records,
        'latest': latest,
        'chart_data': json.dumps(chart_qs),
    })
