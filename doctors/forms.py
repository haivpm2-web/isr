from django import forms
from patients.models import PatientProfile, ECGRecord, LegRecoveryRecord, ExaminationRecord, PrescriptionRecord, RehabilitationAssessment


class ECGRecordForm(forms.ModelForm):
    class Meta:
        model = ECGRecord
        fields = [
            'recorded_at', 'heart_rate',
            'pr_interval', 'qrs_duration', 'qt_interval', 'qtc_interval', 'rr_interval',
            'p_wave_amplitude', 'qrs_amplitude', 't_wave_amplitude',
            'st_change', 'rhythm', 'is_abnormal', 'notes',
        ]
        widgets = {
            'recorded_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control', 'min': 20, 'max': 300}),
            'pr_interval': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'qrs_duration': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'qt_interval': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'qtc_interval': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'rr_interval': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'p_wave_amplitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'qrs_amplitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            't_wave_amplitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'st_change': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'rhythm': forms.Select(attrs={'class': 'form-select'}),
            'is_abnormal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'recorded_at': 'Thời gian đo',
            'heart_rate': 'Nhịp tim (bpm)',
            'pr_interval': 'Khoảng PR (ms)',
            'qrs_duration': 'Thời gian QRS (ms)',
            'qt_interval': 'Khoảng QT (ms)',
            'qtc_interval': 'Khoảng QTc (ms)',
            'rr_interval': 'Khoảng RR (ms)',
            'p_wave_amplitude': 'Biên độ sóng P (mV)',
            'qrs_amplitude': 'Biên độ QRS (mV)',
            't_wave_amplitude': 'Biên độ sóng T (mV)',
            'st_change': 'Thay đổi đoạn ST (mm)',
            'rhythm': 'Loại nhịp',
            'is_abnormal': 'Có bất thường',
            'notes': 'Nhận xét / Kết luận',
        }


class LegRecoveryForm(forms.ModelForm):
    class Meta:
        model = LegRecoveryRecord
        fields = [
            'recorded_at', 'affected_leg',
            'muscle_strength', 'range_of_motion',
            'heart_rate', 'spo2', 'fatigue_index',
            'imu_velocity', 'imu_acceleration',
            'gait_speed', 'cadence', 'step_length', 'plantar_force',
            'pain_level', 'swelling_level',
            'walking_ability', 'recovery_percentage',
            'physical_therapy_notes', 'doctor_notes',
        ]
        widgets = {
            'recorded_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'affected_leg': forms.Select(attrs={'class': 'form-select'}),
            'muscle_strength': forms.Select(attrs={'class': 'form-select'}),
            'range_of_motion': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 180}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control', 'min': 30, 'max': 300}),
            'spo2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 50, 'max': 100}),
            'fatigue_index': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
            'imu_velocity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
            'imu_acceleration': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'gait_speed': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
            'cadence': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 0}),
            'step_length': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 0}),
            'plantar_force': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 0}),
            'pain_level': forms.Select(attrs={'class': 'form-select'}),
            'swelling_level': forms.Select(attrs={'class': 'form-select'}),
            'walking_ability': forms.Select(attrs={'class': 'form-select'}),
            'recovery_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'physical_therapy_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'doctor_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'recorded_at': 'Thời gian ghi nhận',
            'affected_leg': 'Chân bị ảnh hưởng',
            'muscle_strength': 'Sức mạnh cơ (MRC 0–5)',
            'range_of_motion': 'ROM (góc khớp, độ)',
            'heart_rate': 'Nhịp tim (HR, bpm)',
            'spo2': 'SpO₂ (%)',
            'fatigue_index': 'Mức mệt (fatigue index 0–10)',
            'imu_velocity': 'IMU velocity (m/s)',
            'imu_acceleration': 'IMU acceleration (m/s²)',
            'gait_speed': 'Tốc độ dáng đi (m/s)',
            'cadence': 'Cadence (bước/phút)',
            'step_length': 'Chiều dài bước (cm)',
            'plantar_force': 'Lực đạp chân / plantar force (N)',
            'pain_level': 'Mức độ đau (VAS 0–10)',
            'swelling_level': 'Mức độ sưng',
            'walking_ability': 'Khả năng đi lại',
            'recovery_percentage': 'Tỷ lệ phục hồi (%)',
            'physical_therapy_notes': 'Ghi chú vật lý trị liệu',
            'doctor_notes': 'Ghi chú bác sĩ',
        }


# ── Widget helper ─────────────────────────────────────────────────────────────
def _num(extra=None):
    attrs = {'class': 'form-control'}
    if extra:
        attrs.update(extra)
    return forms.NumberInput(attrs=attrs)

def _txt(rows=3):
    return forms.Textarea(attrs={'class': 'form-control', 'rows': rows})

def _sel():
    return forms.Select(attrs={'class': 'form-select'})

def _date():
    return forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})

def _datetime():
    return forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})


# ── PatientBioForm – tiểu sử bệnh lý ─────────────────────────────────────────
class PatientBioForm(forms.Form):
    """Cập nhật tiểu sử bệnh lý cho PatientProfile."""
    chief_complaint = forms.CharField(
        required=False, widget=_txt(3), label='Lý do vào viện / Triệu chứng chính')
    present_illness = forms.CharField(
        required=False, widget=_txt(4), label='Bệnh sử hiện tại')
    past_medical_history = forms.CharField(
        required=False, widget=_txt(4), label='Tiền sử bệnh lý')
    surgical_history = forms.CharField(
        required=False, widget=_txt(3), label='Tiền sử phẫu thuật')
    family_history = forms.CharField(
        required=False, widget=_txt(3), label='Tiền sử gia đình')
    social_history = forms.CharField(
        required=False, widget=_txt(3), label='Tiền sử xã hội')
    allergies = forms.CharField(
        required=False, widget=_txt(2), label='Dị ứng')
    current_medications = forms.CharField(
        required=False, widget=_txt(3), label='Thuốc đang dùng')
    treatment_status = forms.ChoiceField(
        choices=PatientProfile.TREATMENT_STATUS_CHOICES,
        required=True,
        widget=_sel(), label='Trạng thái điều trị')
    surgery_status = forms.ChoiceField(
        choices=PatientProfile.SURGERY_STATUS_CHOICES,
        required=True,
        widget=_sel(), label='Trạng thái phẫu thuật')
    surgery_name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Tên phẫu thuật / thủ thuật')
    surgery_date = forms.DateField(
        required=False, widget=_date(), label='Ngày phẫu thuật')
    postoperative_status = forms.ChoiceField(
        choices=PatientProfile.POSTOPERATIVE_STATUS_CHOICES,
        required=False, widget=_sel(), label='Tình trạng hậu phẫu')
    discharge_date = forms.DateField(
        required=False, widget=_date(), label='Ngày xuất viện')
    discharge_condition = forms.ChoiceField(
        choices=PatientProfile.DISCHARGE_CONDITION_CHOICES,
        required=False, widget=_sel(), label='Tình trạng xuất viện')
    notes = forms.CharField(
        required=False, widget=_txt(3), label='Ghi chú khác')

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('treatment_status')
        discharge_date = cleaned_data.get('discharge_date')
        discharge_condition = cleaned_data.get('discharge_condition')
        if status == 'discharged' and not discharge_condition:
            self.add_error('discharge_condition', 'Cần chọn tình trạng xuất viện.')
        if status == 'discharged' and not discharge_date:
            self.add_error('discharge_date', 'Cần nhập ngày xuất viện.')
        surgery_status = cleaned_data.get('surgery_status')
        surgery_name = cleaned_data.get('surgery_name')
        surgery_date = cleaned_data.get('surgery_date')
        postoperative_status = cleaned_data.get('postoperative_status')
        if surgery_status in {'indicated', 'planned', 'pre_op', 'post_op', 'completed'} and not surgery_name:
            self.add_error('surgery_name', 'Cần nhập tên phẫu thuật / thủ thuật.')
        if surgery_status in {'post_op', 'completed'} and not surgery_date:
            self.add_error('surgery_date', 'Cần nhập ngày phẫu thuật.')
        if surgery_status in {'post_op', 'completed'} and not postoperative_status:
            self.add_error('postoperative_status', 'Cần chọn tình trạng hậu phẫu.')
        if status != 'discharged':
            cleaned_data['discharge_condition'] = ''
            cleaned_data['discharge_date'] = None
        if surgery_status not in {'post_op', 'completed'}:
            cleaned_data['postoperative_status'] = ''
        return cleaned_data


# ── ExaminationRecordForm – lịch sử khám ─────────────────────────────────────
class ExaminationRecordForm(forms.ModelForm):
    class Meta:
        model = ExaminationRecord
        fields = [
            'exam_date',
            'blood_pressure_systolic', 'blood_pressure_diastolic',
            'heart_rate', 'respiratory_rate', 'temperature', 'spo2',
            'weight', 'height',
            'chief_complaint', 'clinical_findings', 'diagnosis',
            'treatment_plan', 'prescription', 'follow_up_date', 'notes',
        ]
        widgets = {
            'exam_date': _datetime(),
            'blood_pressure_systolic': _num({'min': 60, 'max': 250}),
            'blood_pressure_diastolic': _num({'min': 40, 'max': 150}),
            'heart_rate': _num({'min': 30, 'max': 300}),
            'respiratory_rate': _num({'min': 6, 'max': 60}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 35, 'max': 42}),
            'spo2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 50, 'max': 100}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'chief_complaint': _txt(3),
            'clinical_findings': _txt(4),
            'diagnosis': _txt(3),
            'treatment_plan': _txt(3),
            'prescription': _txt(4),
            'follow_up_date': _date(),
            'notes': _txt(2),
        }
        labels = {
            'exam_date': 'Ngày giờ khám',
            'blood_pressure_systolic': 'Huyết áp tâm thu (mmHg)',
            'blood_pressure_diastolic': 'Huyết áp tâm trương (mmHg)',
            'heart_rate': 'Nhịp tim (bpm)',
            'respiratory_rate': 'Nhịp thở (lần/phút)',
            'temperature': 'Nhiệt độ (°C)',
            'spo2': 'SpO₂ (%)',
            'weight': 'Cân nặng (kg)',
            'height': 'Chiều cao (cm)',
            'chief_complaint': 'Lý do khám / Triệu chứng',
            'clinical_findings': 'Kết quả thăm khám lâm sàng',
            'diagnosis': 'Chẩn đoán',
            'treatment_plan': 'Hướng điều trị / Kế hoạch',
            'prescription': 'Đơn thuốc',
            'follow_up_date': 'Ngày tái khám',
            'notes': 'Ghi chú thêm',
        }


class PrescriptionRecordForm(forms.ModelForm):
    class Meta:
        model = PrescriptionRecord
        fields = [
            'issued_at', 'follow_up_date',
            'diagnosis', 'clinical_notes',
            'blood_pressure_systolic', 'blood_pressure_diastolic',
            'heart_rate', 'respiratory_rate', 'temperature', 'spo2', 'weight',
            'pain_score', 'blood_glucose',
            'medications', 'dosage_instructions', 'advice', 'notes',
        ]
        widgets = {
            'issued_at': _datetime(),
            'follow_up_date': _date(),
            'diagnosis': _txt(3),
            'clinical_notes': _txt(4),
            'blood_pressure_systolic': _num({'min': 60, 'max': 250}),
            'blood_pressure_diastolic': _num({'min': 40, 'max': 150}),
            'heart_rate': _num({'min': 30, 'max': 300}),
            'respiratory_rate': _num({'min': 6, 'max': 60}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 35, 'max': 42}),
            'spo2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 50, 'max': 100}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'pain_score': _num({'min': 0, 'max': 10}),
            'blood_glucose': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 0}),
            'medications': _txt(6),
            'dosage_instructions': _txt(4),
            'advice': _txt(3),
            'notes': _txt(2),
        }
        labels = {
            'issued_at': 'Ngày giờ cấp thuốc',
            'follow_up_date': 'Ngày tái khám',
            'diagnosis': 'Chẩn đoán',
            'clinical_notes': 'Tóm tắt lâm sàng / chỉ định',
            'blood_pressure_systolic': 'Huyết áp tâm thu (mmHg)',
            'blood_pressure_diastolic': 'Huyết áp tâm trương (mmHg)',
            'heart_rate': 'Nhịp tim (bpm)',
            'respiratory_rate': 'Nhịp thở (lần/phút)',
            'temperature': 'Nhiệt độ (°C)',
            'spo2': 'SpO₂ (%)',
            'weight': 'Cân nặng (kg)',
            'pain_score': 'Mức độ đau (0–10)',
            'blood_glucose': 'Đường huyết mao mạch (mmol/L)',
            'medications': 'Thuốc kê / toa thuốc',
            'dosage_instructions': 'Cách dùng thuốc',
            'advice': 'Dặn dò cho bệnh nhân',
            'notes': 'Ghi chú nội bộ',
        }


# ── RehabilitationAssessmentForm – đánh giá phục hồi chức năng ───────────────
class RehabilitationAssessmentForm(forms.ModelForm):
    class Meta:
        model = RehabilitationAssessment
        fields = [
            'assessed_at', 'assessment_type',
            # ADL
            'barthel_index', 'fim_score', 'mrs_score',
            # Vận động & cơ
            'fugl_meyer_upper', 'fugl_meyer_lower',
            'rivermead_motor_index', 'mas_score',
            'motricity_index_upper', 'motricity_index_lower', 'rom_notes',
            # Thăng bằng & dáng đi
            'berg_balance_scale', 'dynamic_gait_index', 'six_minute_walk',
            # Đau & nhận thức
            'pain_rating', 'dash_score', 'nihss_score',
            # Dấu hiệu sinh tồn nền
            'bp_systolic', 'bp_diastolic', 'heart_rate', 'respiratory_rate',
            'notes',
        ]
        widgets = {
            'assessed_at': _datetime(),
            'assessment_type': _sel(),
            'barthel_index': _num({'min': 0, 'max': 100}),
            'fim_score': _num({'min': 18, 'max': 126}),
            'mrs_score': _sel(),
            'fugl_meyer_upper': _num({'min': 0, 'max': 66}),
            'fugl_meyer_lower': _num({'min': 0, 'max': 34}),
            'rivermead_motor_index': _num({'min': 0, 'max': 15}),
            'mas_score': _num({'min': 0, 'max': 48}),
            'motricity_index_upper': _num({'min': 0, 'max': 100}),
            'motricity_index_lower': _num({'min': 0, 'max': 100}),
            'rom_notes': _txt(3),
            'berg_balance_scale': _num({'min': 0, 'max': 56}),
            'dynamic_gait_index': _num({'min': 0, 'max': 24}),
            'six_minute_walk': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 0}),
            'pain_rating': _num({'min': 0, 'max': 10}),
            'dash_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 0, 'max': 100}),
            'nihss_score': _num({'min': 0, 'max': 42}),
            'bp_systolic': _num({'min': 60, 'max': 250}),
            'bp_diastolic': _num({'min': 40, 'max': 150}),
            'heart_rate': _num({'min': 30, 'max': 300}),
            'respiratory_rate': _num({'min': 6, 'max': 60}),
            'notes': _txt(3),
        }
