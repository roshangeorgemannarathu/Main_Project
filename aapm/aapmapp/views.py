from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .models import dealer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q  # Import Q for complex queries
from django.http import JsonResponse
from django.http import Http404
from .models import UserProfile,CartItem
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse
from .urls import *
from django.views.decorators.csrf import csrf_exempt


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


import razorpay
#for activating user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.urls import NoReverseMatch,reverse
# Create your views here.

#email
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
from django.conf import settings
from django.core.mail import EmailMessage


from .models import Pet, Aquarium

#threading
import threading

#reset passwor generater
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# Create your views here.


def homelogin(request):
        return render(request, 'homelogin.html')



def register(request):
    if request.method == 'POST': 
        fullname = request.POST['fullname']
        username = request.POST['username']
        role = request.POST['role']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'register.html', {'error_message': 'Passwords do not match'})

        # Create a user instance but do not save it yet
        user = dealer(username=username, email=email,role=role ,fullname=fullname,)

        # Set the password for the user
        user.set_password(password)

        # Save the user to the database
        user.save()

        # Redirect to the home page or any desired page
        return redirect('login')

    return render(request, 'register.html')


# def toggle_activation(request, dealer_id):
#     dealer = get_object_or_404(dealer, id=dealer_id)  # Use 'Dealer' instead of 'Customer'

#     # Toggle the dealer's activation status
#     dealer.is_active = not dealer.is_active
#     dealer.save()

#     # Redirect back to the dealer list page
#     return redirect('dealers')  # Update 'dealers' with the correct URL name for your dealer list page

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            request.session['role'] = user.role
            if user.username == "admin":
                return redirect('admin_dashboard')
            else:
                return redirect('userloginhome')
        else:
            messages.error(request, 'Invalid credentials!!')
    return render(request, 'login.html')



def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('userloginhome')

@login_required(login_url='login')



@never_cache
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')





def users(request):
    # Query the database to get the data you want to display on the admin dashboard
    dealers = dealer.objects.all()  # You can adjust this queryset based on your requirements
    # You can fetch other data in a similar way
    dealers = dealer.objects.filter(is_superuser=False)

    # Pass the data to the template context
    context = {
        'dealers': dealers,
        # Add other data you want to pass to the template
    }
    
    return render(request, 'users.html', context)




@never_cache
def customers(request):
    customers = dealer.objects.all()  # You can adjust this queryset based on your requirements

    # Query the database to get the data you want to display on the admin dashboard
    customers = dealer.objects.filter(role='customer')  # Filter by role 'customer'

    # Pass the data to the template context
    context = {
        'customers': customers,  # Use a meaningful name like 'customers' for the filtered queryset
        # Add other data you want to pass to the template
    }
    return render(request, 'customers.html', context)  


def dealers(request):
    # Query the database to get the data you want to display on the admin dashboard
    dealers = dealer.objects.filter(role='dealer')  # Filter by role 'customer'

    # Pass the data to the template context
    context = {
        'dealers': dealers,  # Use a meaningful name like 'customers' for the filtered queryset
        # Add other data you want to pass to the template
    }
    return render(request, 'dealers.html', context) 


def deliveryman(request):
    # Query the database to get the data you want to display on the admin dashboard
    deliveryman = dealer.objects.filter(role='deliveryman')  # Filter by role 'deliveryman'

    # Pass the data to the template context
    context = {
        'deliveryman': deliveryman,  # Update the variable name to 'deliverymen'
        # Add other data you want to pass to the template
    }
    return render(request, 'deliveryman.html', context)
# def toggle_activation(request, customers_id):
#     customers= get_object_or_404(dealer, id=customers_id)  # Use 'dealer' instead of 'Dealer'

#     if request.method == 'POST':
#         action = request.POST.get('action')  # Get the value of the clicked button

#         if action == 'activate':
#             customers.is_active = True
#         elif action == 'deactivate':
#             customers.is_active = False

#         customers.save()

#         # Send a JSON response to update the button text on the page
#         response_data = {'message': 'Activation status toggled successfully.'}
#         return JsonResponse(response_data)

#     # Redirect back to the customers list page
#     return redirect('customers')

    
# def toggle_dealer_activation(request, dealer_id):
#     dealer = get_object_or_404(dealers, id=dealer_id)

#     if request.method == 'POST':
#         action = request.POST.get('action')  # Get the value of the clicked button

#         if action == 'activate':
#             dealer.is_active = True
#         elif action == 'deactivate':
#             dealer.is_active = False

#         dealer.save()

#         # Send a JSON response to update the button text on the page
#         response_data = {'message': 'Activation status toggled successfully.'}
#         return JsonResponse(response_data)

#     # Redirect back to the dealer list page
#     return redirect('dealers')

def toggle_deliveryman_activation(request, deliveryman_id):
    deliveryman= get_object_or_404(dealers, id=deliveryman_id)

    if request.method == 'POST':
        action = request.POST.get('action')  # Get the value of the clicked button

        if action == 'activate':
            deliveryman.is_active = True
        elif action == 'deactivate':
            deliveryman.is_active = False

        dealer.save()

        # Send a JSON response to update the button text on the page
        response_data = {'message': 'Activation status toggled successfully.'}
        return JsonResponse(response_data)

    # Redirect back to the dealer list page
    return redirect('deliveryman')
def a(request):
    if requdd_pet_or_aquariumest.method == 'POST':
        category = request.POST.get('category')
        image = request.FILES.get('image')

        if category == 'aquarium':
            form = AquariumForm(request.POST, request.FILES)
            if form.is_valid():
                aquarium = form.save(commit=False)
                aquarium.image = image
                aquarium.save()
                return redirect('success')  # Redirect to a success page
        elif category == 'pets':
            form = PetForm(request.POST, request.FILES)
            if form.is_valid():
                pet = form.save(commit=False)
                pet.image = image
                pet.save()
                return redirect('success')  # Redirect to a success page

    else:
        # Handle GET request (display the form)
        form = AquariumForm()  # You can choose which form to display initially

    return render(request, 'add_pet_or_aquarium.html', {'form': form})

def success(request):
    return render(request, 'success.html')  # Create a success template

def add_pets(request):
    # Your view logic for the addpets page
    return render(request, 'addpets.html')


@login_required
@never_cache
def userloginhome(request):
    if request.method == 'POST':
        # Extract form data
        full_name = request.POST.get('fullname')
        date_of_birth = request.POST.get('dateofbirth')
        gender = request.POST.get('gender')  # Assuming you have a gender field in your form
        phone = request.POST.get('phone')
        housename = request.POST.get('housename')
        pincode = request.POST.get('pincode')
        district = request.POST.get('district')
        photoid = request.FILES.get('photoid')
        photo = request.FILES.get('photo')

        # Get or create the user associated with this profile (assuming you have a logged-in user)
        # Replace "request.user" with the actual way you obtain the user object
        user = request.user

        # Create a UserProfile object and save it to the database
        user_profile = UserProfile(
            user=user,
            fullname=full_name,
            dateofbirth=date_of_birth,
            phone=phone,
            housename=housename,
            pincode=pincode,
            district=district,
            photoid=photoid,
            photo=photo
        )
        user_profile.save()

        # Redirect to a success page or do something else
        return JsonResponse({'message': 'Registration successful'})

    return render(request, 'userloginhome.html')


   

def edit_profile(request):
    if request.method == 'POST':
        # Assuming you have a UserProfile model
        user_profile = UserProfile.objects.get(user=request.user)

        user_profile.full_name = request.POST.get('fullname')
        user_profile.date_of_birth = request.POST.get('dateofbirth')
        user_profile.gender = request.POST.get('gender')
        user_profile.phone_number = request.POST.get('phoneno')
        user_profile.current_address = request.POST.get('currentaddress')

            # Handle the photo upload
        if 'photoid' in request.FILES:
                user_profile.photo_id = request.FILES['photoid']

        user_profile.save()
        
        # Redirect to a success page or the user profile page return redirect('user_profile')  # Replace with the actual URL name of the user profile page

    return render(request, 'edit_profile.html')  # Replace with the actual template name

# Add any additional view functions as needed

def deactivate_user(request, user_id):
    user = get_object_or_404(dealer, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
         # Send deactivation email
        subject = 'Account Deactivation'
        message = 'Your account has been deactivated by the admin.'
        from_email = 'roshangeorge2024b@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('deactivation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.username}' has been deactivated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is already deactivated.")
    return redirect('dealers')

def activate_user(request, user_id):
    user = get_object_or_404(dealer, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()

        # Send activation email
        subject = 'Account Activation'
        message = 'Your account has been activated by the admin.'
        from_email = 'roshangeorge2024b@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.username}' has been activated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is already active.")
    return redirect('dealers')


def userdealer(request):
        # Aquarium.objects.all().delete()
        return render(request, 'userdealer.html')

from django.http import Http404


@login_required
def profile(request):
    user_profiles = UserProfile.objects.filter(user=request.user)

    if user_profiles.exists():
        user_profile = user_profiles.first()

        context = {
            'fullname': user_profile.fullname,
            'dateofbirth': user_profile.dateofbirth,
            #'gender': user_profile.gender,
            'phone': user_profile.phone,
            'housename': user_profile.housename,
            'pincode': user_profile.pincode,
            'district': user_profile.district,
            'photoid': user_profile.photoid.url if user_profile.photoid else '',
            'photo': user_profile.photo.url if user_profile.photo else '',
        }

        return render(request, 'profile.html', context)
    else:
        raise Http404("UserProfile does not exist for this user")




def deactivate_customer(request, user_id):
    user = get_object_or_404(customers, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
         # Send deactivation email
        subject = 'Account Deactivation'
        message = 'Your account has been deactivated by the admin.'
        from_email = 'roshangeorge2024b@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('deactivation_email.html', {'customer': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.username}' has been deactivated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is already deactivated.")
    return redirect(request, 'admin_dashboard.html')

def activate_customer(request, user_id):
    user = get_object_or_404(customers, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()

        # Send activation email
        subject = 'Account Activation'
        message = 'Your account has been activated by the admin.'
        from_email = 'roshangeorge2024b@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_email.html', {'customer': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.username}' has been activated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is already active.")
    return redirect(request, 'admin_dashboard.html')

# @login_required
# def profile(request):
#     try:
#         # Attempt to retrieve the user's profile
#         user_profile = UserProfile.objects.get(user=request.user)
#     except UserProfile.DoesNotExist:
#         # Handle the case when the profile does not exist
#         raise Http404("UserProfile does not exist for this user")

#     # Access the user's current address, adjust this based on your model structure
#     current_address = user_profile.current_address

#     context = {
#         'fullname': user_profile.fullname,
#         'dateofbirth': user_profile.dateofbirth,
#         'gender': user_profile.gender,
#         'phone': user_profile.phone,
#         'housename': user_.housename,
#         'pincode': current_address.pincode,
#         'district': current_address.district,
#         'photoid': user_profile.photo_id,
#         'photo': user_profile.photo,
#     }

#     return render(request, 'profile.html', context)

def viewid(request):
    # Your view logic for the addpets page
    return render(request, 'viewid.html')

def viewimage(request):
    # Your view logic for the addpets page
    return render(request, 'view.html')

@login_required
def viewdatabase(request, dealer_id):
    user = request.user

    print(f"Dealer ID from URL: {dealer_id}")
    print(f"Current User ID: {user.id}")

    if dealer.objects.filter(id=request.user.id).exists():
        user_pets = Pet.objects.filter(dealer=user)
        user_aquariums = Aquarium.objects.filter(dealer=user)

        print(f"User's Pets: {user_pets}")
        print(f"User's Aquariums: {user_aquariums}")

        return render(request, 'viewdatabase.html', {'user_pets': user_pets, 'user_aquariums': user_aquariums})
    else:
        # Handle the case where the user is trying to access another user's data
        # You can display an error message or handle it as needed.
        return render(request, '')  # Create an 'access_denied.html' template
    
from django.shortcuts import redirect

@login_required
def delete_item(request, item_type, item_id):
    user = request.user

    if item_type == 'aquarium':
        item = Aquarium.objects.get(id=item_id)
    elif item_type == 'pet':
        item = Pet.objects.get(id=item_id)
    else:
        # Handle invalid item_type, e.g., by displaying an error message.
        return redirect('viewdatabase')

    if item.dealer == user:
        item.delete()
        return redirect('viewdatabase')
    else:
        # Handle unauthorized access, e.g., by displaying an error message.
        return redirect('viewdatabase')




@login_required
def addpets(request):
    if request.method == 'POST':
        category = request.POST.get('category')

        if category == 'aquarium':
            # Process the Aquarium form
            name = request.POST.get('aquarium_name')
            price = request.POST.get('aquarium_price')
            quantity = request.POST.get('pet_quantity')
            description = request.POST.get('aquarium_description')
            location = request.POST.get('aquarium_location')
            image = request.FILES.get('aquarium_image')

            # Create the Aquarium object and associate it with the current user
            Aquarium.objects.create(dealer=request.user, name=name, price=price, quantity=quantity, location=location, image=image,description=description)

        elif category == 'pets':
            # Process the Pet form
            category = request.POST.get('pet_category')
            pet_breed = request.POST.get('pet_breed')
            pet_age = request.POST.get('pet_age')
            price = request.POST.get('pet_price')
            quantity = request.POST.get('pet_quantity')
            pet_description = request.POST.get('pet_description')
            location = request.POST.get('pet_location')
            image = request.FILES.get('pet_image')

            # Create the Pet object and associate it with the current user
            Pet.objects.create(dealer=request.user, category=category, price = price , quantity=quantity, location=location, image=image, pet_breed=pet_breed, pet_age=pet_age, pet_description=pet_description)

        # Redirect to the 'viewdatabase' view for the current user
        return redirect('viewdatabase', dealer_id=request.user.id)

    return render(request, 'addpets.html')

def delete_aquarium(request, aquarium_id):
    aquarium = get_object_or_404(Aquarium, pk=aquarium_id)
    aquarium.delete()
    return redirect('viewdatabase')

def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    pet.delete()
    return redirect('viewdatabase')



def edit_viewdatabase(request, pk):
    item = None
    category = request.POST.get('category')

    if category == 'aquarium':
        item = get_object_or_404(Aquarium, pk=pk)
    elif category == 'pets':
        item = get_object_or_404(Pet, pk=pk)

    if request.method == 'POST':
        # Handle the data update here based on the category
        if category == 'aquarium':
            item.name = request.POST.get('aquarium_name')
            item.price = request.POST.get('aquarium_price')
            item.location = request.POST.get('aquarium_location')
            if request.FILES.get('aquarium_image'):
                item.image = request.FILES.get('aquarium_image')
        elif category == 'pets':
            item.category = request.POST.get('pet_category')
            item.price = request.POST.get('pet_price')
            item.location = request.POST.get('pet_location')
            if request.FILES.get('pet_image'):
                item.image = request.FILES.get('pet_image')

        item.save()  # Save the changes

        # Redirect to a view page or another page as needed
        return redirect('view_database')

    return render(request, 'edit_viewdatabase.html', {'item': item})


def adminviewitem(request):
    pets = Pet.objects.all()
    aquariums = Aquarium.objects.all()

    return render(request, 'adminviewitem.html', {'pets': pets, 'aquariums': aquariums})


def admin_approve_pet(request, pet_id):
    # Get the pet to be approved
    pet = get_object_or_404(Pet, id=pet_id)
    
    # Assuming you have a status field in your Pet model, you can update it to 'approved'
    pet.status = 'approved'
    pet.save()

    # Redirect back to the admin view item page
    return redirect('admin_view_item', item_id=pet.id, item_type='pet')

def admin_reject_pet(request, pet_id):
    # Get the pet to be rejected
    pet = get_object_or_404(Pet, id=pet_id)

    # You can delete the pet or mark it as 'rejected'
    pet.delete()  # Delete the pet
    # OR
    # pet.status = 'rejected'  # Mark it as 'rejected'
    # pet.save()

    # Redirect back to the admin view item page
    return redirect('admin_view_item', item_id=pet.id, item_type='pet')

def admin_approve_aquarium(request, aquarium_id):
    # Get the aquarium to be approved
    aquarium = get_object_or_404(Aquarium, id=aquarium_id)
    
    # Assuming you have a status fie6.status = 'approved'
    aquarium.save()

    # Redirect back to the admin view item page
    return redirect('admin_view_item', item_id=aquarium.id, item_type='aquarium')

def admin_reject_aquarium(request, aquarium_id):
    # Get the aquarium to be rejected
    aquarium = get_object_or_404(Aquarium, id=aquarium_id)

    # You can delete the aquarium or mark it as 'rejected'
    aquarium.delete()  # Delete the aquarium
    # OR
    # aquarium.status = 'rejected'  # Mark it as 'rejected'
    # aquarium.save()

    # Redirect back to the admin view item page
    return redirect('admin_view_item', item_id=aquarium.id, item_type='aquarium')



def usercustomer(request):
        return render(request, 'usercustomer.html')



# def cart(request):
#     pets = Pet.objects.all()
#     aquariums = Aquarium.objects.all()
#     return render(request, 'cart.html', {'pets': pets, 'aquariums': aquariums})

@never_cache
def customer_account(request):
    aquariums = Aquarium.objects.all()
    pets = Pet.objects.all()
    
    return render(request, 'customer_account.html', {'aquariums': aquariums, 'pets': pets})
@never_cache
def dealer_account(request):
        return render(request, 'dealer_account.html')

def enable_aquarium(request, aquarium_id):
    aquarium = get_object_or_404(Aquarium, id=aquarium_id)
    aquarium.is_enabled = True
    aquarium.save()
    return redirect('viewdatabase', user_id=request.user.id)  # Replace 'viewdatabase' with your actual view name

def disable_aquarium(request, aquarium_id):
    aquarium = get_object_or_404(Aquarium, id=aquarium_id)
    aquarium.is_enabled = False
    aquarium.save()
    return redirect('viewdatabase', user_id=request.user.id)

def enable_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.is_enabled = True
    pet.save()
    return redirect('viewdatabase', user_id=request.user.id)

def disable_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.is_enabled = False
    pet.save()
    return redirect('viewdatabase', user_id=request.user.id)

# def add_to_cart(request, category, item_id):
#     cart = Cart(request)

#     if category == 'aquarium':
#         item = get_object_or_404(Aquarium, pk=item_id)
#         context = {
#             'category': 'Aquarium',
#             'name': item.name,
#             'description': item.description,
#             'price': item.price,
#             'quantity': item.quantity,
#             'location': item.location,
#             'image': item.image.url,
#         }
#     elif category == 'pet':
#         item = get_object_or_404(Pet, pk=item_id)
#         context = {
#             'category': 'Pet',
#             'sub_category': item.get_category_display(),
#             'breed': item.pet_breed,
#             'pet_age': item.pet_age,
#             'price': item.price,
#             'quantity': item.quantity,
#             'location': item.location,
#             'image': item.image.url,
#         }
#     else:
#         # Handle other categories if needed
#         return redirect('home')  # Redirect to home if category is not recognized

#     cart.add(item=item)
#     return render(request, 'your_template/add_to_cart.html', context)



# @login_required
# def add_to_cart(request, category, item_id):
#     print(category)
#     print(item_id)
#     uid=request.user
#     user_profile = get_object_or_404(UserProfile, user_id=uid)
#     CartItem.objects.create(
#                         user=user_profile,
#                         item_category="aquarium",
#                         item_id=item_id,
#                         quantity=1
#                     )
#     return redirect('add_to_cart')
    
  
# def add_to_cart(request, category, item_id):
#     try:
#         # Retrieve the item based on the category
#         if category == 'pet':
#             item = get_object_or_404(Pet, id=item_id)
#         elif category == 'aquarium':
#             item = get_object_or_404(Aquarium, id=item_id)
#         else:
#             # Handle other categories if needed
#             item = None

#         if item:
#             if request.user.is_authenticated:
#                 user_profile = get_object_or_404(UserProfile, user=request.user)

#                 # Check if the item is already in the cart
#                 cart_item = CartItem.objects.filter(
#                     user=user_profile,
#                     item_category=category,
#                     item_id=item_id
#                 ).first()

#                 # If the item is already in the cart, update the quantity
#                 if cart_item:
#                     cart_item.quantity += 1
#                     cart_item.save()
#                 else:
#                     # If the item is not in the cart, create a new entry
#                     CartItem.objects.create(
#                         user=user_profile,
#                         item_category=category,
#                         item_id=item_id,
#                         quantity=1
#                     )

#                 messages.success(request, f"{item.name} added to the cart successfully.")
#             else:
#                 messages.warning(request, "Please log in to add items to your cart.")
#     except Exception as e:
#         # Log the exception or handle it appropriately
#         messages.error(request, f"An error occurred while adding the item to the cart: {str(e)}")

#     return redirect('customer_account')


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import CartItem, UserProfile, Aquarium, Pet
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, category, item_id):
    try:
        # Retrieve the item based on the category
        if category == 'pet':
            item = get_object_or_404(Pet, id=item_id)
        elif category == 'aquarium':
            item = get_object_or_404(Aquarium, id=item_id)
        else:
            # Handle other categories if needed
            item = None

        if item:
            if request.user.is_authenticated:
                user_profile = get_object_or_404(UserProfile, user=request.user)

                # Check if the item is already in the cart
                cart_item = CartItem.objects.filter(
                    user=user_profile,
                    item_category=category,
                    item_id=item_id
                ).first()

                # If the item is already in the cart, update the quantity
                if cart_item:
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    # If the item is not in the cart, create a new entry
                    CartItem.objects.create(
                        user=user_profile,
                        item_category=category,
                        item_id=item_id,
                        quantity=1,
                        pet=item if category == 'pet' else None,
                        aquarium=item if category == 'aquarium' else None,
                    )

                return redirect('/mycart/')
            else:
                messages.warning(request, "Please log in to add items to your cart.")
    except Exception as e:
        # Log the exception or handle it appropriately
        messages.error(request, f"An error occurred while adding the item to the cart: {str(e)}")

    return redirect('customer_account')


def mycart(request):
    # Retrieve relevant data and pass it to the template
    user_profile_list = UserProfile.objects.filter(user=request.user)
    
    if not user_profile_list:
        # Handle the case where no UserProfile is found
        return HttpResponse("User profile not found.", status=404)

    # Choose the first UserProfile instance (you may want to modify this logic)
    user_profile = user_profile_list[0]

    cart_items = CartItem.objects.filter(user=user_profile)
    context = {'cart_items': cart_items}
    
    return render(request, 'add_to_cart.html', context)



def item_detail(request, category, item_id):
    if category == 'pet':
        item = get_object_or_404(Pet, id=item_id)
    elif category == 'aquarium':
        item = get_object_or_404(Aquarium, id=item_id)
    else:
        # Handle other categories if needed
        item = None

    return render(request, 'item_detail.html', {'item': item, 'category': category})

# def pet_details(request, pet_id):
#     pet = get_object_or_404(Pet, id=pet_id)

    
#     client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))

#     DATA = {
#     "amount": 100,
#     "currency": "INR",
#     "receipt": "receipt#1",
#     "notes": {
#         "key1": "value3",
#         "key2": "value2"
#      }
#     }
#     payment =client.order.create(data=DATA)
#     return render(request, 'pet_details.html', {'pet': pet})

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import razorpay

def pet_details(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    amount_in_paise = pet.price * 100  # Assuming pet.price is the price of the pet

    if request.method == 'POST':
        # Assuming you have your Razorpay API credentials stored in your Django settings
        razorpay_key_id = "rzp_test_KPliOP7waiGNR8"
        razorpay_key_secret = "ehsJBVnmAmuDFkFbXIsi2Gm3"

        client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))

        DATA = {
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2"
             }
        }
        payment = client.order.create(data=DATA)

        context = {
            'pet': pet,
            'payment': payment,
            'amount_in_paise': amount_in_paise,  # Add the multiplied amount to the context
        }

        return render(request, 'pet_details.html', context)

    return render(request, 'pet_details.html', {'pet': pet, 'amount_in_paise': amount_in_paise})


# def aquarium_details(request, aquarium_id):
#     aquarium = get_object_or_404(Aquarium, id=aquarium_id)
#     context = {'aquarium': aquarium}
#     return render(request, 'aquarium_details.html', context)

def aquarium_details(request, aquarium_id):
    aquarium = get_object_or_404(Aquarium, id=aquarium_id)

    amount_in_paise = aquarium.price * 100  # Assuming pet.price is the price of the pet

    if request.method == 'POST':
        # Assuming you have your Razorpay API credentials stored in your Django settings
        razorpay_key_id = "rzp_test_KPliOP7waiGNR8"
        razorpay_key_secret = "ehsJBVnmAmuDFkFbXIsi2Gm3"

        client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))

        DATA = {
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2"
             }
        }
        payment = client.order.create(data=DATA)

        context = {
            'pet': aquarium,
            'payment': payment,
            'amount_in_paise': amount_in_paise,  # Add the multiplied amount to the context
        }

        return render(request, 'aquarium_details.html', context)

    return render(request, 'aquarium_details.html', {'aquarium': aquarium, 'amount_in_paise': amount_in_paise})




# def buy_now(request, category, item_id):
#     # Your 'buy_now' view logic goes here
#     return render(request, 'customer_account.html')

def buy_now(request, category, item_id):

    return render(request, 'pet_details.html', {'pet': pet, 'order': order})

@csrf_exempt
def razorpay_payment(request):
    print('hello')
    if request.method == 'POST':
        # Verify the Razorpay payment
        params_dict = request.POST
        razorpay_signature = params_dict.get('razorpay_signature')
        order_id = params_dict.get('razorpay_order_id')
        razorpay_payment_id = params_dict.get('razorpay_payment_id')

        # Verify the payment
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        try:
            client.utility.verify_payment_signature(params_dict, razorpay_signature, order_id)
            # Payment verified, process the order or update the status as needed
            return HttpResponse('Payment Successful')
        except Exception as e:
            # Payment verification failed
            return HttpResponse(f'Payment Failed: {str(e)}')
    else:
        # Invalid request method
        return HttpResponse(status=400)
    
    
    
def payment_successful(request):
    if request.method == 'POST':
        # Verify the Razorpay payment
        params_dict = request.POST
        razorpay_signature = params_dict.get('razorpay_signature')
        order_id = params_dict.get('razorpay_order_id')
        razorpay_payment_id = params_dict.get('razorpay_payment_id')

        # Verify the payment
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        try:
            client.utility.verify_payment_signature(params_dict, razorpay_signature, order_id)
            # Payment verified, process the order or update the status as needed

            # Assuming you have an Order model with a 'user' and 'status' field
            try:
                order = Order.objects.get(user=request.user, status='paid')  # Adjust the query as needed

                # Do something with the order, for example, update its status
                order.status = 'completed'
                order.save()

            except Order.DoesNotExist:
                # Handle the case where the order does not exist
                return HttpResponse('Order not found')

            # Redirect to the payment_successful page
            return redirect('payment_successful')

        except Exception as e:
            # Payment verification failed
            return HttpResponse(f'Payment Failed: {str(e)}')
    else:
        # Invalid request method
        return HttpResponse(status=400)
    
def deliveryman_account(request):
    # Your view logic here
     return render(request, 'deliveryman_account.html')
    

