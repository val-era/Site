from django.urls import path
from . import views
from user import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('register/', user_views.register, name='register'),
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('feedbackfrombyers', views.feedback, name='feedback'),
    path('contacts', views.contacts, name='contacts'),
    path(r'messenger/<parameter>', views.messenger, name='messenger'),
    path(r'del/<parameter>', views.remove_items, name='del'),
    path(r'save/<parameter>', views.remove_items, name='save'),
    path(r'updateargs/<parameter>', views.update_args, name='updateargs'),
    path(r'fullpage/<parameter>', views.messenger_full, name='fullpage'),
    path(r'load_image/<parameter>', views.load_image, name='load_image'),
    path(r'delmsg/<parameter>', views.del_msg, name='delmsg'),
    path('groupe', views.groupe, name='groupe')
]