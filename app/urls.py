from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm,ChangePasswordForm,PasswordReset, SetPassword

urlpatterns = [
    # path('', views.home),
    path("",views.ProductView.as_view(), name = "home"),
    path('product-detail/<int:id>', views.ProductDetails.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/',views.plus_cart,name='pluscart'),
    path('minuscart/',views.minus_cart,name='minuscart'),
    path('removecart/',views.remove_cart,name='removecart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.paymentdone, name='payment'),

    # path("match/",views.match_item,name="match"),

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topdata'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomdata'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name = "app/login.html", authentication_form = LoginForm), name='login'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    
    path("passchange/",auth_views.PasswordChangeView.as_view(template_name = "app/passwordchange.html",form_class = ChangePasswordForm,success_url = "/passchangedone/"),name = "changepass"),
    path("passchangedone/",auth_views.PasswordChangeView.as_view(template_name = "app/passwordchangedone.html"),name = "passchangedone"),
    
    path("password-reset/",auth_views.PasswordResetView.as_view(template_name= "app/password_reset.html",form_class = PasswordReset),
    name = "passwordreset"),

    path("password-reset/done/",auth_views.PasswordResetDoneView.as_view(template_name= "app/password_reset_done.html"),
    name = "password_reset_done"),   

    path('reset/confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="app/pass_reset_confirm.html", 
    form_class = SetPassword,), name="password_reset_confirm"),

    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/pass_reset_complete.html'),
    name = "password_reset_complete"),

    path('checkout/', views.checkout, name='checkout'),
    path("logout/",auth_views.LogoutView.as_view(), name='logout')
]



