from django import template

register = template.Library()

TRANSLATIONS = {
    "en": {
        "Phục hồi chức năng": "Rehabilitation",
        "Tổng quan": "Dashboard",
        "Tạo tài khoản": "Create Accounts",
        "Bệnh nhân": "Patient",
        "Bác sĩ": "Doctor",
        "Điều dưỡng / Y tá": "Nurse",
        "Quản trị viên": "Administrator",
        "ECG": "ECG",
        "Kết quả ECG": "ECG Results",
        "Phục hồi chân": "Leg Recovery",
        "Đăng xuất": "Sign Out",
        "QUẢN TRỊ": "ADMINISTRATION",
        "BÁC SĨ": "DOCTOR",
        "ĐIỀU DƯỠNG": "NURSE",
        "BỆNH NHÂN": "PATIENT",
        "Thêm bệnh nhân": "Add Patient",
        "Thêm bác sĩ": "Add Doctor",
        "Thêm điều dưỡng": "Add Nurse",
        "Thêm admin": "Add Administrator",
        "Danh sách bệnh nhân": "Patient List",
        "Tính năng": "Features",
        "Theo dõi ECG": "ECG Monitoring",
        "Quản lý bệnh nhân": "Patient Management",
        "Biểu đồ tiến trình": "Progress Charts",
        "Liên hệ": "Contact",
        "Hệ thống": "System",
        "Bảo mật SSL": "SSL Security",
        "Dữ liệu được mã hóa": "Encrypted Data",
        "Hỗ trợ đa thiết bị": "Multi-device Support",
        "Đăng nhập": "Sign In",
        "Vui lòng đăng nhập để tiếp tục": "Please sign in to continue",
        "Tên đăng nhập": "Username",
        "Mật khẩu": "Password",
        "Hệ thống bảo mật – Chỉ dành cho nhân viên y tế được cấp quyền": "Secure system – Access for authorized healthcare staff only",
        "Tổng quan bác sĩ": "Doctor Dashboard",
        "Tổng quan điều dưỡng": "Nurse Dashboard",
        "Nhập dữ liệu bệnh nhân": "Patient Data Entry",
        "Bệnh nhân của tôi": "My Patients",
        "ECG Bất thường": "Abnormal ECGs",
        "ECG gần đây": "Recent ECGs",
        "Ghi nhận phục hồi": "Recovery Records",
        "Tất cả": "View All",
        "Chưa có bệnh nhân nào.": "No patients yet.",
        "Chưa có ECG nào.": "No ECG records yet.",
        "Chưa có dữ liệu phục hồi.": "No recovery data yet.",
        "Phục hồi gần đây": "Recent Recovery",
        "Tổng quan sức khỏe": "Health Overview",
        "Nhập viện": "Admission",
        "Nhịp tim (bpm)": "Heart Rate (bpm)",
        "Phục hồi": "Recovery",
        "Sức mạnh cơ (MRC)": "Muscle Strength (MRC)",
        "Mức độ đau (VAS)": "Pain Level (VAS)",
        "Xu hướng nhịp tim": "Heart Rate Trend",
        "Xem tất cả": "View All",
        "Tiến trình phục hồi": "Recovery Progress",
        "Chi tiết": "Details",
        "Chưa có dữ liệu ECG": "No ECG data yet",
        "ECG gần nhất": "Latest ECG",
        "Nhịp tim": "Heart Rate",
        "Khoảng PR": "PR Interval",
        "Thời gian QRS": "QRS Duration",
        "Khoảng QT": "QT Interval",
        "Nhịp:": "Rhythm:",
        "Cần chú ý": "Needs Attention",
        "Phục hồi gần nhất": "Latest Recovery",
        "Tỷ lệ phục hồi tổng thể": "Overall Recovery",
        "Sức cơ MRC": "MRC Strength",
        "Biên độ": "Range of Motion",
        "Đau VAS": "VAS Pain",
        "Khả năng đi lại:": "Walking Ability:",
        "Quản trị tài khoản": "Account Administration",
        "Đang hoạt động": "Active",
        "Tạo tài khoản:": "Create account:",
        "Danh sách tài khoản": "Account List",
        "Họ và tên": "Full Name",
        "Email": "Email",
        "Số điện thoại": "Phone Number",
        "Vai trò": "Role",
        "Trạng thái": "Status",
        "Ngày tạo": "Created",
        "Thao tác": "Actions",
        "Hoạt động": "Active",
        "Vô hiệu": "Disabled",
        "Vô hiệu hóa": "Disable",
        "Kích hoạt": "Activate",
        "Xóa": "Delete",
        "Không có tài khoản nào.": "No accounts found.",
        "Admin": "Administrator",
    }
}


def _get_language(context):
    request = context.get("request")
    if not request:
        return "vi"
    language = request.session.get("site_language") or request.COOKIES.get("site_language") or "vi"
    return language if language in {"vi", "en"} else "vi"


@register.simple_tag(takes_context=True)
def t(context, value):
    if value is None:
        return ""
    text = str(value)
    language = _get_language(context)
    if language == "vi":
        return text
    return TRANSLATIONS.get(language, {}).get(text, text)
