from django.contrib.auth import views as auth_views
from django.urls import path
import custom_user.views


urlpatterns = [
    #Custom user urls
    path('accounts/login/', custom_user.views.login),
    path('accounts/logout/', custom_user.views.logout),
    path('accounts/logged_in/', custom_user.views.logged_in),
    path('accounts/invalid/', custom_user.views.invalid_login),
    path('accounts/auth/', custom_user.views.auth_view),
    path('accounts/change_password/', custom_user.views.change_password_post),
    path('accounts/update_settings/', custom_user.views.update_user_setting_post),
    path('accounts/delete/', custom_user.views.delete_account_post),
    path('settings/', custom_user.views.settings_view),

    path('accounts/password_reset/', auth_views.password_reset, {'template_name': 'custom_user/password_reset.html'}, name='password_reset'),
    path('accounts/password_reset/done/', auth_views.password_reset_done, {'template_name': 'custom_user/password_reset_done.html'}, name='password_reset_done'),
    path('accounts/reset/<str:uidb64>/<str:token>/', auth_views.password_reset_confirm, {'template_name': 'custom_user/password_reset_confirm.html'}, name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.password_reset_complete, {'template_name': 'custom_user/password_reset_complete.html'}, name='password_reset_complete'),
]
