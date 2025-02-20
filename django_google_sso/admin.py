from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from django_google_sso import conf
from django_google_sso.models import GoogleSSOUser

if conf.GOOGLE_SSO_ENABLED:
    admin.site.login_template = "admin_sso/login.html"

User = get_user_model()


class GoogleSSOInlineAdmin(admin.StackedInline):
    model = GoogleSSOUser
    readonly_fields = ("google_id",)


@admin.register(GoogleSSOUser)
class GoogleSSOAdmin(admin.ModelAdmin):
    list_display = ("user", "google_id")
    readonly_fields = ("google_id",)


class SSOUserAdmin(UserAdmin):
    model = User
    inlines = [GoogleSSOInlineAdmin]


if conf.GOOGLE_SSO_PROVIDE_USER_ADMIN_PAGE:
    if admin.site.is_registered(User):
        admin.site.unregister(User)
    admin.site.register(User, SSOUserAdmin)
