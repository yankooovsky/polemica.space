from django.contrib import admin

from authn.models.openid import OAuth2App, OAuth2Token, OAuth2AuthorizationCode
from authn.models.session import Session, Code


class OAuth2AppAdmin(admin.ModelAdmin):
    list_display = (
        "client_id",
        "name",
        "website",
        "owner",
        "created_at",
    )
    ordering = ("-created_at",)


admin.site.register(OAuth2App, OAuth2AppAdmin)


class OAuth2TokenAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "client_id",
        "token_type",
        "scope",
        "issued_at",
        "expires_in",
    )
    ordering = ("-issued_at",)


admin.site.register(OAuth2Token, OAuth2TokenAdmin)


class OAuth2AuthorizationCodeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "client_id",
        "code",
        "scope",
        "auth_time",
        "nonce",
    )
    ordering = ("-auth_time",)


admin.site.register(OAuth2AuthorizationCode, OAuth2AuthorizationCodeAdmin)


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "recipient",
        "code",
        "user",
        "created_at",
        "expires_at",
    )
    ordering = ("-created_at",)
