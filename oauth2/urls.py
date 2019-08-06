from django.urls import path

from oauth2 import basic_views
from oauth2.views import registration_views, login_views, token_grant_views, data_grant_views, auth_grant_views

urlpatterns = [
    path('index_page', basic_views.index, name='index'),
    path('registration_page', registration_views.register_page, name='registration_page'),
    path('client_secret_assignment', registration_views.client_secret_assignment, name='client_secret_assignment'),
    path('registration', registration_views.register, name='registration'),
    path('registration_done', registration_views.register_done, name='registration_done'),

    path('logout', login_views.logout, name='logout'),
    path('login_page', login_views.login_page, name='login_page'),
    path('login', login_views.login, name='login'),
    path('fcm_login', login_views.fcm_login_response, name='fcm_login'),

    path('authorize', auth_grant_views.authorize, name='authorize'),
    path('fcm_authorize', auth_grant_views.fcm_authorize, name='fcm_authorize'),
    path('token', token_grant_views.access_token, name='token'),
    path('notification', basic_views.notification_response, name='notification_response'),

    path('data', data_grant_views.get_data, name='get_data'),
    path('fcm_data', data_grant_views.fcm_get_data, name='fcm_data')
]