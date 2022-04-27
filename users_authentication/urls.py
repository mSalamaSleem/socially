from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('account_settings/', ProfileSettingUpdateView.as_view(), name='account_settings'),
    path('password_reset', password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="auth/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password/password_reset_complete.html'), name='password_reset_complete'),
]
