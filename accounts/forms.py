from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Tên đăng nhập',
            'autofocus': True,
        }),
        label='Tên đăng nhập',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Mật khẩu',
        }),
        label='Mật khẩu',
    )


class BaseUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Mật khẩu',
        min_length=6,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Xác nhận mật khẩu',
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'username': 'Tên đăng nhập',
            'first_name': 'Tên',
            'last_name': 'Họ',
            'email': 'Email',
            'phone_number': 'Số điện thoại',
            'date_of_birth': 'Ngày sinh',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Mật khẩu xác nhận không khớp.')
        return cleaned_data


class CreatePatientForm(BaseUserForm):
    GENDER_CHOICES = [('M', 'Nam'), ('F', 'Nữ')]
    TREATMENT_STATUS_CHOICES = [
        ('inpatient', 'Điều trị nội viện'),
        ('home', 'Điều trị tại nhà'),
        ('discharged', 'Đã xuất viện'),
    ]
    DISCHARGE_CONDITION_CHOICES = [
        ('', 'Chưa áp dụng'),
        ('recovered', 'Khỏi / hồi phục tốt'),
        ('improved', 'Đỡ / cải thiện'),
        ('stable', 'Ổn định'),
        ('transferred', 'Chuyển viện'),
        ('ama', 'Xin về / trái chỉ định'),
        ('other', 'Khác'),
    ]
    SURGERY_STATUS_CHOICES = [
        ('none', 'Chưa có chỉ định phẫu thuật'),
        ('indicated', 'Có chỉ định phẫu thuật'),
        ('planned', 'Đã lên kế hoạch phẫu thuật'),
        ('pre_op', 'Đang chuẩn bị tiền phẫu'),
        ('post_op', 'Đang hậu phẫu'),
        ('completed', 'Đã phẫu thuật'),
        ('cancelled', 'Hoãn / hủy phẫu thuật'),
    ]
    POSTOPERATIVE_STATUS_CHOICES = [
        ('', 'Chưa áp dụng'),
        ('stable', 'Hậu phẫu ổn định'),
        ('monitoring', 'Đang theo dõi sát'),
        ('improving', 'Đang cải thiện'),
        ('complication', 'Có biến chứng'),
        ('critical', 'Nặng / cần can thiệp thêm'),
        ('recovered', 'Phục hồi tốt sau mổ'),
    ]
    BLOOD_TYPE_CHOICES = [
        ('', 'Chưa xác định'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Giới tính',
    )
    blood_type = forms.ChoiceField(
        choices=BLOOD_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Nhóm máu',
    )
    diagnosis = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Chẩn đoán ban đầu',
    )
    admission_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Ngày nhập viện',
    )
    treatment_status = forms.ChoiceField(
        choices=TREATMENT_STATUS_CHOICES,
        initial='inpatient',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Trạng thái điều trị',
    )
    discharge_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Ngày xuất viện',
    )
    discharge_condition = forms.ChoiceField(
        choices=DISCHARGE_CONDITION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Tình trạng xuất viện',
    )
    surgery_status = forms.ChoiceField(
        choices=SURGERY_STATUS_CHOICES,
        initial='none',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Trạng thái phẫu thuật',
    )
    surgery_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Tên phẫu thuật / thủ thuật',
    )
    surgery_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Ngày phẫu thuật',
    )
    postoperative_status = forms.ChoiceField(
        choices=POSTOPERATIVE_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Tình trạng hậu phẫu',
    )
    doctor = forms.ModelChoiceField(
        queryset=None,  # set in __init__
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Bác sĩ phụ trách',
        empty_label='-- Chưa phân công --',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from doctors.models import DoctorProfile
        self.fields['doctor'].queryset = DoctorProfile.objects.select_related('user').all()

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('treatment_status')
        discharge_date = cleaned_data.get('discharge_date')
        discharge_condition = cleaned_data.get('discharge_condition')
        if status == 'discharged' and not discharge_condition:
            self.add_error('discharge_condition', 'Cần chọn tình trạng xuất viện khi bệnh nhân đã xuất viện.')
        if status == 'discharged' and not discharge_date:
            self.add_error('discharge_date', 'Cần nhập ngày xuất viện khi bệnh nhân đã xuất viện.')
        surgery_status = cleaned_data.get('surgery_status')
        surgery_name = cleaned_data.get('surgery_name')
        surgery_date = cleaned_data.get('surgery_date')
        postoperative_status = cleaned_data.get('postoperative_status')
        if surgery_status in {'indicated', 'planned', 'pre_op', 'post_op', 'completed'} and not surgery_name:
            self.add_error('surgery_name', 'Cần nhập tên phẫu thuật / thủ thuật khi đã có trạng thái phẫu thuật.')
        if surgery_status in {'post_op', 'completed'} and not surgery_date:
            self.add_error('surgery_date', 'Cần nhập ngày phẫu thuật cho trạng thái hậu phẫu hoặc đã mổ.')
        if surgery_status in {'post_op', 'completed'} and not postoperative_status:
            self.add_error('postoperative_status', 'Cần chọn tình trạng hậu phẫu.')
        if surgery_status not in {'post_op', 'completed'}:
            cleaned_data['postoperative_status'] = ''
        return cleaned_data


class CreateDoctorForm(BaseUserForm):
    DEPARTMENT_CHOICES = [
        ('cardiology', 'Tim mạch'),
        ('rehabilitation', 'Phục hồi chức năng'),
        ('orthopedics', 'Chỉnh hình - Chấn thương'),
        ('neurology', 'Thần kinh'),
        ('internal', 'Nội tổng quát'),
        ('surgery', 'Ngoại tổng quát'),
        ('other', 'Khác'),
    ]

    specialization = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Chuyên khoa',
    )
    license_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Số chứng chỉ hành nghề',
    )
    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Khoa',
    )


class CreateNurseForm(BaseUserForm):
    pass


class CreateAdminForm(BaseUserForm):
    pass
