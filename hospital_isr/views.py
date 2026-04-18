from django.conf import settings
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST


@require_POST
def set_language_view(request):
    language = request.POST.get("language", "vi")
    if language not in {"vi", "en"}:
        language = settings.LANGUAGE_CODE

    request.session["site_language"] = language
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        next_url = "/"

    response = redirect(next_url)
    response.set_cookie("site_language", language, max_age=60 * 60 * 24 * 365, samesite="Lax")
    return response
