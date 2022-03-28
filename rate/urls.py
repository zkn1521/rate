from django.urls import path

from rate import views

app_name = 'rate'
urlpatterns = [
    path('list/', views.List),
    path('view/', views.Views),
    path('avarage/<pro_id>/<module_code>/', views.Ave),
    path('rateone/<pro_id>/<module_code>/<year>/<semester>/<rate>/', views.rateone),
    path('users/register/', views.register),
    path('users/login/', views.login_user),
    path('users/logout/', views.logout_user),
]