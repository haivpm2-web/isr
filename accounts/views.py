from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db import transaction
from functools import wraps
from .models import CustomUser
from .forms import LoginForm, CreatePatientForm, CreateDoctorForm, CreateNurseForm, CreateAdminForm


# ── Decorators ────────────────────────────────────────────────────────────────

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_admin_user():
            messages.error(request, 'Bạn không có quyền truy cập trang này.')
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


# ── Auth views ────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Chào mừng, {user.get_full_name() or user.username}!')
            return _redirect_by_role(user)
        messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    else:
        form = LoginForm(request)

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Bạn đã đăng xuất.')
    return redirect('accounts:login')


def _redirect_by_role(user):
    if user.is_admin_user():
        return redirect('accounts:admin_dashboard')
    elif user.is_doctor():
        return redirect('doctors:dashboard')
    elif user.is_nurse_user():
        return redirect('doctors:dashboard')
    return redirect('patients:dashboard')


# ── Admin views ────────────────────────────────────────────────────────────────

@admin_required
def admin_dashboard(request):
    users = CustomUser.objects.all().order_by('role', 'username')
    context = {
        'users': users,
        'total_patients': users.filter(role='patient').count(),
        'total_doctors': users.filter(role='doctor').count(),
        'total_nurses': users.filter(role='nurse').count(),
        'total_admins': users.filter(role='admin').count(),
        'total_active': users.filter(is_active=True).count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@admin_required
def create_account(request):
    role = request.GET.get('role', 'patient')
    if role not in ('patient', 'doctor', 'nurse', 'admin'):
        role = 'patient'

    FormClass = {
        'patient': CreatePatientForm,
        'doctor': CreateDoctorForm,
        'nurse': CreateNurseForm,
        'admin': CreateAdminForm,
    }[role]

    form = FormClass(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        try:
            with transaction.atomic():
                user = form.save(commit=False)
                user.role = role
                user.set_password(form.cleaned_data['password'])
                user.save()

                if role == 'patient':
                    from patients.models import PatientProfile
                    PatientProfile.objects.create(
                        user=user,
                        gender=form.cleaned_data.get('gender', 'M'),
                        blood_type=form.cleaned_data.get('blood_type', ''),
                        diagnosis=form.cleaned_data.get('diagnosis', ''),
                        treatment_status=form.cleaned_data.get('treatment_status', 'inpatient'),
                        admission_date=form.cleaned_data.get('admission_date'),
                        discharge_date=form.cleaned_data.get('discharge_date'),
                        discharge_condition=form.cleaned_data.get('discharge_condition', ''),
                        surgery_status=form.cleaned_data.get('surgery_status', 'none'),
                        surgery_name=form.cleaned_data.get('surgery_name', ''),
                        surgery_date=form.cleaned_data.get('surgery_date'),
                        postoperative_status=form.cleaned_data.get('postoperative_status', ''),
                        doctor=form.cleaned_data.get('doctor'),
                    )
                elif role == 'doctor':
                    from doctors.models import DoctorProfile
                    DoctorProfile.objects.create(
                        user=user,
                        specialization=form.cleaned_data.get('specialization', ''),
                        license_number=form.cleaned_data.get('license_number', ''),
                        department=form.cleaned_data.get('department', 'rehabilitation'),
                    )

                messages.success(request, f'Tạo tài khoản "{user.get_full_name() or user.username}" thành công!')
                return redirect('accounts:admin_dashboard')
        except Exception as exc:
            messages.error(request, f'Lỗi tạo tài khoản: {exc}')

    role_label = {'patient': 'Bệnh nhân', 'doctor': 'Bác sĩ', 'nurse': 'Điều dưỡng / Y tá', 'admin': 'Quản trị viên'}
    return render(request, 'accounts/create_account.html', {
        'form': form,
        'role': role,
        'role_label': role_label[role],
    })


@admin_required
def delete_account(request, user_id):
    target = get_object_or_404(CustomUser, pk=user_id)
    if target == request.user:
        messages.error(request, 'Không thể xóa tài khoản của chính mình.')
        return redirect('accounts:admin_dashboard')

    if request.method == 'POST':
        name = target.get_full_name() or target.username
        target.delete()
        messages.success(request, f'Đã xóa tài khoản: {name}')
        return redirect('accounts:admin_dashboard')

    return render(request, 'accounts/confirm_delete.html', {'target_user': target})


@admin_required
def toggle_active(request, user_id):
    if request.method == 'POST':
        target = get_object_or_404(CustomUser, pk=user_id)
        if target == request.user:
            messages.error(request, 'Không thể tự thay đổi trạng thái tài khoản của mình.')
        else:
            target.is_active = not target.is_active
            target.save()
            status = 'kích hoạt' if target.is_active else 'vô hiệu hóa'
            messages.success(request, f'Đã {status} tài khoản {target.get_full_name() or target.username}.')
    return redirect('accounts:admin_dashboard')
