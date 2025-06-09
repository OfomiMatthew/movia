from .views import EditProfile, PasswordChange, SignUp,logout_view,user_profile
from django.contrib.auth import views as authViews 
from django.urls import path 


urlpatterns = [
    path('edit-profile/',EditProfile,name='edit-profile'),
    path('profile/<username>/',user_profile,name='profile'),
    path('signup/',SignUp,name='signup'),
    path('login/',authViews.LoginView.as_view(template_name='registration/login.html'),name='login'),
    # path('logout/',authViews.LogoutView.as_view(),{'next_page':'login'},name='logout'),
    path('logout/',logout_view,name='logout'),
    path('change-password/',PasswordChange,name='change-password'),
    path('change-password-done',authViews.PasswordChangeDoneView.as_view(template_name='change_password_done.html'),name='change-password-done'),
    path('password-reset',authViews.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),name='password_reset'),
    path('password-reset-done/done',authViews.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('password-reset/<uidb64>/<token>,',authViews.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset/complete',authViews.PasswordResetCompleteView.as_view(),name='password-reset-complete'),
    
    
    
]
