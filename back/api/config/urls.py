"""patios_cordoba URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .settings import STATIC_ROOT, STATIC_URL
from django.conf.urls.static import static
admin.site.site_header = 'Masaveu'
admin.site.site_title = 'Masaveu'
admin.site.index_title = 'Masaveu'

schema_view = get_schema_view(
    openapi.Info(
        title="Masaveu API",
        default_version='v1',
        description="Masaveu API",
        contact=openapi.Contact(email="vladgoia2811@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/admin/', admin.site.urls),
    re_path(r'^api/v1/swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0)),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('api/v1/middleware/login/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/middleware/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/middleware/verify/',
         TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/password_reset/', include('django_rest_passwordreset.urls',
                                           namespace='password_reset')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/utils/', include('utils.urls')),
    path('api/v1/captures/', include('captures.urls')),
    path('api/v1/equipments/', include('equipments.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/settings/', include('settings.urls')),

] + static(STATIC_URL, document_root=STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
