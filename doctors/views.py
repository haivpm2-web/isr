from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from functools import wraps
from .models import DoctorProfile
from patients.models import PatientProfile, ECGRecord, LegRecoveryRecord, ExaminationRecord, PrescriptionRecord, RehabilitationAssessment
from .forms import ECGRecordForm, LegRecoveryForm, ExaminationRecordForm, PrescriptionRecordForm, RehabilitationAssessmentForm, PatientBioForm


# ── Decorators and access helpers ─────────────────────────────────────────────

def clinical_staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_clinical_staff():
            messages.error(request, 'Trang này chỉ dành cho nhân viên lâm sàng.')
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_doctor():
            messages.error(request, 'Trang này chỉ dành cho bác sĩ.')
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def nurse_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_nurse_user():
            messages.error(request, 'Trang này chỉ dành cho điều dưỡng / y tá.')
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def _get_doctor(request):
    try:
        return request.user.doctor_profile
    except DoctorProfile.DoesNotExist:
        return None


def _get_accessible_patients(request):
    queryset = PatientProfile.objects.select_related('user', 'doctor__user')
    if request.user.is_doctor():
        profile = _get_doctor(request)
        if not profile:
            return queryset.none()
        return queryset.filter(doctor=profile)
    if request.user.is_nurse_user():
        return queryset.all()
    return queryset.none()


def _get_accessible_patient_or_404(request, patient_id):
    return get_object_or_404(_get_accessible_patients(request), id=patient_id)


# ── Views ─────────────────────────────────────────────────────────────────────

@clinical_staff_required
def dashboard(request):
    profile = _get_doctor(request) if request.user.is_doctor() else None
    if request.user.is_doctor() and not profile:
        messages.error(request, 'Không tìm thấy hồ sơ bác sĩ.')
        return redirect('accounts:login')

    patients = _get_accessible_patients(request)
    recent_ecgs = ECGRecord.objects.filter(
        patient__in=patients
    ).select_related('patient__user').order_by('-recorded_at')[:6]

    recent_recoveries = LegRecoveryRecord.objects.filter(
        patient__in=patients
    ).select_related('patient__user').order_by('-recorded_at')[:6]

    critical_patients = []
    recovered_patients = []
    for patient in patients:
        latest_ecg = patient.latest_ecg
        latest_recovery = patient.latest_recovery
        reasons = []
        severity = 0

        if latest_ecg and latest_ecg.is_abnormal:
            reasons.append('ECG bất thường')
            severity += 3
        if latest_recovery:
            if latest_recovery.recovery_percentage < 45:
                reasons.append('Phục hồi chậm')
                severity += 2
            if latest_recovery.pain_level >= 7:
                reasons.append('Đau cao')
                severity += 2
            if latest_recovery.fatigue_index is not None and latest_recovery.fatigue_index >= 7:
                reasons.append('Mệt nhiều')
                severity += 1

        if reasons:
            critical_patients.append({
                'patient': patient,
                'latest_ecg': latest_ecg,
                'latest_recovery': latest_recovery,
                'reasons': reasons,
                'severity': severity,
            })

        if latest_recovery and latest_recovery.recovery_percentage >= 80 and latest_recovery.pain_level <= 3:
            if not latest_ecg or not latest_ecg.is_abnormal:
                recovered_patients.append({
                    'patient': patient,
                    'latest_ecg': latest_ecg,
                    'latest_recovery': latest_recovery,
                })

    critical_patients.sort(key=lambda item: item['severity'], reverse=True)
    recovered_patients.sort(
        key=lambda item: (
            item['latest_recovery'].recovery_percentage,
            -(item['latest_recovery'].pain_level or 0),
        ),
        reverse=True,
    )

    context = {
        'profile': profile,
        'staff_user': request.user,
        'patients': patients,
        'patient_count': patients.count(),
        'recent_ecgs': recent_ecgs,
        'recent_recoveries': recent_recoveries,
        'abnormal_ecg_count': ECGRecord.objects.filter(patient__in=patients, is_abnormal=True).count(),
        'critical_patients': critical_patients[:4],
        'critical_patient_count': len(critical_patients),
        'recovered_patients': recovered_patients[:4],
        'recovered_patient_count': len(recovered_patients),
    }
    return render(request, 'doctors/dashboard.html', context)


@clinical_staff_required
def patient_list(request):
    profile = _get_doctor(request) if request.user.is_doctor() else None
    patients = _get_accessible_patients(request)
    return render(request, 'doctors/patient_list.html', {
        'profile': profile,
        'patients': patients,
    })


@clinical_staff_required
def patient_detail(request, patient_id):
    profile = _get_doctor(request) if request.user.is_doctor() else None
    patient = _get_accessible_patient_or_404(request, patient_id)
    ecg_records = patient.ecg_records.all()[:10]
    recovery_records = patient.recovery_records.all()[:10]
    recent_examinations = patient.examination_records.all().order_by('-exam_date')[:5]
    recent_prescriptions = patient.prescriptions.all().order_by('-issued_at')[:5]
    recent_rehab_assessments = patient.rehab_assessments.all().order_by('-assessed_at')[:5]
    latest_ecg = patient.latest_ecg
    latest_recovery = patient.latest_recovery

    case_flags = []
    if latest_ecg and latest_ecg.is_abnormal:
        case_flags.append({
            'level': 'danger',
            'icon': 'fa-heart-pulse',
            'text': f'ECG gần nhất bất thường: {latest_ecg.get_rhythm_display()}.',
        })
    if latest_recovery:
        if latest_recovery.recovery_percentage < 45:
            case_flags.append({
                'level': 'warning',
                'icon': 'fa-person-walking-with-cane',
                'text': f'Phục hồi hiện {latest_recovery.recovery_percentage}%, tiến triển còn chậm.',
            })
        if latest_recovery.pain_level >= 7:
            case_flags.append({
                'level': 'danger',
                'icon': 'fa-triangle-exclamation',
                'text': f'Đau mức {latest_recovery.pain_level}/10, cần giảm tải và theo dõi thêm.',
            })
        if latest_recovery.fatigue_index is not None and latest_recovery.fatigue_index >= 7:
            case_flags.append({
                'level': 'warning',
                'icon': 'fa-battery-quarter',
                'text': f'Fatigue {latest_recovery.fatigue_index}/10 sau tập luyện.',
            })

    if not case_flags:
        case_flags.append({
            'level': 'success',
            'icon': 'fa-circle-check',
            'text': 'Ca điều trị đang ổn định, tiếp tục theo phác đồ hiện tại.',
        })

    return render(request, 'doctors/patient_detail.html', {
        'profile': profile,
        'patient': patient,
        'ecg_records': ecg_records,
        'recovery_records': recovery_records,
        'recent_examinations': recent_examinations,
        'recent_prescriptions': recent_prescriptions,
        'recent_rehab_assessments': recent_rehab_assessments,
        'latest_ecg': latest_ecg,
        'latest_recovery': latest_recovery,
        'case_flags': case_flags,
    })


@nurse_required
def add_ecg(request, patient_id):
    patient = _get_accessible_patient_or_404(request, patient_id)
    form = ECGRecordForm(request.POST or None, initial={'recorded_at': timezone.now().strftime('%Y-%m-%dT%H:%M')})

    if request.method == 'POST' and form.is_valid():
        ecg = form.save(commit=False)
        ecg.patient = patient
        ecg.recorded_by = request.user
        ecg.save()
        messages.success(request, 'Đã thêm kết quả ECG thành công.')
        return redirect('doctors:patient_detail', patient_id=patient.id)

    return render(request, 'doctors/add_ecg.html', {'form': form, 'patient': patient})


@nurse_required
def add_recovery(request, patient_id):
    patient = _get_accessible_patient_or_404(request, patient_id)
    form = LegRecoveryForm(request.POST or None, initial={'recorded_at': timezone.now().strftime('%Y-%m-%dT%H:%M')})

    if request.method == 'POST' and form.is_valid():
        rec = form.save(commit=False)
        rec.patient = patient
        rec.recorded_by = request.user
        rec.save()
        messages.success(request, 'Đã thêm dữ liệu phục hồi thành công.')
        return redirect('doctors:patient_detail', patient_id=patient.id)

    return render(request, 'doctors/add_recovery.html', {'form': form, 'patient': patient})


# ── Patient bio / medical history ─────────────────────────────────────────────

@nurse_required
def edit_patient_bio(request, patient_id):
    patient = _get_accessible_patient_or_404(request, patient_id)
    bio_fields = [
        'chief_complaint', 'present_illness', 'past_medical_history',
        'surgical_history', 'family_history', 'social_history',
        'allergies', 'current_medications', 'treatment_status', 'surgery_status', 'surgery_name', 'surgery_date', 'postoperative_status', 'discharge_date', 'discharge_condition', 'notes',
    ]
    initial = {f: getattr(patient, f) for f in bio_fields}

    form = PatientBioForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        for f in bio_fields:
            setattr(patient, f, form.cleaned_data.get(f, ''))
        patient.save()
        messages.success(request, 'Đã cập nhật tiểu sử bệnh lý.')
        return redirect('doctors:patient_detail', patient_id=patient.id)

    return render(request, 'doctors/edit_patient_bio.html', {'form': form, 'patient': patient})


# ── Examination (visit history) ───────────────────────────────────────────────

@nurse_required
def add_examination(request, patient_id):
    patient = _get_accessible_patient_or_404(request, patient_id)
    form = ExaminationRecordForm(
        request.POST or None,
        initial={'exam_date': timezone.now().strftime('%Y-%m-%dT%H:%M')},
    )

    if request.method == 'POST' and form.is_valid():
        exam = form.save(commit=False)
        exam.patient = patient
        exam.examined_by = request.user
        exam.save()
        messages.success(request, 'Đã thêm lịch sử khám thành công.')
        return redirect('doctors:patient_detail', patient_id=patient.id)

    return render(request, 'doctors/add_examination.html', {'form': form, 'patient': patient})


@clinical_staff_required
def examination_list(request, patient_id):
    patient = _get_accessible_patient_or_404(request, patient_id)
    records = patient.examination_records.all()
    return render(request, 'doctors/examination_list.html', {
        'patient': patient, 'records': records,
    })


@clinical_staff_required
def examination_detail(request, patient_id, exam_id):
    patient = _get_accessible_patient_or_404(request, patient_id)
    exam = get_object_or_404(ExaminationRecord, id=exam_id, patient=patient)
    return render(request, 'doctors/examination_detail.html', {
        'patient': patient, 'exam': exam,
    })


@doctor_required
def add_prescription(request, patient_id):
    profile = _get_doctor(request)
    if not profile:
        return redirect('accounts:login')

    patient = _get_accessible_patient_or_404(request, patient_id)
    exam_id = request.GET.get('exam_id') or request.POST.get('exam_id')
    current_exam = None
    if exam_id:
        current_exam = get_object_or_404(ExaminationRecord, id=exam_id, patient=patient)

    latest_exam = current_exam or patient.examination_records.first()
    initial = {
        'issued_at': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'diagnosis': patient.diagnosis,
        'clinical_notes': getattr(latest_exam, 'clinical_findings', ''),
        'follow_up_date': getattr(latest_exam, 'follow_up_date', None),
    }
    if latest_exam:
        initial.update({
            'blood_pressure_systolic': latest_exam.blood_pressure_systolic,
            'blood_pressure_diastolic': latest_exam.blood_pressure_diastolic,
            'heart_rate': latest_exam.heart_rate,
            'respiratory_rate': latest_exam.respiratory_rate,
            'temperature': latest_exam.temperature,
            'spo2': latest_exam.spo2,
            'weight': latest_exam.weight,
        })

    form = PrescriptionRecordForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        prescription = form.save(commit=False)
        prescription.patient = patient
        prescription.prescribed_by = request.user
        prescription.examination = current_exam
        prescription.save()
        messages.success(request, 'Đã tạo chỉ định thuốc và đơn thuốc thành công.')
        return redirect('doctors:prescription_detail', patient_id=patient.id, prescription_id=prescription.id)

    return render(request, 'doctors/add_prescription.html', {
        'form': form,
        'patient': patient,
        'latest_exam': latest_exam,
        'current_exam': current_exam,
    })


@clinical_staff_required
def prescription_list(request, patient_id):
    patient = _get_accessible_patient_or_404(request, patient_id)
    records = patient.prescriptions.all()
    return render(request, 'doctors/prescription_list.html', {
        'patient': patient,
        'records': records,
    })


@clinical_staff_required
def prescription_detail(request, patient_id, prescription_id):
    patient = _get_accessible_patient_or_404(request, patient_id)
    prescription = get_object_or_404(PrescriptionRecord, id=prescription_id, patient=patient)
    return render(request, 'doctors/prescription_detail.html', {
        'patient': patient,
        'prescription': prescription,
    })


# ── Rehabilitation assessment ─────────────────────────────────────────────────

@nurse_required
def add_rehab_assessment(request, patient_id):
    patient = _get_accessible_patient_or_404(request, patient_id)
    form = RehabilitationAssessmentForm(
        request.POST or None,
        initial={'assessed_at': timezone.now().strftime('%Y-%m-%dT%H:%M')},
    )

    if request.method == 'POST' and form.is_valid():
        ra = form.save(commit=False)
        ra.patient = patient
        ra.assessed_by = request.user
        ra.save()
        messages.success(request, 'Đã thêm đánh giá phục hồi chức năng.')
        return redirect('doctors:rehab_assessment_detail', patient_id=patient.id, ra_id=ra.id)

    return render(request, 'doctors/add_rehab_assessment.html', {'form': form, 'patient': patient})


@clinical_staff_required
def rehab_assessment_list(request, patient_id):
    patient = _get_accessible_patient_or_404(request, patient_id)
    records = patient.rehab_assessments.all()
    return render(request, 'doctors/rehab_assessment_list.html', {
        'patient': patient, 'records': records,
    })


@clinical_staff_required
def rehab_assessment_detail(request, patient_id, ra_id):
    patient = _get_accessible_patient_or_404(request, patient_id)
    ra = get_object_or_404(RehabilitationAssessment, id=ra_id, patient=patient)
    return render(request, 'doctors/rehab_assessment_detail.html', {
        'patient': patient, 'ra': ra,
    })

