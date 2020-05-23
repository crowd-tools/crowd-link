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

sale_campaign_list = api_views.SaleCampaignViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

sale_campaign_detail = api_views.SaleCampaignViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})

sale_campaign_detail_create_link = api_views.SaleLinkViewSet.as_view({
    'post': 'create_link'
})

sale_link_detail = api_views.SaleLinkViewSet.as_view({
    'get': 'retrieve'
})

click_campaign_list = api_views.ClickCampaignViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

click_campaign_detail = api_views.ClickCampaignViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})

click_campaign_detail_create_link = api_views.ClickLinkViewSet.as_view({
    'post': 'create_link'
})

click_link_detail = api_views.ClickLinkViewSet.as_view({
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

    path('sale/campaigns/', sale_campaign_list, name='salecampaign-list'),
    path('sale/campaigns/<int:pk>/', sale_campaign_detail, name='salecampaign-detail'),
    path('sale/campaigns/<int:pk>/create_link/', sale_campaign_detail_create_link, name='salecampaign-detail-create-link'),
    path('sale/links/<int:pk>/', sale_link_detail, name='salelink-detail'),

    path('click/campaigns/', click_campaign_list, name='clickcampaign-list'),
    path('click/campaigns/<int:pk>/', click_campaign_detail, name='clickcampaign-detail'),
    path('click/campaigns/<int:pk>/create_link/', click_campaign_detail_create_link, name='clickcampaign-detail-create-link'),
    path('click/links/<int:pk>/', click_link_detail, name='clicklink-detail'),
])

urlpatterns += [
    path('auth/', include('social_django.urls', namespace='social')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
