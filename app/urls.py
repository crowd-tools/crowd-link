from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('view/', views.index, name='index'),
    path('view/links/', views.link_list_view, name='link_list'),
    path('view/links/create/<int:pk>', views.link_create_view, name='link_create'),
    path('view/link/<int:pk>', views.link_detail_view, name='link_detail'),
    path('view/campaigns/create', views.campaign_create, name='campaign_create'),
    path('view/campaigns/submit', views.campaign_submit, name='campaign_submit'),
    path('view/campaigns', views.campaign_list_view, name='campaign_list'),
    path('view/campaign/<int:pk>', views.campaign_detail_view, name='campaign_detail'),
    path('view/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('l/<str:url_code>', views.link_view, name='link_view'),
]
