from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import buy_now, razorpay_payment
from django.urls import path



urlpatterns = [
    path('', views.homelogin, name='homelogin'),
    path('register/',views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('homelogin/',views.homelogin, name='homelogin'),
    path('userloginhome/', views.userloginhome, name='userloginhome'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/users.html', views.users, name='users'),  # Define the URL pattern for users.html
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/login/',views.user_login,name='login'),
    path('admin_dashboard/customers.html', views.customers,name='customers'),
    path('admin_dashboard/dealers.html', views.dealers,name='dealers'),
    path('admin_dashboard/dealers.html', views.dealers,name='dealers'),
    path('admin_dashboard/deliveryman.html', views.deliveryman,name='deliveryman'),
    #path('toggle-activation/<int:customers_id>/', views.toggle_activation, name='toggle_activation'),
   # path('toggle-activation/<int:dealers_id>/', views.toggle_activation, name='toggle_activation'),
   # path('toggle-activation/<int:deliveryman_id>/', views.toggle_activation, name='toggle_activation'),
     #path('addpets/', views.add_pets, name='add_pets'),
    #  path('edit_profile/', views.edit_profile, name='edit_profile'),
     path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('userdealer/', views.userdealer, name='userdealer'),
    path('viewid/',views.viewid,name='viewid'),
     path('viewimage/',views.viewimage,name='viewimage'),

    path('addpets/', views.addpets, name='addpets'),
    path('activate_user/<int:user_id>/', views.activate_customer, name='activate_customer'),
    path('deactivate_user/<int:user_id>/', views.deactivate_customer, name='deactivate_customer'),

    path('profile/', views.profile, name='profile'),
    path('viewdatabase/<int:dealer_id>/', views.viewdatabase, name='viewdatabase'),


     path('aquariums/delete/<int:aquarium_id>/', views.delete_aquarium, name='delete_aquarium'),
    path('pets/delete/<int:pet_id>/', views.delete_pet, name='delete_pet'),
    path('edit_viewdatabase/<int:pk>/', views.edit_viewdatabase, name='edit_viewdatabase'),



     path('adminviewitem/', views.adminviewitem, name='adminviewitem'),


      path('admin/approve-pet/<int:pet_id>/', views.admin_approve_pet, name='admin_approve_pet'),
    path('admin/reject-pet/<int:pet_id>/', views.admin_reject_pet, name='admin_reject_pet'),
    path('admin/approve-aquarium/<int:aquarium_id>/', views.admin_approve_aquarium, name='admin_approve_aquarium'),
    path('admin/reject-aquarium/<int:aquarium_id>/', views.admin_reject_aquarium, name='admin_reject_aquarium'),
    path('delete/<str:item_type>/<int:item_id>/', views.delete_item, name='delete_item'),


path('usercustomer/', views.usercustomer, name='usercustomer'),

# path('cart/',views.cart, name='cart'),
 path('purchase/', views.purchase_item, name='purchase_item'), 
 
 path('customer_account/', views.customer_account, name='customer_account'),
 path('dealer_account/', views.dealer_account, name='dealer_account'),
 path('deliveryman/account/', views.deliveryman_account, name='deliveryman_account'),
 path('enable_aquarium/<int:aquarium_id>/', views.enable_aquarium, name='enable_aquarium'),
    path('disable_aquarium/<int:aquarium_id>/',views. disable_aquarium, name='disable_aquarium'),
    path('enable_pet/<int:pet_id>/', views.enable_pet, name='enable_pet'),
    path('disable_pet/<int:pet_id>/', views.disable_pet, name='disable_pet'),
    path('add_to_cart/<str:category>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('mycart/',views.mycart,name="mycart"),
    # path('add_to_cart/<str:category>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
     path('deliveryman_account/', views.deliveryman_account, name='deliveryman_account'),
     path('pet_details/<int:pet_id>/', views.pet_details, name='pet_details'),
     
     path('aquarium_details/<int:aquarium_id>/', views.aquarium_details, name='aquarium_details'),
     path('buy_now/<str:category>/<int:item_id>/', views.buy_now, name='buy_now'),
   
    path('razorpay-payment/', razorpay_payment, name='razorpay_payment'),
     path('payment_successful/', views.payment_successful, name='payment_successful'),
   

        path('add_payment_details/', views.add_payment_details, name='add_payment_details'),
         
         path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    
    path('paymenthandler1/', views.paymenthandler1, name='paymenthandler1'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_unsuccess/', views.payment_unsuccess, name='payment_unsuccess'),
    path('order/', views.order, name='order'),
    # path('submit_review/', views.submit_review, name='submit_review'),
    path('submit_review/<int:pet_id>/', views.submit_review, name='submit_review'),
    path('order_management/', views.order_management, name='order_management'),
    
    path('Dealer_feedback/', views.Dealer_feedback, name='Dealer_feedback'),
    
    # path('product-details/', views.product_details_view, name='product_details'),
    
    path('dealer_sales/', views.dealer_sales, name='dealer_sales'),
    path('dealer/dashboard/', views.dealer_dashboard, name='dealer_dashboard'),
    path('payment-details/', views.payment_details_view, name='payment_details'),
    #  path('submit_review_aqu/<int:aquarium_id>/', views.submit_review_aqu, name='submit_review_aqu')
    path('submit_review_aqu/<int:aquarium_id>/', views.submit_review_aqu, name='submit_review_aqu'),
     path('add_to_cart/<str:category>/<int:item_id>/',views. add_to_cart, name='add_to_cart'),


    # path('add_delivery_man/', views.add_delivery_man, name='add_delivery_man'),
     path('add_delivery_man/', views.add_delivery_man, name='add_delivery_man'),
    # path('import_delivery_men/', views.import_delivery_men, name='import_delivery_men'),
    path('Delivery_successfully_registerd/', views.Delivery_successfully_registerd, name='Delivery_successfully_registerd'),
    path('deliveryman_list/', views.deliveryman_list, name='deliveryman_list'),
    path('change_password/', views.change_password, name='change_password'),
    path('Delivery_unsuccessfully_registerd/', views.Delivery_unsuccessfully_registerd, name='Delivery_unsuccessfully_registerd'),



 

]


    #path('usercustomer/', views.usercustomer, name='usercustomer'),


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
   #path('user_accounts/', views.user_accounts,name='user_accounts'),
    #path('forgotpassword/',views.forgotpassword, name='forgotpassword'),
    
    #path('homelogin/', views.home,name='homelogin'),

    