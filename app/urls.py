from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('links/', views.link_list_view, name='link_list'),
    path('links/create/<int:pk>', views.link_create_view, name='link_create'),
    path('link/<int:pk>', views.link_detail_view, name='link_detail'),
    path('campaigns/create', views.campaign_create, name='campaign_create'),
    path('campaigns/submit', views.campaign_submit, name='campaign_submit'),
    path('campaigns', views.campaign_list_view, name='campaign_list'),
    path('campaign/<int:pk>', views.campaign_detail_view, name='campaign_detail'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<str:url_code>', views.link_view, name='link_view'),
]
