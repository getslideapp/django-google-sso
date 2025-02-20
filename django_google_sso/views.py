from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from django_google_sso import conf
from django_google_sso.main import GoogleAuth, UserHelper


@require_http_methods(["GET"])
def start_login(request: HttpRequest) -> HttpResponseRedirect:
    # Get next url
    next_param = request.GET.get("next")
    clean_param = (
        next_param
        if next_param.startswith("http") or next_param.startswith("/")
        else f"//{next_param}"
    )
    next_path = urlparse(clean_param).path

    # Get Google Auth URL
    google = GoogleAuth(request)
    auth_url, state = google.flow.authorization_url(prompt="consent")

    # Save data on Session
    if not request.session.session_key:
        request.session.create()
    request.session.set_expiry(conf.GOOGLE_SSO_TIMEOUT * 60)
    request.session["sso_state"] = state
    request.session["sso_next_url"] = next_path
    request.session.save()

    # Redirect User
    return HttpResponseRedirect(auth_url)


@require_http_methods(["GET"])
def callback(request: HttpRequest) -> HttpResponseRedirect:
    admin_url = reverse("admin:index")
    google = GoogleAuth(request)
    code = request.GET.get("code")
    state = request.GET.get("state")

    # Check if Google SSO is enabled
    if not conf.GOOGLE_SSO_ENABLED:
        messages.add_message(request, messages.ERROR, _("Google SSO not enabled."))
        return HttpResponseRedirect(admin_url)

    # First, check for authorization code
    if not code:
        messages.add_message(
            request, messages.ERROR, _("Authorization Code not received from SSO.")
        )
        return HttpResponseRedirect(admin_url)

    # Then, check state.
    request_state = request.session.get("sso_state")
    next_url = request.session.get("sso_next_url")

    if not request_state or state != request_state:
        messages.add_message(
            request, messages.ERROR, _("State Mismatch. Time expired?")
        )
        return HttpResponseRedirect(admin_url)

    # Get Access Token from Google
    try:
        google.flow.fetch_token(code=code)
    except Exception as error:
        messages.add_message(request, messages.ERROR, str(error))
        return HttpResponseRedirect(admin_url)

    # Get User Info from Google
    user_helper = UserHelper(google.get_user_info(), request)

    # Check if User Info is valid to login
    if not user_helper.email_is_valid:
        messages.add_message(
            request,
            messages.ERROR,
            _(
                f"Email address not allowed: {user_helper.user_email}. "
                f"Please contact your administrator."
            ),
        )
        return HttpResponseRedirect(admin_url)

    # Get or Create User
    if conf.GOOGLE_SSO_AUTO_CREATE_USERS:
        user = user_helper.get_or_create_user()
    else:
        user = user_helper.find_user()

    if not user or not user.is_active:
        return HttpResponseRedirect(admin_url)

    # Login User
    login(request, user, conf.GOOGLE_SSO_AUTHENTICATION_BACKEND)
    request.session.set_expiry(conf.GOOGLE_SSO_SESSION_COOKIE_AGE)

    return HttpResponseRedirect(next_url or admin_url)
