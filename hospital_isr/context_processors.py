def language_settings(request):
    site_language = request.session.get("site_language") or request.COOKIES.get("site_language") or "vi"
    if site_language not in {"vi", "en"}:
        site_language = "vi"

    return {
        "site_language": site_language,
        "language_choices": (
            ("vi", "VI"),
            ("en", "EN"),
        ),
    }
