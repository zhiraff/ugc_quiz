import os

from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.views import serve
from django.views.static import serve as media_serve
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions
from django.conf import settings

# Возможность выбирать схему (http/https) в сваггере
class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
    # url='https://192.168.1.8:8080/',
   public=True,
   generator_class=BothHttpAndHttpsSchemaGenerator,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls', namespace='account')), #   работа с аккаунтами
    path("api/v1/quiz/", include("quiz.urls_api")),    #   API
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),  #   swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),    #   swagger
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), #   redoc
    path('', include('quiz.urls')),    # все остальные ссылки
]


# обработка статики и медиа
urlpatterns.append(path('static/<path:path>', serve, {'insecure': True}))

urlpatterns.append(path('media/<path:path>', media_serve, {'document_root': settings.MEDIA_ROOT}))

# страница сваггера и редок
# urlpatterns.append(path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),)
# urlpatterns.append(path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'))
# urlpatterns.append(path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'))

# немного кастомизации админки не помешает
admin.site.site_title = f"UGC"
admin.site.site_header = f"UGC"
admin.site.index_title = f"UGC | Версия ПО: {os.getenv('version', '0.0.1')}"