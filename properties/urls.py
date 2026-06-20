from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('property/<slug:slug>/',views.property_detail,name='property_detail'),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("properties/", views.property_manage, name="property_manage"),
    path("properties/add/", views.property_add, name="property_add"),
    path("properties/<int:pk>/edit/", views.property_edit, name="property_edit"),
    path('gallery-image/<int:pk>/delete/',views.image_delete,name='image_delete'),
    path("properties/<int:pk>/delete/", views.property_delete, name="property_delete"),


    path("enquiries/", views.enquiry_list, name="enquiry_list"),
    path("enquiries/<int:pk>/view", views.enquiry_detail, name="enquiry_detail"),
    path('enquiries/<int:pk>/delete/', views.enquiry_delete, name='enquiry_delete'),
    path('submit-enquiry/',views.submit_enquiry,name='submit_enquiry'),

    path("video-enquiries/", views.videoviewing_list, name="videoviewing_list"),
    path('video-enquiries/<int:pk>/delete/', views.video_enquiry_delete, name='video_enquiry_delete'),
    path('submit-video-viewing/',views.submit_video_viewing,name='submit_video_viewing'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]