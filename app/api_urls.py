from django.urls import include, path
from rest_framework import routers

from . import api_views

router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'groups', api_views.GroupViewSet)
router.register(r'campaigns', api_views.CampaignViewSet)
router.register(r'links', api_views.LinkViewSet)


urlpatterns = [
    path('', include(router.urls), name='foo'),
    path('auth/', include('rest_framework.urls'))
]
