from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns

from . import api_views

user_list = api_views.UserViewSet.as_view({
    'get': 'list',
})

user_detail = api_views.UserViewSet.as_view({
    'get': 'retrieve',
})

campaign_list = api_views.CampaignViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

campaign_detail = api_views.CampaignViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})

campaign_detail_create_link = api_views.CampaignViewSet.as_view({
    'post': 'create_link'
})

link_detail = api_views.LinkViewSet.as_view({
    'get': 'retrieve'
})

# Swagger documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = format_suffix_patterns([
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('campaigns/', campaign_list, name='campaign-list'),
    path('campaigns/<int:pk>/', campaign_detail, name='campaign-detail'),
    path('campaigns/<int:pk>/create_link/', campaign_detail_create_link, name='campaign-detail-create-link'),
    path('links/<int:pk>/', link_detail, name='link-detail'),
])

urlpatterns += [
    path('auth/', include('social_django.urls', namespace='social')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
