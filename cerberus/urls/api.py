from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from django.conf import settings
from django.urls import include, path

from .. import api, reports

urlpatterns = [
    path("reports/", include(reports.urls)),
    path("api-auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api-auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api-auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework_auth")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", include(api.router.urls)),
    path("", include(api.urls)),
]

if settings.DEBUG:
    # Django
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
