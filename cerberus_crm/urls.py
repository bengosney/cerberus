# Django
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

# Locals
from .views import htmx_logout_then_login

urlpatterns = [
    path("", include("cerberus.urls.urls")),
    path("api/", include("cerberus.urls.api")),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", htmx_logout_then_login, name="logout"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
