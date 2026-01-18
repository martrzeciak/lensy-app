from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path('profile/avatar/update/', views.update_avatar, name='update_avatar'),
    path('profile/avatar/remove/', views.remove_avatar, name='remove_avatar'),
    path('profile/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
    path('profile/<str:username>/<str:list_type>/', views.user_list_view, name='user_list'),
    path("profile/<str:username>/", views.profile_view, name="user_profile"),
    path('edit/', views.edit_profile_view, name='edit_profile'),

]