from datetime import timezone
import json
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
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Review, Review_Aquarium
from django.shortcuts import redirect


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


from .models import *


#threading
import threading
import math
from .models import Userpayment, Userpayment_aquarium
#reset passwor generater
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# Create your views here.


#add delivery man
# from django.http import HttpResponseRedirect
# from .forms import DeliveryManForm


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
    # Perform logout logic here
    # For example, you can clear session data
    request.session.clear()
    # Redirect to the desired page after logout
    return redirect('login')


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
    # Query the database to get the deliverymen
    deliverymen = dealer.objects.filter(role='deliveryman')

    # Pass the deliverymen data to the template context
    context = {
        'deliverymen': deliverymen,
    }
    return render(request, 'deliveryman.html', context)



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

# def add_pets(request):
#     # Your view logic for the addpets page
#     return render(request, 'addpets.html')


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


   


def deactivate_user(request, user_id):
    user = get_object_or_404(dealer, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
        
        # Attempt to send deactivation email
        try:
            subject = 'Account Deactivation'
            message = 'Your account has been deactivated by the admin.'
            from_email = 'roshangeorge2024b@mca.ajce.in'  # Replace with your email
            recipient_list = [user.email]
            html_message = render_to_string('deactivation_email.html', {'user': user})

            send_mail(subject, message, from_email, recipient_list, html_message=html_message)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        except Exception as e:
            # Handle other potential errors
            return HttpResponse(f'Error: {str(e)}')
        
        messages.success(request, f"User '{user.username}' has been deactivated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is already deactivated.")
    return redirect('dealers')

def activate_user(request, user_id):
    user = get_object_or_404(dealer, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()

        # Attempt to send activation email
        try:
            subject = 'Account Activation'
            message = 'Your account has been activated by the admin.'
            from_email = 'roshangeorge2024b@mca.ajce.in'  # Replace with your email
            recipient_list = [user.email]
            html_message = render_to_string('activation_email.html', {'user': user})

            send_mail(subject, message, from_email, recipient_list, html_message=html_message)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        except Exception as e:
            # Handle other potential errors
            return HttpResponse(f'Error: {str(e)}')

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
        from_email = 'roshangeorge2k66@gmail.com'  # Replace with your email
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
        from_email = 'roshangeorge2k66@gmail.com'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_email.html', {'customer': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.username}' has been activated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is already active.")
    return redirect(request, 'admin_dashboard.html')



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
            quantity = request.POST.get('aquarium_quantity')
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
            location = request.POST.get('pet_city')
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









@never_cache
def customer_account(request):
    # Fetch all pets from the database
    pets = Pet.objects.all()

    # Check if any of the pets are already sold
    for pet in pets:
        if Userpayment.objects.filter(item=pet).exists():
            pet.status = 'sold'
            pet.save()

    # Fetch all aquariums from the database
    aquariums = Aquarium.objects.all()

    # Check if any of the aquariums are already sold
    for aquarium in aquariums:
        if Userpayment_aquarium.objects.filter(item=aquarium).exists():
            aquarium.status = 'sold'
            aquarium.save()

    # Try to fetch user profile information
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        full_name = user_profile.fullname
        if user_profile.photo:
            photo_url = user_profile.photo.url
        else:
            # Provide a default photo URL or handle it accordingly
            photo_url = '/path/to/default/photo.jpg'  # Adjust this path as needed
    except UserProfile.DoesNotExist:
        # Handle the case where no UserProfile object is found for the user
        full_name = ''
        photo_url = ''
    except UserProfile.MultipleObjectsReturned:
        # Handle the case where multiple UserProfile objects are found for the user
        # You might want to log this error or handle it differently based on your application's requirements
        full_name = ''
        photo_url = ''
    
    context = {
        'full_name': full_name,
        'photo_url': photo_url,
        'pets': pets,
        'aquariums': aquariums
    }

    # Render the template with the updated pet and aquarium status
    return render(request, 'customer_account.html', context)



# def customer_account(request):
#     # Fetch all pets from the database
#     pets = Pet.objects.all()

#     # Check if any of the pets are already sold
#     for pet in pets:
#         if Userpayment.objects.filter(item=pet).exists():
#             pet.status = 'sold'
#             pet.save()

#     # Fetch all aquariums from the database
#     aquariums = Aquarium.objects.all()


#     # Check if any of the aquariums are already sold
#     for aquarium in aquariums:
#         if Userpayment_aquarium.objects.filter(item=aquarium).exists():
#             aquarium.status = 'sold'
#             aquarium.save()

#     # Render the template with the updated pet and aquarium status
            
#     return render(request, 'customer_account.html', {'pets': pets, 'aquariums': aquariums})

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





    
  
# 

# from django.shortcuts import get_object_or_404, redirect, render
# from django.contrib import messages
# from .models import CartItem, UserProfile, Aquarium, Pet
# from django.contrib.auth.decorators import login_required

# @login_required
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
#                 cart_item, created = CartItem.objects.get_or_create(
#                     user=user_profile,
#                     item_category=category,
#                     item_id=item_id,
#                     defaults={'quantity': 1,
#                               'pet': item if category == 'pet' else None,
#                               'aquarium': item if category == 'aquarium' else None}
#                 )

#                 # If the item is already in the cart, update the quantity
#                 if not created:
#                     cart_item.quantity += 1
#                     cart_item.save()

#                 return redirect('/mycart/')
#             else:
#                 messages.warning(request, "Please log in to add items to your cart.")
#     except Exception as e:
#         # Log the exception or handle it appropriately
#         messages.error(request, f"An error occurred while adding the item to the cart: {str(e)}")

#     return redirect('customer_account')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet, Aquarium, CartItem

def add_to_cart(request, category, item_id):
    if request.method == 'POST':
        user = request.user
        quantity = request.POST.get('quantity', 1)  # Assuming you have a quantity input field in your form

        if category == 'pet':
            item = get_object_or_404(Pet, id=item_id)
        elif category == 'aquarium':
            item = get_object_or_404(Aquarium, id=item_id)
        else:
            # Handle invalid category
            return redirect('home')  # Redirect to home page or another appropriate page
        
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            item_category=category,
            item_id=item_id,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        return redirect('add_to_cart_success')  # Assuming you have a URL named 'add_to_cart_success'

    else:
        # Handle GET requests differently if needed
        pass




# def mycart(request):
#     # Retrieve relevant data and pass it to the template
#     user_profile_list = UserProfile.objects.filter(user=request.user)
    
#     if not user_profile_list:
#         # Handle the case where no UserProfile is found
#         return HttpResponse("User profile not found.", status=404)

#     # Choose the first UserProfile instance (you may want to modify this logic)
#     user_profile = user_profile_list[0]

#     cart_items = CartItem.objects.filter(user=user_profile)
#     context = {'cart_items': cart_items}
    
#     return render(request, 'add_to_cart.html', context)


from django.shortcuts import render, redirect

def purchase_item(request):
    if request.method == 'POST':
        # Handle the purchase logic here
        # For example, you can process the purchase and redirect the user to a thank you page
        # After processing the purchase, redirect the user to the purchase.html page or any other page as needed
        return redirect('')  # Replace 'purchase' with the name of the view that renders purchase.html
    else:
        # Handle GET requests (optional)
        # If the request method is GET, render the purchase.html template
        return render(request, 'purchase.html')


# def mycart(request):
#     if request.method == 'POST':
#         # Assuming you have a form to add items to the cart
#         # Retrieve item data from the form submission
#         item_id = request.POST.get('item_id')
#         item_category = request.POST.get('item_category')
#         quantity = int(request.POST.get('quantity'))
        
#         # Retrieve the user's profile
#         user_profile_list = UserProfile.objects.filter(user=request.user)
        
#         if not user_profile_list:
#             return HttpResponse("User profile not found.", status=404)
        
#         user_profile = user_profile_list[0]

#         # Create or update the cart item
#         if item_category == 'pet':
#             # Retrieve pet object based on item_id
#             # Replace 'Pet' with your actual model name for pets
#             pet = Pet.objects.get(id=item_id)
#             # Create or update the cart item for the pet
#             cart_item, created = CartItem.objects.get_or_create(user=user_profile, pet=pet)
#             if not created:
#                 cart_item.quantity += quantity
#                 cart_item.save()
#         elif item_category == 'aquarium':
#             # Retrieve aquarium object based on item_id
#             # Replace 'Aquarium' with your actual model name for aquariums
#             aquarium = Aquarium.objects.get(id=item_id)
#             # Create or update the cart item for the aquarium
#             cart_item, created = CartItem.objects.get_or_create(user=user_profile, aquarium=aquarium)
#             if not created:
#                 cart_item.quantity += quantity
#                 cart_item.save()

#         # Redirect to the cart page after adding items
#         return redirect('mycart')

#     else:
#         user_profile_list = UserProfile.objects.filter(user=request.user)
#         if not user_profile_list:
#             return HttpResponse("User profile not found.", status=404)

#         user_profile = user_profile_list[0]

#         cart_items = CartItem.objects.filter(user=user_profile)
#         context = {'cart_items': cart_items}

#         return render(request, 'add_to_cart.html', context)
    
    from django.shortcuts import render, redirect, HttpResponse
from .models import CartItem, UserProfile, Pet, Aquarium

def mycart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item_category = request.POST.get('item_category')
        quantity =  request.POST.get('quantity')
        
        # Retrieve the user's profile
        user_profile_list = UserProfile.objects.filter(user=request.user)
        
        if not user_profile_list:
            return HttpResponse("User profile not found.", status=404)
        
        user_profile = user_profile_list[0]

        # Create or update the cart item
        if item_category == 'pet':
            # Retrieve pet object based on item_id
            # Replace 'Pet' with your actual model name for pets
            pet = Pet.objects.get(id=item_id)
            # Create or update the cart item for the pet
            cart_item, created = CartItem.objects.get_or_create(user=user_profile, pet=pet)
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        elif item_category == 'aquarium':
            # Retrieve aquarium object based on item_id
            # Replace 'Aquarium' with your actual model name for aquariums
            aquarium = Aquarium.objects.get(id=item_id)
            # Create or update the cart item for the aquarium
            cart_item, created = CartItem.objects.get_or_create(user=user_profile, aquarium=aquarium)
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

        # Redirect to the cart page after adding items
        return redirect('mycart')
    else:
        user_profile_list = UserProfile.objects.filter(user=request.user)
        if not user_profile_list:
            return HttpResponse("User profile not found.", status=404)

        user_profile = user_profile_list[0]

        cart_items = CartItem.objects.filter(user=user_profile)
        det_Pet = Pet.objects.all()
        det_aqu = Aquarium.objects.all()
        context = {'cart_items': cart_items,
                   'det_pet' : det_Pet}

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




from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import razorpay


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

from .models import CartItem, UserProfile, Pet
from django.contrib import messages

def add_to_cart(request, category, item_id):
    # Retrieve the user's profile
    user_profile_list = UserProfile.objects.filter(user=request.user)
    
    if not user_profile_list:
        return HttpResponse("User profile not found.", status=404)
    
    user_profile = user_profile_list[0]

    # Retrieve the item object based on the category
    if category == 'pet':
        item = get_object_or_404(Pet, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(user=user_profile, item_category='pet', item_id=item_id)
    else:
        # Handle for other item categories (e.g., aquarium)
        pass

    if created:
        messages.success(request, f"{item.pet_breed} added to cart successfully!")
    else:
        messages.info(request, f"{item.pet_breed} is already in your cart!")

    return redirect('pet_details', pet_id=item_id)


# from django.shortcuts import render, get_object_or_404
# from django.conf import settings
# from .models import Pet

# def pet_details(request, pet_id):
#     # Assuming you have a Pet model with a location field
#     pet = get_object_or_404(Pet, id=pet_id)
#     currency = 'INR'

#     amount = int(pet.price * 100)  # Convert to integer
#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                        currency=currency,
#                                                        payment_capture='0'))
 
#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = '/paymenthandler/'
 
#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url
#     context['pet'] = pet
#     context['location'] = pet.location  # Add location to context
    
#     return render(request, 'pet_details.html', context=context)


# from django.shortcuts import render, get_object_or_404
# from django.conf import settings
# from .models import Pet
# import razorpay

# def pet_details(request, pet_id):
#     # Assuming you have a Pet model with a location field
#     pet = get_object_or_404(Pet, id=pet_id)
#     currency = 'INR'

#     amount = int(pet.price * 100)  # Convert to integer

#     # Initialize Razorpay client with your API key
#     razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

#     try:
#         # Create Razorpay order
#         razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                            currency=currency,
#                                                            payment_capture='0'))
        
#         # Order ID of the newly created order
#         razorpay_order_id = razorpay_order['id']
#         callback_url = '/paymenthandler/'
        
#         # Pass necessary details to the frontend
#         context = {
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_merchant_key': settings.RAZOR_KEY_ID,
#             'razorpay_amount': amount,
#             'currency': currency,
#             'callback_url': callback_url,
#             'pet': pet,
#             'location': pet.location
#         }
        
#         return render(request, 'pet_details.html', context=context)
    
#     except Exception as e:
#         # Handle exceptions, such as authentication errors
#         error_message = f"An error occurred: {str(e)}"
#         return render(request, 'error.html', {'error_message': error_message})

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Pet
import razorpay

def pet_details(request, pet_id):
    print(f"Request Method: {request.method}")
    request.session['pet_id'] = pet_id
    print(f"Session Pet ID: {request.session['pet_id']}")

    # if request.method == 'POST':
    #     quantity = request.POST.get('quantity', 1)
    #     request.session['quantity'] = int(quantity)
    #     print(f"Pet ID: {pet_id}, Quantity: {quantity}")
    #     return redirect('pets_detail', pet_id=pet_id)
    
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'pet_details.html', {'pet': pet})

def payment_suport(request,pet_id):
    quan =1
    if request.method == 'POST':
        quan = int( request.POST.get('quantity', 1))
        request.session['quantity'] = int(quan)
        print (quan)
    pet = get_object_or_404(Pet, id=pet_id)
    # quan = request.session.get('quantity', 1)
    currency = 'INR'
    amount = int(pet.price * 100)  # Convert to integer
    amount = amount * quan
    total = pet.price * quan
    razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    try:
        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
        razorpay_order_id = razorpay_order['id']
        callback_url = '/paymenthandler/'
        context = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': currency,
            'callback_url': callback_url,
            'pet': pet,
            'quan':quan,
            'total': total,
            'location': pet.location
        }
        print(context)
        return render(request, 'pet_details1.html', context=context)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render(request, 'error.html', {'error_message': error_message})



# from django.shortcuts import render
# import razorpay
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponseBadRequest
 
# from django.http import HttpResponse, HttpResponseBadRequest
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import get_object_or_404
# from .models import Pet
# from django.utils import timezone



# @csrf_exempt
# def paymenthandler(request):
#     if request.method == "POST":
#         try:
#             # Initialize Razorpay client with your API key
#             razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }

#             # Log the received parameters for debugging
#             print("Received POST data:", params_dict)

#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(params_dict)

#             if result:
#                 # Signature verification succeeded
#                 pet_id = request.session.get('pet_id')
#                 if pet_id:
#                     pet = get_object_or_404(Pet, id=pet_id)
#                     pet.status = "inactive"  # Set the status to "inactive"
#                     pet.save()

#                     try:
#                         # Save payment details to Userpayment table
#                         current_datetime = timezone.now()
#                         user_payment_instance = Userpayment.objects.create(
#                             user=request.user,  # Adjust as per your user model
#                             cart=1,  # Adjust as per your requirement
#                             amount=pet.price,
#                             datetime=current_datetime,
#                             order_id_data=razorpay_order_id,
#                             payment_id_data=payment_id,
#                             item=pet 
#                         )
#                         # render success page on successful capture of payment
#                         return render(request, 'payment_success.html')
#                     except Exception as e:
#                         # Log the exception or handle it as appropriate
#                         print(e)  # Print the exception for debugging
#                         return HttpResponse("fail: {}".format(str(e)))
#                 else:
#                     # No pet_id found in session
#                     return HttpResponseBadRequest("No pet_id found in session")
#             else:
#                 # Signature verification failed
#                 return HttpResponse("Razorpay Signature Verification Failed", status=400)
#         except Exception as e:
#             # Log any exceptions for debugging
#             print(e)
#             return HttpResponseBadRequest("An error occurred: {}".format(str(e)))
#     else:
#         # Invalid request method
#         return HttpResponseBadRequest("Invalid request method")


#new

# from django.shortcuts import render, get_object_or_404
# import razorpay
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse, HttpResponseBadRequest
# from .models import Pet
# from django.utils import timezone

# @csrf_exempt
# def paymenthandler(request):
#     if request.method == "POST":
#         try:
#             razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
#             result = razorpay_client.utility.verify_payment_signature(params_dict)

#             if result:
#                 pet_id = request.session.get('pet_id')

#                 if pet_id:
#                     pet = get_object_or_404(Pet, id=pet_id)
#                     pet.status = "inactive"
#                     pet.save()

#                     try:
#                         current_datetime = timezone.now()
#                         user_payment_instance = Userpayment.objects.create(
#                             user=request.user,
#                             cart=1,
#                             amount=pet.price,
#                             datetime=current_datetime,
#                             order_id_data=razorpay_order_id,
#                             payment_id_data=payment_id,
#                             item=pet 
#                         )


#                         user_address = UserProfile.objects.get(user=request.user) 
#                         user=request.user
#                         print("ppp")
#                         print("User Address:", user_address.pincode)
#                         delivery_boys = DeliveryMan.objects.filter(pincode=user_address.pincode)
#                         print("qqq")
#                         print("Delivery Boys:", delivery_boys)
#                         selected_delivery_boy = delivery_boys.first()  
#                         print("rrr")
#                         print("Selected Delivery Boy:", selected_delivery_boy)
                
#                         delivery_assignment = DeliveryAssignment.objects.create(
#                                  user=user,
#                                 delivery_man=selected_delivery_boy,
#                                product=pet
#                            )

#                         return render(request, 'payment_success.html')
#                     except Exception as e:
#                         print(e)
#                         return HttpResponse("fail: {}".format(str(e)))
#                 else:
#                     return HttpResponseBadRequest("No pet_id found in session")
#             else:
#                 return HttpResponse("Razorpay Signature Verification Failed", status=400)
#         except Exception as e:
#             print(e)
#             return HttpResponseBadRequest("An error occurred: {}".format(str(e)))
#     else:
#         return HttpResponseBadRequest("Invalid request method")




from django.shortcuts import render, get_object_or_404
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Pet, Userpayment, UserProfile, DeliveryMan, DeliveryAssignment
from django.utils import timezone

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)

            if result:
                pet_id = request.session.get('pet_id')
                quan = request.session.get('quantity', 1)
                if pet_id:
                    pet = get_object_or_404(Pet, id=pet_id)
                    # pet.quantity = pet.quantity - quan
                    # if pet.quantity == 0 : 
                    #     pet.status = "inactive"
                    # pet.save()

                    current_datetime = timezone.now()
                    user_address = UserProfile.objects.get(user=request.user)
                    amount = pet.price

                    user_payment_instance = Userpayment.objects.create(
                        user=request.user,
                        cart=quan ,
                        amount=amount,
                        datetime=current_datetime,
                        order_id_data=razorpay_order_id,
                        payment_id_data=payment_id,
                        item=pet
                    )

                    delivery_boys = DeliveryMan.objects.filter(pincode=user_address.pincode)
                    selected_delivery_boy = delivery_boys.first()

                    if selected_delivery_boy:
                        delivery_assignment = DeliveryAssignment.objects.create(
                            user=request.user,
                            delivery_man=selected_delivery_boy,
                            product=pet,
                            order_id=razorpay_order_id 
                        )
                    else:
                        return HttpResponse("No delivery boy available for your location.")

                    return render(request, 'payment_success.html')
                else:
                    return HttpResponseBadRequest("No pet_id found in session")
            else:
                return HttpResponse("Razorpay Signature Verification Failed", status=400)
        except Pet.DoesNotExist:
            return HttpResponseBadRequest("Pet not found")
        except UserProfile.DoesNotExist:
            return HttpResponseBadRequest("User profile not found")
        except DeliveryMan.DoesNotExist:
            return HttpResponseBadRequest("No delivery boy found")
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("An error occurred: {}".format(str(e)))
    else:
        return HttpResponseBadRequest("Invalid request method")



# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse, HttpResponseBadRequest
# from django.views.decorators.csrf import csrf_exempt
# from django.utils import timezone
# from .models import Userpayment, DeliveryAssignment
# from .models import Pet, DeliveryMan, UserProfile
# import razorpay
# from django.conf import settings


# @csrf_exempt
# def paymenthandler(request):
#     if request.method == "POST":
#         try:
#             razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
#             result = razorpay_client.utility.verify_payment_signature(params_dict)

#             if result:
#                 pet_id = request.session.get('pet_id')

#                 if pet_id:
#                     pet = get_object_or_404(Pet, id=pet_id)
#                     pet.status = "inactive"
#                     pet.save()

#                     try:
#                         current_datetime = timezone.now()
#                         user_payment_instance = Userpayment.objects.create(
#                             user=request.user,
#                             cart=1,
#                             amount=pet.price,
#                             datetime=current_datetime,
#                             order_id_data=razorpay_order_id,
#                             payment_id_data=payment_id,
#                             item=pet 
#                         )

#                         user_address = UserProfile.objects.get(user=request.user)
#                         delivery_boys = DeliveryMan.objects.filter(pincode=user_address.pincode)
#                         if delivery_boys.exists():
#                             selected_delivery_boy = delivery_boys.first()  
#                             delivery_assignment = DeliveryAssignment.objects.create(
#                                 user=request.user,
#                                 delivery_man=selected_delivery_boy,
#                                 product=pet,
#                                 payment_id=payment_id  # Set payment_id here
#                             )
#                             return render(request, 'payment_success.html')
#                         else:
#                             return HttpResponse("No available delivery boys for this pincode.")
#                     except Exception as e:
#                         print(e)
#                         return HttpResponse("fail: {}".format(str(e)))
#                 else:
#                     return HttpResponseBadRequest("No pet_id found in session")
#             else:
#                 return HttpResponse("Razorpay Signature Verification Failed", status=400)
#         except Exception as e:
#             print(e)
#             return HttpResponseBadRequest("An error occurred: {}".format(str(e)))
#     else:
#         return HttpResponseBadRequest("Invalid request method")


# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# import razorpay


# def aquarium_details(request, aquarium_id):
#     request.session['item_id'] = aquarium_id
#     request.session['item_type'] = 'aquarium'

#     aquarium = get_object_or_404(Aquarium, id=aquarium_id)
#     currency = 'INR'

#     # Ensure amount is at least 100 paise (1 INR)
#     amount = max(int(math.ceil(aquarium.price * 100)), 100)

#     # Ensure amount is a multiple of 100 paise
#     amount = (amount // 100) * 100

#     razorpay_order =razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
 
#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = '/paymenthandler1/'
 
#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url
#     context['aquarium'] = aquarium
#     return render(request, 'aquarium_details.html', context=context)





# from django.shortcuts import render, get_object_or_404
# from django.conf import settings
# from django.urls import reverse
# from django.http import HttpResponseServerError
# import razorpay

# from .models import Aquarium

# def aquarium_details(request, aquarium_id):
#     # Retrieve the aquarium object or return a 404 error if not found
#     aquarium = get_object_or_404(Aquarium, id=aquarium_id)
    
#     # Calculate the amount in the smallest currency unit (paise for INR)
#     amount = int(aquarium.price * 100)
#     currency = 'INR'
    
#     # Initialize the Razorpay client with your API keys
#     razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    
#     try:
#         # Create a Razorpay order
#         razorpay_order = razorpay_client.order.create({
#             'amount': amount,
#             'currency': currency,
#             'payment_capture': '0'  # Set to '1' for automatic capture
#         })
        
#         # Extract the Razorpay order ID
#         razorpay_order_id = razorpay_order['id']
        
#         # Build the callback URL for the payment handler view
#         callback_url = request.build_absolute_uri(reverse('paymenthandler1'))
        
#         # Prepare the context data to pass to the template
#         context = {
#             'aquarium': aquarium,
#             'amount': amount,
#             'currency': currency,
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_merchant_key': settings.RAZOR_KEY_ID,
#             'callback_url': callback_url
#         }
        
#         # Render the aquarium details template with the context data
#         return render(request, 'aquarium_details.html', context=context)
    
#     except razorpay.errors.RazorpayError as e:
#         # Handle Razorpay errors
#         error_message = f"Razorpay error: {e}"
#         return HttpResponseServerError(error_message)
#     except Exception as e:
#         # Handle other unexpected errors
#         error_message = f"An error occurred: {e}"
#         return HttpResponseServerError(error_message)




from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Aquarium
import razorpay

def aquarium_details(request, aquarium_id):
    try:
        aquarium = Aquarium.objects.get(id=aquarium_id)
    except Aquarium.DoesNotExist:
        return render(request, 'error.html', {'error_message': 'Aquarium not found'})

    request.session['aquarium_id'] = aquarium_id
    currency = 'INR'
    amount = int(aquarium.price * 100)  # Convert to integer

    razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    
    try:
        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
        razorpay_order_id = razorpay_order['id']
        callback_url = reverse('paymenthandler1')  # Assuming 'paymenthandler1' is the name of your view
        context = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': currency,
            'callback_url': callback_url,
            'aquarium': aquarium,
            'location': aquarium.location
        }
        return render(request, 'aquarium_details.html', context=context)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render(request, 'error.html', {'error_message': error_message})








# @csrf_exempt
# def paymenthandler1(request):
#     if request.method == "POST":
#         try:
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }

#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(params_dict)

#             item_id = request.session.pop('item_id', None)
#             item_type = request.session.pop('item_type', None)

#             if result is not None:
#                 try:
#                     current_datetime = timezone.now()
#                     if item_type == 'pet':
#                         item = get_object_or_404(Pet, id=item_id)
#                     elif item_type == 'aquarium':
#                         item = get_object_or_404(Aquarium, id=item_id)
#                     else:
#                         # Handle invalid item type
#                         return HttpResponseBadRequest("Invalid item type")

#                     # Save payment details to Userpayment_aquarium table
#                     user_payment_instance = Userpayment_aquarium.objects.create(
#                         user=request.user,
#                         cart=1,
#                         amount=item.price,
#                         datetime=current_datetime,
#                         order_id_data=razorpay_order_id,
#                         payment_id_data=payment_id,
#                         item=item  # Associate the payment with the correct item
#                     )
#                     # render success page on successful capture of payment
#                     return render(request, 'payment_success.html')
#                 except Exception as e:
#                     # Log the exception or handle it as appropriate
#                     print(e)
#                     return HttpResponse("fail: {}".format(str(e)))
#             else:
#                 # if signature verification fails.
#                 return HttpResponse("signature fail")
#         except Exception as e:
#             # if we don't find the required parameters in POST data
#             print(e)
#             return HttpResponseBadRequest()
#     else:
#         # if other than POST request is made.
#         return HttpResponseBadRequest()


from django.shortcuts import render, get_object_or_404
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Aquarium, Userpayment_aquarium, UserProfile, DeliveryMan, DeliveryAssignment1
from django.utils import timezone

@csrf_exempt
def paymenthandler1(request):
    if request.method == "POST":
        try:
            razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)

            if result:
                aquarium_id = request.session.get('aquarium_id')

                if aquarium_id:
                    aquarium = get_object_or_404(Aquarium, id=aquarium_id)
                    aquarium.status = "inactive"
                    aquarium.save()

                    current_datetime = timezone.now()
                    user_address = UserProfile.objects.get(user=request.user)
                    amount = aquarium.price

                    user_payment_instance = Userpayment_aquarium.objects.create(
                        user=request.user,
                        cart=1,
                        amount=amount,
                        datetime=current_datetime,
                        order_id_data=razorpay_order_id,
                        payment_id_data=payment_id,
                        item=aquarium
                    )

                    delivery_boys = DeliveryMan.objects.filter(pincode=user_address.pincode)
                    selected_delivery_boy = delivery_boys.first()

                    if selected_delivery_boy:
                        delivery_assignment = DeliveryAssignment1.objects.create(
                            user=request.user,
                            delivery_man=selected_delivery_boy,
                            product=aquarium,
                            order_id=razorpay_order_id 
                        )
                    else:
                        return HttpResponse("No delivery boy available for your location.")

                    return render(request, 'payment_success.html')
                else:
                    return HttpResponseBadRequest("No aquarium_id found in session")
            else:
                return HttpResponse("Razorpay Signature Verification Failed", status=400)
        except Pet.DoesNotExist:
            return HttpResponseBadRequest("Aquarium not found")
        except UserProfile.DoesNotExist:
            return HttpResponseBadRequest("User profile not found")
        except DeliveryMan.DoesNotExist:
            return HttpResponseBadRequest("No delivery boy found")
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("An error occurred: {}".format(str(e)))
    else:
        return HttpResponseBadRequest("Invalid request method")
















def buy_now(request, category, item_id):

    return render(request, 'customer_account.html', {'pet': pet, 'order': order})

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
    
    
    
@csrf_exempt
def handle_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')

        try:
            order = Order.objects.get(payment_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                order.payment_status = True
                order.save()
                user = request.user
                user.cart.cartitem_set.all().delete()
                return JsonResponse({'message': 'Payment successful'})
            else:
                return JsonResponse({'message': 'Payment failed'})

        except Order.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order ID'})
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'})

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

            # Saving payment information to the database
            user_payment_obj = Userpayment.objects.create(
                user=request.user,  # Assuming you have authenticated users
                amount=params_dict.get('amount'),  # Adjust fields as needed
                datetime=params_dict.get('datetime'),  # Adjust fields as needed
                order_id_data=order_id,
                payment_id_data=razorpay_payment_id,
                # item_id=
            )

            # Redirect to the payment_successful page
            return redirect('payment_success')  # Assuming 'customer_account' is a valid URL name

        except Exception as e:
            # Payment verification faileddea
            return HttpResponse(f'Payment Failed: {str(e)}')
    else:
        # Invalid request method
        return HttpResponse(status=400)
    
# def deliveryman_account(request):
#     # Your view logic here
#      return render(request, 'deliveryman_account.html')
    
   

# from django.contrib.auth.models import User
# from .models import UserProfile

# def deliveryman_account(request):
#     try:
#         # Get the UserProfile object associated with the current user
#         user_profile = UserProfile.objects.get(user=request.user)
#     except UserProfile.DoesNotExist:
#         # If UserProfile does not exist for the current user, create one
#         user_profile = UserProfile.objects.create(
#             user=request.user,
#             fullname=request.user.get_full_name(),  # Assuming User model has first_name and last_name fields
#             # You can set other fields here
#         )

#     context = {
#         'user_profile': user_profile
#     }
#     return render(request, 'deliveryman_account.html', context)


# from django.contrib.auth.models import User
# from .models import UserProfile

# def deliveryman_account(request):
#     try:
#         # Get the UserProfile object associated with the current user
#         user_profile = UserProfile.objects.get(user=request.user)
#     except UserProfile.DoesNotExist:
#         # If UserProfile does not exist for the current user, create one
#         user_profile = UserProfile.objects.create(
#             user=request.user,
#             fullname=request.user.get_full_name(),  # Assuming User model has first_name and last_name fields
#             # You can set other fields here
#         )

#     context = {
#         'user_profile': user_profile
#     }
#     return render(request, 'deliveryman_account.html', context)




# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import UserProfile  # Import the UserProfile model

# @login_required
# def deliveryman_account(request):
#     # Retrieve the user's profile
#     user_profile = UserProfile.objects.get(user=request.user)
#     context = {
#         'user_profile': user_profile
#     }
#     return render(request, 'deliveryman_account.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def deliveryman_account(request):
    user_profiles = UserProfile.objects.filter(user=request.user)
    if user_profiles.exists():
        # If there are multiple UserProfile objects, get the first one
        user_profile = user_profiles.first()
        full_name = user_profile.fullname
        if user_profile.photo:
            photo_url = user_profile.photo.url
        else:
            # Provide a default photo URL or handle it accordingly
            photo_url = '/path/to/default/photo.jpg'  # Adjust this path as needed
    else:
        # Handle the case where the user has no profile
        full_name = ''
        photo_url = ''

    context = {
        'full_name': full_name,
        'photo_url': photo_url
    }

    return render(request, 'deliveryman_account.html', context)





from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dealer_account(request):
    # Logic to fetch dealer details or perform any other operations
    return render(request, 'dealer_account.html')

def payment_success(request):
     return render(request, 'payment_success.html')

def payment_unsuccess(request):
     return render(request, 'payment_unsuccess.html')   



@login_required
def order(request):
    # Get the logged-in customer
    customer = request.user

    # Fetch user payments for the logged-in customer from both models
    user_payments = Userpayment.objects.filter(user=customer)
    user_payments_aquarium = Userpayment_aquarium.objects.filter(user=customer)

    # Fetch all pets
    pets = Pet.objects.all()

    # Extract pet IDs
    pet_ids = [pet.id for pet in pets]

    return render(request, 'order.html', {'user_payments': user_payments, 'user_payments_aquarium': user_payments_aquarium, 'pet_ids': pet_ids})

# def order(request):
#     # Fetch all user payments from both models
#     user_payments = Userpayment.objects.all()  # Retrieve all user payments from Userpayment model
#     user_payments_aquarium = Userpayment_aquarium.objects.all()  # Retrieve all user payments from Userpayment_aquarium model

#     # Fetch all pets
#     pets = Pet.objects.all()

#     # Extract pet IDs
#     pet_ids = [pet.id for pet in pets]

#     return render(request, 'order.html', {'user_payments': user_payments, 'user_payments_aquarium': user_payments_aquarium, 'pet_ids': pet_ids})

def order_management(request):
    # Assuming you have authentication in place to identify the dealer
    dealer = request.user.dealer  # Assuming you have a dealer associated with the user
    
    # Fetching dealer's sales with related user, pet, and payment details
    sales = Userpayment.objects.filter(user=dealer)
    
    context = {
        'sales': sales
    }
    
    return render(request, 'order_management.html', context)
    

# def Dealer_feedback(request):
#      return render(request, 'Dealer_feedback.html') 

def Dealer_feedback(request):
    pet_reviews = Review.objects.all()
    aquarium_reviews = Review_Aquarium.objects.all()
    return render(request, 'Dealer_feedback.html', {'pet_reviews': pet_reviews, 'aquarium_reviews': aquarium_reviews})

from django.utils import timezone
@csrf_exempt
def add_payment_details(request):
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

            # Create a UserPayment instance
            try:
                current_datetime = timezone.now()
                payment_instance = UserPayment.objects.create(
                    user=request.user,  # Assuming the user is authenticated
                    order_id_data=order_id,
                    payment_id_data=razorpay_payment_id,
                    datetime=current_datetime,
                    # Add more fields as needed
                )

                # Optionally, you can perform additional actions here
                # such as updating user account, sending confirmation emails, etc.

                # Redirect to the customer_account.html page
                return redirect('customer_account')  # Adjust the URL name as needed

            except Exception as e:
                # Handle exceptions related to creating UserPayment instance
                return HttpResponse(f'Failed to add payment details: {str(e)}')

        except Exception as e:
            # Payment verification failed
            return HttpResponse(f'Payment Failed: {str(e)}')

    else:
        # Invalid request method
        return HttpResponse(status=400)


    

    def product_details(request, payment_id):
     user_payments= get_object_or_404(Userpayment, pk=payment_id)
    return render(request, 'product_details.html', {'user_payment': user_payment})




def dealer_dashboard(request):
    # Fetch data for the dealer
    dealer_payments = Userpayment.objects.filter(user=request.user.dealer)

    return render(request, 'dealer_dashboard.html', {'dealer_payments': dealer_payments})

# def dealer_sales(request, dealer_id=None):
#     if dealer_id is not None:
#         dealer_obj = dealer.objects.get(id=dealer_id)
#         payments_pet = Userpayment.objects.filter(item__dealer=dealer_obj)
#         payments_aquarium = Userpayment_aquarium.objects.filter(item__dealer=dealer_obj)
#     else:
#         # If no dealer_id is provided, fetch all payments
#         payments_pet = Userpayment.objects.all()
#         payments_aquarium = Userpayment_aquarium.objects.all()
    
#     context = {
#         'dealer': dealer_obj if dealer_id is not None else None,
#         'payments': list(payments_pet) + list(payments_aquarium)
#     }
#     return render(request, 'dealer_sales.html', context)


@login_required
def dealer_sales(request):
    # Retrieve the logged-in dealer
    dealer_obj = request.user
    
    # Filter payments for pets belonging to the dealer
    payments_pet = Userpayment.objects.filter(item__dealer=dealer_obj)
    
    # Filter payments for aquariums belonging to the dealer
    payments_aquarium = Userpayment_aquarium.objects.filter(item__dealer=dealer_obj)
    
    context = {
        'dealer': dealer_obj,
        'payments': list(payments_pet) + list(payments_aquarium)
    }
    return render(request, 'dealer_sales.html', context)


def payment_details_view(request):
    # For Pet payments
    pet_payments = Userpayment.objects.select_related('user', 'item').all()
    pet_payment_details = []
    for payment in pet_payments:
        pet_payment_details.append({
            'payment_id': payment.id,
            'customer_id': payment.user.id,
            'customer_name': payment.user.fullname,
            'dealer_id': payment.item.dealer.id,
            'dealer_name': payment.item.dealer.fullname,
            'order_id': payment.order_id_data,
            'payment_details': payment.payment_id_data,
            'item_id': payment.item.id,
            'item_name': payment.item.pet_breed,
            'item_image': payment.item.image.url,
            'amount': payment.amount,
            'datetime': payment.datetime
        })

    # For Aquarium payments
    aquarium_payments = Userpayment_aquarium.objects.select_related('user', 'item').all()
    aquarium_payment_details = []
    for payment in aquarium_payments:
        aquarium_payment_details.append({
            'payment_id': payment.id,
            'customer_id': payment.user.id,
            'customer_name': payment.user.fullname,
            'dealer_id': payment.item.dealer.id,
            'dealer_name': payment.item.dealer.fullname,
            'order_id': payment.order_id_data,
            'payment_details': payment.payment_id_data,
            'item_id': payment.item.id,
            'item_name': payment.item.name,
            'item_image': payment.item.image.url,
            'amount': payment.amount,
            'datetime': payment.datetime
        })

    # Pass the payment details to the template
    return render(request, 'payment_details.html', {'pet_payments': pet_payment_details, 'aquarium_payments': aquarium_payment_details})

# @login_required
# def submit_review(request):
#     if request.method == 'POST':
#         product_name = request.POST.get('item-name')
#         rating = request.POST.get('product_rating')
#         review_text = request.POST.get('product_review')
#         print(product_name)

#         print(rating)
#         print(review_text)

#         # Get the current user as the dealer
#         dealer = request.user

#         # Create a new review object and save it to the database
#         review = Review.objects.create(
#             dealer=dealer,
#             product_name=product_name,
#             rating=rating,
#             review_text=review_text
#         )

#         # Optionally, you can add validation logic here before saving the review

#         messages.success(request, 'Your review has been submitted successfully.')
#         return redirect('customer_account')  # Redirect to the home page or any other page you prefer
#     return render(request, 'order.html')



@login_required
def submit_review(request, pet_id):
    if request.method == 'POST':
        rating = request.POST.get('product_rating')
        review_text = request.POST.get('product_review')

        # Get the current user as the dealer
        dealer = request.user

        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            messages.error(request, 'The selected pet does not exist.')
            return redirect('customer_account')  # Redirect to a suitable page if the pet doesn't exist

        # Create a new review object and save it to the database
        review = Review.objects.create(
            dealer=dealer,
            pet=pet,
            rating=rating,
            review_text=review_text
        )

        # Optionally, you can add validation logic here before saving the review

        messages.success(request, 'Your review has been submitted successfully.')
        return redirect('customer_account')  # Redirect to the home page or any other page you prefer
    return render(request, 'order.html')


@login_required
def submit_review_aqu(request, aquarium_id):
    if request.method == 'POST':
        # Retrieve data from the POST request
        rating_aqu = request.POST.get('product_rating_aqu')  # Update to match the name attribute in the form
        review_text_aqu = request.POST.get('product_review_aqu')  # Update to match the name attribute in the form

        # Get the current user as the dealer
        dealer = request.user

        try:
            aquarium = Aquarium.objects.get(id=aquarium_id)
        except Aquarium.DoesNotExist:
            messages.error(request, 'The selected aquarium does not exist.')
            return redirect('customer_account')  # Redirect to a suitable page if the aquarium doesn't exist

        # Create a new review object and save it to the database
        review = Review_Aquarium.objects.create(
            dealer_aqu=dealer,
            aquarium=aquarium,
            rating_aqu=rating_aqu,
            review_text_aqu=review_text_aqu
        )

        # Optionally, you can add validation logic here before saving the review

        messages.success(request, 'Your review has been submitted successfully.')
        return redirect('customer_account')  # Redirect to the home page or any other page you prefer
    
    # If the request method is not POST, render the form again
    return render(request, 'order.html')







# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.conf import settings
# import csv
# from .models import DeliveryMan, dealer
# import random
# import string
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.urls import reverse
# from django.core.mail import send_mail
# from django.conf import settings
# from django.urls import reverse

# # Define a function to generate a temporary password
# def generate_temporary_password():
#     # Generate a random password of length 10
#     temporary_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
#     return temporary_password

# class CustomTokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return (
#             str(user.pk) + str(timestamp) + str(user.email)
#         )

# def send_login_email(delivery_man, temporary_password, request):
#     subject = 'Your account has been created'
#     # Generate unique token for login link using custom token generator
#     token_generator = CustomTokenGenerator()
#     token = token_generator.make_token(delivery_man)
#     uid = urlsafe_base64_encode(force_bytes(delivery_man.pk))
#     # Construct login link
#     login_link = request.build_absolute_uri(reverse('login')) + f'?uid={uid}&token={token}'
#     message = f'Hi {delivery_man.name},\n\nYour account has been created successfully. You can login using the following link:\n{login_link}\n\nUsername: {delivery_man.email}\nTemporary Password: {temporary_password}\n\nPlease login to your account and change your password.\n\nBest regards,\nYour Company Name'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [delivery_man.email]
#     send_mail(subject, message, email_from, recipient_list)


# def add_delivery_man(request):
#     if request.method == 'POST':
#         if 'csvFile' in request.FILES:  # If CSV file is uploaded
#             csv_file = request.FILES['csvFile']
#             decoded_file = csv_file.read().decode('utf-8').splitlines()
#             csv_reader = csv.reader(decoded_file)
#             for row in csv_reader:
#                 name, email, phone, house_name, district, city, pincode, vehicle_type, vehicle_no = row
#                 delivery_man = DeliveryMan.objects.create(
#                     name=name,
#                     email=email,
#                     phone=phone,
#                     house_name=house_name,
#                     district=district,
#                     city=city,
#                     pincode=pincode,
#                     vehicle_type=vehicle_type,
#                     vehicle_no=vehicle_no
#                 )
#                 temporary_password = generate_temporary_password()  # Generate temporary password
#                 send_login_email(delivery_man, temporary_password, request)  # Send login email with temporary password
#             return redirect('admin_dashboard')
#         else:  # If form is submitted
#             name = request.POST.get('name')
#             email = request.POST.get('email')
#             phone = request.POST.get('phone')
#             house_name = request.POST.get('house_name')
#             district = request.POST.get('district')
#             city = request.POST.get('city')
#             pincode = request.POST.get('pincode')
#             vehicle_type = request.POST.get('vehicle_type')
#             vehicle_no = request.POST.get('vehicle_no')
#             # Check if dealer with same email already exists
#             existing_dealer = dealer.objects.filter(email=email).first()
#             if existing_dealer:
#                 # Update existing dealer object
#                 existing_dealer.fullname = name
#                 existing_dealer.save()
#             else:
#                 # Create new dealer object
#                 dealer_obj = dealer.objects.create(
#                     email=email,
#                     username=email,
#                     fullname=name,
#                     role="deliveryman"
#                 )
#                 dealer_obj.set_password('temporary_password')  # Set temporary password
#                 dealer_obj.save()
#             delivery_man = DeliveryMan.objects.create(
#                 name=name,
#                 email=email,
#                 phone=phone,
#                 house_name=house_name,
#                 district=district,
#                 city=city,
#                 pincode=pincode,
#                 vehicle_type=vehicle_type,
#                 vehicle_no=vehicle_no
#             )
#             temporary_password = generate_temporary_password()  # Generate temporary password
#             send_login_email(delivery_man, temporary_password, request)  # Send login email with temporary password
#             return redirect('admin_dashboard')
#     return render(request, 'add_delivery_man.html')

from django.shortcuts import render, redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import csv
import random
import string
from .models import DeliveryMan, dealer

# Define a function to generate a temporary password
def generate_temporary_password():
    # Generate a random password of length 10
    temporary_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return temporary_password

class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.email)
        )

def send_login_email(delivery_man, temporary_password, request):
    subject = 'Your account has been created'
    # Generate unique token for login link using custom token generator
    token_generator = CustomTokenGenerator()
    token = token_generator.make_token(delivery_man)
    uid = urlsafe_base64_encode(force_bytes(delivery_man.pk))
    # Construct login link
    login_link = request.build_absolute_uri(reverse('login')) + f'?uid={uid}&token={token}'
    message = f'Hi {delivery_man.name},\n\nYour account has been created successfully. You can login using the following link:\n{login_link}\n\nUsername: {delivery_man.email}\nTemporary Password: {temporary_password}\n\nPlease login to your account and change your password.\n\nBest regards,\nYour Company Name'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [delivery_man.email]
    send_mail(subject, message, email_from, recipient_list)

def add_delivery_man(request):
    if request.method == 'POST':
        if 'csvFile' in request.FILES:  # If CSV file is uploaded
            csv_file = request.FILES['csvFile']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)
            for row in csv_reader:
                name, email, phone, house_name, district, city, pincode, vehicle_type, vehicle_no = row
                # Check if dealer with same email already exists
                existing_dealer = dealer.objects.filter(email=email).first()
                if existing_dealer:
                    # Update existing dealer object
                    existing_dealer.fullname = name
                    existing_dealer.save()
                else:
                    # Create new dealer object
                    dealer_obj = dealer.objects.create(
                        email=email,
                        username=email,
                        fullname=name,
                        role="deliveryman"
                    )

                delivery_man = DeliveryMan.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    house_name=house_name,
                    district=district,
                    city=city,
                    pincode=pincode,
                    vehicle_type=vehicle_type,
                    vehicle_no=vehicle_no
                )
                temporary_password = generate_temporary_password()  # Generate temporary password
                send_login_email(delivery_man, temporary_password, request)  # Send login email with temporary password
            return redirect('admin_dashboard')
        else:  # If form is submitted
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            house_name = request.POST.get('house_name')
            district = request.POST.get('district')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            vehicle_type = request.POST.get('vehicle_type')
            vehicle_no = request.POST.get('vehicle_no')

            dealer_obj, created = dealer.objects.get_or_create(
                email=email,
                defaults={'username': email, 'fullname': name, 'role': "deliveryman"}
            )
            if not created:
                # Update existing dealer object
                dealer_obj.fullname = name
                dealer_obj.save()

            # Create DeliveryMan object
            delivery_man = DeliveryMan.objects.create(
                name=name,
                email=email,
                phone=phone,
                house_name=house_name,
                district=district,
                city=city,
                pincode=pincode,
                vehicle_type=vehicle_type,
                vehicle_no=vehicle_no
            )

            # Generate temporary password
            temporary_password = generate_temporary_password()

            # Set temporary password for dealer object
            dealer_obj.set_password(temporary_password)
            dealer_obj.save()

            # Send login email with temporary password
            send_login_email(delivery_man, temporary_password, request)

            return redirect('admin_dashboard')

    return render(request, 'add_delivery_man.html')
    

















def Delivery_successfully_registerd(request):
    return render(request, 'Delivery_successfully_registerd.html')

def Delivery_unsuccessfully_registerd(request):
    return render(request, 'Delivery_unsuccessfully_registerd.html')





def deliveryman_list(request):
    deliverymen = DeliveryMan.objects.all()
    return render(request, 'deliveryman_list.html', {'deliverymen': deliverymen})

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user

        # Check if the current password is correct
        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')

        # Check if the new passwords match
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('change_password')

        # Set the new password
        user.set_password(new_password1)
        user.save()

        # Update session to prevent the user from being logged out
        update_session_auth_hash(request, user)

        messages.success(request, 'Password changed successfully.')
        return redirect('deliveryman_account')  # Redirect to the appropriate URL after password change

    return render(request, 'change_password.html')

from django.shortcuts import render
from django.http import JsonResponse

# Placeholder function for simulating fish species prediction
def predict_fish_species(image):
    # Simulate prediction result
    return "Simulated Fish Species"

# Placeholder function for simulating grouping of compatible species
def group_compatible_species(species):
    # Simulate grouping of compatible species
    return ["Simulated Species 1", "Simulated Species 2", "Simulated Species 3"]

def home(request):
    return render(request, 'home.html')

def predict(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        
        # Simulate prediction using the placeholder function
        predicted_species = predict_fish_species(image)
        
        # Return the simulated predicted species as JSON response
        return JsonResponse({'predicted_species': predicted_species})
    else:
        return JsonResponse({'error': 'No image file uploaded'})

def group_species(request):
    if request.method == 'POST' and 'species' in request.POST:
        species = request.POST['species']
        
        # Simulate grouping of compatible species using the placeholder function
        grouped_species = group_compatible_species(species)
        
        # Return the simulated grouped species as JSON response
        return JsonResponse({'grouped_species': grouped_species})
    else:
        return JsonResponse({'error': 'No species provided'})
    
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        # Handle the uploaded CSV file here
        csv_file = request.FILES['csv_file']
        # Process the CSV file data
        
        # Render success message or perform other operations
        return render(request, 'upload_csv.html', {'success_message': 'CSV file uploaded successfully'})
    else:
        return render(request, 'upload_csv.html')
    

    # views.py

from django.shortcuts import render
from .models import Pet, Aquarium

def search_results(request):
    # Retrieve the search query from the GET parameters
    query = request.GET.get('query')

    # Perform the search logic
    pets = Pet.objects.filter(pet_breed__icontains=query) | Pet.objects.filter(pet_description__icontains=query)
    aquariums = Aquarium.objects.filter(name__icontains=query) | Aquarium.objects.filter(description__icontains=query)

    # Pass the search results to the template
    context = {
        'query': query,
        'pets': pets,
        'aquariums': aquariums,
    }
    
    return render(request, 'customer_account.html', context)


@never_cache
@login_required
def chatbot_redirect(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        # Check if the message is a greeting
        if message.lower() in ['hello', 'hai', 'hi', 'hola']:
            response_message = "How can I help you?"
            return JsonResponse({'response_message': response_message})

        # Check if the message contains the word 'packages' or 'package'
        if 'packages' in message.lower() or 'package' in message.lower():
            # If 'packages' is found in the message, construct the response with a link to view packages
            view_packages_link = reverse('matdest:view_packages')
            booked_packages_link = reverse('matdest:my_packages')

            response_message = "Here are some matching links:<br>"
            response_message += f"<a href='{view_packages_link}'>View Packages</a><br>"
            response_message += f"<a href='{booked_packages_link}'>Show Booked Packages</a>"
            return JsonResponse({'response_message': response_message})

        # Implement your logic here to determine the redirect URL based on the message
        if message.lower() == 'premium':
            response_message = "Click to get more details of premium: <a href='{}'>Premium</a>".format(reverse('matpayment:view_premium'))
            return JsonResponse({'response_message': response_message})
        
        if message.lower() == 'booking':
            response_message = "Click to get more details of booked packages: <a href='{}'>My Bookings</a>".format(reverse('matdest:my_packages'))
            return JsonResponse({'response_message': response_message})
        
        if 'chat' in message.lower() or 'chats' in message.lower() or 'message' in message.lower():
            response_message = "Click to get mychats: <a href='{}'>Chats</a>".format(reverse('matchat:mychats'))
            return JsonResponse({'response_message': response_message})
        else:
            redirect_url = '/path/to/default/view/'  # Replace with the default URL

        # If the message doesn't match any predefined responses, construct a default response
        default_response = "Sorry, your query didn't match any of our options."
        return JsonResponse({'response_message': default_response})
    else:
        # If the request method is not POST, return an error response
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# @never_cache
# def location(request):
#         return render(request, 'location.html')
@never_cache
@login_required
def location(request):
    # Retrieve user's full name and photo
    user_profile = UserProfile.objects.filter(user=request.user).first()
    if user_profile:
        full_name = user_profile.fullname
        photo_url = user_profile.photo.url if user_profile.photo else '/path/to/default/photo.jpg'
    else:
        full_name = ''
        photo_url = ''

    context = {
        'full_name': full_name,
        'photo_url': photo_url
    }
    return render(request, 'location.html', context)

@never_cache
def loc(request):
        return render(request, 'loc.html')


# 

from django.shortcuts import render, redirect
from .models import Userpayment, Userpayment_aquarium
from .models import AcceptedOrder  # Import the AcceptedOrder model if not already imported
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def del_orders(request):
    user_profiles = UserProfile.objects.filter(user=request.user)
    if user_profiles.exists():
        # If there are multiple UserProfile objects, get the first one
        user_profile = user_profiles.first()
        full_name = user_profile.fullname
        if user_profile.photo:
            photo_url = user_profile.photo.url
        else:
            # Provide a default photo URL or handle it accordingly
            photo_url = '/path/to/default/photo.jpg'  # Adjust this path as needed
    else:
        # Handle the case where the user has no profile
        full_name = ''
        photo_url = ''

    user_payments = Userpayment.objects.select_related('user').all()
    user_aquarium_payments = Userpayment_aquarium.objects.select_related('user').all()

    context = {
        'full_name': full_name,
        'photo_url': photo_url,
        'user_payments': user_payments,
        'user_aquarium_payments': user_aquarium_payments
    }
    return render(request, 'del_orders.html', context)










@never_cache
def your_deliveries(request):
        return render(request, 'your_deliveries.html')

from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import redirect

def process_selected_items(request):
     if request.method == 'POST':
        selected_items_list = request.POST.getlist('selected_items')
        # Convert the selected items to a list of dictionaries
        selected_deliveries = []
        for item_str in selected_items_list:
            parts = item_str.split(',')
            if len(parts) >= 3:
                order_id, item_name, status = parts
                selected_deliveries.append({
                    'order_id': order_id,
                    'item_name': item_name,
                    'status': status
                })
        # Store selected items in session
        request.session['selected_deliveries'] = selected_deliveries
        return redirect('selected_deliveries')
     else:
        return redirect('error')  



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def selected_deliveries(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    full_name = user_profile.fullname if user_profile else ''
    photo_url = user_profile.photo.url if user_profile and user_profile.photo else '/path/to/default/photo.jpg'

    selected_deliveries_pets = []
    selected_deliveries_aquarium = []

    # Retrieve selected deliveries from session
    selected_items_list = request.session.get('selected_deliveries', [])
    for item_dict in selected_items_list:
        if isinstance(item_dict, dict):
            order_id = item_dict.get('order_id')
            item_name = item_dict.get('item_name')
            status = item_dict.get('status')
            # Depending on item type, retrieve relevant data and append to the respective list
            if item_name.startswith('pet'):
                # Assuming you have logic to fetch data for pets
                selected_deliveries_pets.append({
                    'order_id': order_id,
                    'item': item_name,
                    'status': status,
                    # Add more fields as needed
                })
            elif item_name.startswith('aquarium'):
                # Assuming you have logic to fetch data for aquariums
                selected_deliveries_aquarium.append({
                    'order_id': order_id,
                    'item': item_name,
                    'status': status,
                    # Add more fields as needed
                })
        else:
            # Handle the case where the session data is not in the expected format
            pass

    context = {
        'full_name': full_name,
        'photo_url': photo_url,
        'selected_deliveries_pets': selected_deliveries_pets,
        'selected_deliveries_aquarium': selected_deliveries_aquarium
    }

    return render(request, 'selected_deliveries.html', context)

def pet_describtion(request, pet_id):
    # Assuming you have a Pet model with a location field
    pet = get_object_or_404(Pet, id=pet_id)
    currency = 'INR'

    amount = int(pet.price * 100)  # Convert to integer
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['pet'] = pet
    context['location'] = pet.location  # Add location to context
    
    return render(request, 'pet_describtion.html', context=context)


# from django.shortcuts import render, get_object_or_404
# from .models import Aquarium

# def aquarium_describtion(request, aquarium_id):
#     # Assuming you have a Aquarium model with a location field
#     aquarium = get_object_or_404(Aquarium, id=aquarium_id)

#     # Prepare context data to pass to the template
#     context = {
#         'aquarium': aquarium,
#         'location': aquarium.location  # Add location to context if needed
#     }
    
#     return render(request, 'aquarium_describtion.html', context=context)

# from django.shortcuts import render, get_object_or_404
# from .models import Pet

# def pet_describtion(request, pet_id):
#     # Assuming you have a Aquarium model with a location field
#     pet = get_object_or_404(Pet, id=pet_id)

#     # Prepare context data to pass to the template
#     context = {
#         'pet': pet,
#         'location': pet.location  # Add location to context if needed
#     }
    
#     return render(request, 'pet_describtion.html', context=context)



from django.shortcuts import render, get_object_or_404, redirect
from .models import Pet, Aquarium, CartItem

def aquarium_description(request, aquarium_id):
    aquarium = get_object_or_404(Aquarium, id=aquarium_id)
    context = {
        'aquarium': aquarium,
        'location': aquarium.location
    }
    if request.method == 'POST':
        # Process form submission
        # Assuming you have a form field named 'quantity'
        quantity = request.POST.get('quantity', '1')
        user = request.user  # Assuming the user is authenticated
        cart_item = CartItem.objects.create(
            user=user,
            item_category='aquarium',
            item_id=aquarium.id,
            quantity=quantity
        )
        # Optionally, you can add a success message here
        return redirect('cart')  # Redirect to the cart page or any other page
    return render(request, 'aquarium_description.html', context=context)

# def pet_description(request, pet_id):
#     pet = get_object_or_404(Pet, id=pet_id)
#     context = {
#         'pet': pet,
#         'location': pet.location
#     }
#     if request.method == 'POST':
#         # Process form submission
#         # Assuming you have a form field named 'quantity'
#         quantity = request.POST.get('quantity', 1)
#         user = request.user  # Assuming the user is authenticated
#         cart_item = CartItem.objects.create(
#             user=user,
#             item_category='pet',
#             item_id=pet.id,
#             quantity=quantity
#         )
#         # Optionally, you can add a success message here
#         return redirect('cart')  # Redirect to the cart page or any other page
#     return render(request, 'pet_description.html', context=context)

from django.shortcuts import redirect

def pet_description(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    context = {'pet': pet}
    
    if request.method == 'POST':
        user = UserProfile.objects.get (user=request.user)
        item_id = pet.id
        quantity = request.POST.get('quantity', 1)
    
        cart_item = CartItem.objects.create(
                user=user,
                item_category='pet',
                item_id=item_id,
                quantity=quantity
            )
            # Optionally, you can add a success message here
        return redirect('mycart')      
    return render(request, 'pet_description.html', context=context)


def add_wishlist(request,pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        user = UserProfile.objects.get (user=request.user)
        item_id = pet.id
        quantity = request.POST.get('quantity', 1)
        wishlist_item = Wishlist.objects.create(
                user=user,
                item_category=pet.category,
                item_id=item_id,
                quantity=quantity
            )
            # Optionally, you can add a success message here
        return redirect('wishlist')  





# from .models import CartItem, UserProfile, Pet, Aquarium
# def wishlist(request):
#     wishlist_items = Wishlist.objects.all()
#     return render(request, 'wishlist.html',{'wishlist_items': wishlist_items})
    

from django.shortcuts import render
from .models import Wishlist

def wishlist(request):
    # Fetch wishlist items along with related Pet or Aquarium objects
    wishlist_items = Wishlist.objects.select_related('pet', 'aquarium').all()
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Aquarium, Wishlist
# from .forms import WishlistForm  # Import the WishlistForm if you have one

# def add_to_wishlist(request, aquarium_id):
#     aquarium = get_object_or_404(Aquarium, id=aquarium_id)
    
#     if request.method == 'POST':
#         form = WishlistForm(request.POST)
#         if form.is_valid():
#             # Create a Wishlist entry
#             wishlist_item = form.save(commit=False)
#             wishlist_item.user = request.user  # Assuming you have user authentication
#             wishlist_item.item_category = 'aquarium'  # Set the item category
#             wishlist_item.item_id = aquarium.id
#             wishlist_item.save()
#             return redirect('aquarium_description', aquarium_id=aquarium_id)
#     else:
#         form = WishlistForm()
    
#     return render(request, 'aquarium_description.html', {'aquarium': aquarium, 'form': form})

def add_to_wishlist(request, aquarium_id):
    aqua = Aquarium.objects.get(id=aquarium_id)
    
    print(aqua)
    return redirect('aquarium_description', aquarium_id=aquarium_id)


def purchase(request):
        return render(request, 'purchase.html')


# views.py

from django.shortcuts import redirect, get_object_or_404
from .models import CartItem

def delete_item(request, item_id):
    # Retrieve the item from the database
    item = get_object_or_404(CartItem, id=item_id)
    
    # Perform deletion
    item.delete()

    # Redirect to the shopping cart page or any other appropriate page
    return redirect('mycart')  # Replace 'cart_page' with the URL name for your cart page


# views.py

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import CartItem, Userpayment, UserProfile, Pet
import razorpay

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=("YOUR_KEY_ID", "YOUR_KEY_SECRET"))  # Replace with your Razorpay API key

@login_required
def purchase_all_items(request):
    if request.method == "POST":
        # Retrieve the current user
        user = request.user
        
        # Retrieve all items in the user's cart
        cart_items = UserProfile.objects.get (user=request.user)
        
        # Process the purchase for each item in the cart
        for item in cart_items:
            # Process the purchase logic for each item (similar to existing purchase logic)
            # Example: Create a payment record, update item status, etc.
            # This logic can be similar to the existing payment logic in your payment handler view

            # Create a payment record for each item in the cart
            # Adjust the payment logic as per your requirements
            Userpayment.objects.create(
                user=user,
                cart=item.cart,
                amount=item.pet.price,  # Assuming you are using the price of the pet
                datetime=timezone.now(),
                order_id_data="order_id",  # Replace with actual order ID
                payment_id_data="payment_id",  # Replace with actual payment ID
                item=item.pet  # Assuming the item is a Pet instance
            )

            # Mark the item as purchased or remove it from the cart
            # Example: Update the status of the item or delete it from the cart
            item.delete()  # Delete the item from the cart after purchase

        # Redirect to a success page or back to the cart page
        return redirect('payment_success')  # Replace 'cart_page' with the actual URL name for your cart page
    else:
        # Handle GET requests or other HTTP methods
        return redirect('cart')  # Redirect back to the cart page

# Other view functions...
    



    #new

# user_profile.latitude = latitude
#         user_profile.longitude = longitude
        
#         user_profile.save()

#         deliveryagent.license_number = license
#         deliveryagent.vechicle_type = vehicle_type
#         deliveryagent.latitude = latitude
#         deliveryagent.longitude = longitude
#         deliveryagent.availability = availability
#         deliveryagent.is_approved = DeliveryAgent.UPDATED
        
#         deliveryagent.save()
#     return render(request, 'deliveryagent/agent_index.html', {'deliveryagent': deliveryagent,'orderitem_delivered_count':orderitem_delivered_count,'orderitem_pending_count':orderitem_pending_count,'allreviews':allreviews,'avg_rating':avg_rating,'orderitem_count':orderitem_count})
   


# def agent_loggout(request):
#     print('Logged Out')
#     logout(request)
#     if 'username' in request.session:
#         del request.session['username']
#         request.session.clear()
#     return redirect(loginu)

# @login_required
# def agentorders(request):
#     deliveryagent = DeliveryAgent.objects.get(user=request.user)
#     return render(request, 'deliveryagent/agentorders.html',{'deliveryagent': deliveryagent})

# @login_required
# def agentprofile(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     deliveryagent = DeliveryAgent.objects.get(user=request.user)
#     if request.method == 'POST':
#         name = request.POST.get('name')
        
#         profile_pic = request.FILES.get('profile_pic')
#         phone_number = request.POST.get('phone_number')
#         address = request.POST.get('address')
#         reset_password = request.POST.get('reset_password')
#         old_password = request.POST.get('old_password') 
        

#         if 'profile_pic' in request.FILES:
#             profile_pic = request.FILES['profile_pic']
#             user_profile.profile_pic = profile_pic
#             print('got')
#         user_profile.name = name
#         deliveryagent.name = name
#         user_profile.phone_number = phone_number
#         deliveryagent.contact = phone_number
#         user_profile.address = address
#         deliveryagent.address=address
        

#         # Check if all three password fields are not empty
#         if old_password and reset_password and request.POST.get('cpass') == reset_password:
#             if request.user.check_password(old_password):
#                 # The old password is correct, set the new password
#                 request.user.set_password(reset_password)
#                 request.user.save()
#                 update_session_auth_hash(request, request.user)  # Update the session to prevent logging out
#             else:
#                 messages.error(request, "Incorrect old password. Password not updated.")
#         else:
#             print("Please fill all three password fields correctly.")
        
#         user_profile.reset_password = reset_password
#         user_profile.save()
#         request.user.save()
#         deliveryagent.save()
#         return redirect('agentprofile') 

#     context = {
#         'user_profile': user_profile,
#         'deliveryagent': deliveryagent
#     }
#     return render(request, 'deliveryagent/agent_profile.html', context)

# @login_required
# def agentorder(request):
#     user = request.user

#     # If the user is a delivery agent, retrieve the delivery agent profile
#     deliveryagent = DeliveryAgent.objects.get(user=user)

    
#     # Retrieve the orders for the current delivery agent where payment is not pending
#     agent_orders = OrderItem.objects.filter(
#         deliveryagent=deliveryagent,
#         order__payment_status=Order.PaymentStatusChoices.SUCCESSFUL  # Filter by payment status
#     )

#     order_items = []
#     for order in agent_orders:
#         itemorder = order.order
     
#         assign = Assigndeliveryagent.objects.get(deliveryagent=deliveryagent,order=order.order)
#         billing = assign.billingdetails
#         order_items.append((order, itemorder, billing))
    
#     context = {
#         'deliveryagent': deliveryagent,
#         'order_items': order_items,
#     }

#     return render(request, 'deliveryagent/agentorders.html', context)    

# def trackmyorder(request):
#     user=request.user
#     order=DeliveryAssignment.objects.filter(user=user)
#     context={
#         'order':order
#     }
#     return render (request,'trackmyorder.html',context)



# from django.shortcuts import render
# from .models import DeliveryAssignment

# def trackmyorder(request):
#     user = request.user
#     orders = DeliveryAssignment.objects.filter(user=user)
#     context = {
#         'orders': orders
#     }
#     return render(request, 'trackmyorder.html', context)


from django.shortcuts import render
from .models import DeliveryAssignment, DeliveryAssignment1

def trackmyorder(request):
    user = request.user
    delivery_assignments = DeliveryAssignment.objects.filter(user=user)
    delivery_assignments1 = DeliveryAssignment1.objects.filter(user=user)
    context = {
        'delivery_assignments': delivery_assignments,
        'delivery_assignments1': delivery_assignments1
    }
    return render(request, 'trackmyorder.html', context)






# from django.shortcuts import render
# from .models import Userpayment  # Import the UserPayment model
# def trackmyorder(request):
#     user = request.user
#     user_payments = Userpayment.objects.filter(user=user)
#     context = {
#         'user_payments': user_payments
#     }
#     return render(request, 'trackmyorder.html', context)





# from .models import DeliveryAssignment, UserProfile

# def ship_order(request):
#     pending_assignments = DeliveryAssignment.objects.filter(status='PENDING')

#     # Fetch corresponding address details
#     addresseswitall = []
#     for assignment in pending_assignments:
#         user_profile = UserProfile.objects.filter(user=assignment.user).first()
#         if user_profile:
#            addresseswitall.append({
#                     'assignment': assignment,
#                     'user_profile': user_profile,
#                 })
#     print(addresseswitall)
    
#     context = {
#         'pending_assignments': addresseswitall ,
#     }
#     return render(request, 'ship_order.html', context)





# def mark_as_shipped(request, assignment_id):
#     if request.method == 'POST':
#         assignment = DeliveryAssignment.objects.get(id=assignment_id)
#         assignment.status = 'SHIPPED'
#         assignment.save()
#     return redirect('ship_order')





from .models import DeliveryAssignment, DeliveryAssignment1, UserProfile

def ship_order(request):
    pending_assignments = DeliveryAssignment.objects.filter(status='PENDING')
    pending_assignments1 = DeliveryAssignment1.objects.filter(status='PENDING')

    addresseswitall = []
    for assignment in pending_assignments:
        user_profile = UserProfile.objects.filter(user=assignment.user).first()
        if user_profile:
            addresseswitall.append({
                'assignment': assignment,
                'type' : "Pet",
                'user_profile': user_profile,
            })

    for assignment1 in pending_assignments1:
        user_profile = UserProfile.objects.filter(user=assignment1.user).first()
        if user_profile:
            addresseswitall.append({
                'assignment': assignment1,
                'type' : "aquarium",
                'user_profile': user_profile,
            })

    context = {
        'pending_assignments': addresseswitall,
    }
    return render(request, 'ship_order.html', context)



# from .models import DeliveryAssignment, DeliveryAssignment1

# def mark_as_shipped(request, assignment_id):
#     if request.method == 'POST':
#         try:
#             assignment = DeliveryAssignment.objects.get(id=assignment_id)
#         except DeliveryAssignment.DoesNotExist:
#             assignment = None
        
#         if not assignment:
#             try:
#                 assignment = DeliveryAssignment1.objects.get(id=assignment_id)
#             except DeliveryAssignment1.DoesNotExist:
#                 assignment = None
        
#         if assignment:
#             assignment.status = 'SHIPPED'
#             assignment.save()
#     return redirect('ship_order')

# from django.shortcuts import get_object_or_404, redirect
# from .models import DeliveryAssignment, DeliveryAssignment1

# def mark_as_shipped(request, assignment_id):
#     if request.method == 'POST':
#         # Try to get the assignment from DeliveryAssignment
#         assignment = DeliveryAssignment.objects.filter(id=assignment_id).first()

#         # If not found in DeliveryAssignment, try DeliveryAssignment1
#         if not assignment:
#             assignment = DeliveryAssignment1.objects.filter(id=assignment_id).first()

#         # If assignment is found, mark it as shipped and redirect
#         if assignment:
#             assignment.status = 'SHIPPED'
#             assignment.save()
#             return redirect('ship_order')

#     # If assignment is not found in any model, return a 404 error
#     return redirect('ship_order')


from django.shortcuts import get_object_or_404, redirect
from .models import DeliveryAssignment, DeliveryAssignment1

def mark_as_shipped(request, assignment_id):
    if request.method == 'POST':
        # Try to get the assignment from DeliveryAssignment
        assignment = DeliveryAssignment.objects.filter(id=assignment_id).first()

        # If not found in DeliveryAssignment, try DeliveryAssignment1
        if not assignment:
            assignment = DeliveryAssignment1.objects.filter(id=assignment_id).first()

        # If assignment is found, mark it as shipped and redirect
        if assignment:
            assignment.status = 'SHIPPED'
            assignment.save()
            return redirect('ship_order')

    # If assignment is not found in any model or request is not POST, return a 404 error
    return redirect('ship_order')  # You can handle this according to your requirements

def mark_as_shipped1(request, assignment_id):
    if request.method == 'POST':
        # Try to get the assignment from DeliveryAssignment
        assignment = DeliveryAssignment1.objects.filter(id=assignment_id).first()

        # If assignment is found, mark it as shipped and redirect
        if assignment:
            assignment.status = 'SHIPPED'
            assignment.save()
            return redirect('ship_order')

    # If assignment is not found in any model or request is not POST, return a 404 error
    return redirect('ship_order')  # You can handle this according to your requirements



def verify_otp(request):
    if request.method == 'POST':
        delivery_assignment_id = request.POST.get('delivery_assignment_id')
        entered_otp = request.POST.get('otp')
        try:
            otp_instance = OTP.objects.get(delivery_assignment_id=delivery_assignment_id)
        except OTP.DoesNotExist:
            return HttpResponse('OTP not found.', status=400)

        if entered_otp == otp_instance.otp:
            delivery_assignment = DeliveryAssignment.objects.get(id=delivery_assignment_id)
            delivery_assignment.status='DELIVERED'
            delivery_assignment.save()
            

           
            # otp_instance.delete()  
            return HttpResponse('Delivery successful!')
        else:
            # OTP doesn't match
            return HttpResponse('Invalid OTP.',status=400)



# def new_orders(request):
#     delivery_boy = request.user.deliveryboy
#     orders = DeliveryAssignment.objects.filter(delivery_boy=delivery_boy,status='SHIPPED')
#     addresses = {}
#     for assignment in orders:
#         # Retrieve the address associated with the user in the delivery assignment
#         address = Address.objects.filter(user=assignment.user).first()
#         if address:
#             addresses[assignment.id] = address

#     context = {
#               'pending_assignments': orders,
#               'addresses': addresses, }
    
#     return render(request,'new_orders.html',context)


# def new_orders(request):
#     delivery_boy = request.user.deliveryman
#     orders = DeliveryAssignment.objects.filter(delivery_boy=delivery_boy, status='SHIPPED')
    
#     # Fetching addresses for the orders
#     addresses = {}
#     for assignment in orders:
#         address = DeliveryAssignment.objects.filter(user=assignment.user).first()
#         if address:
#             addresses[assignment.pk] = address
    
#     context = {
#         'pending_assignments': orders,
#         'addresses': addresses,
#     }
    
#     return render(request, 'out_for_delivery.html', context)

# views.py
# views.py
# views.py
# from django.shortcuts import render
# from .models import DeliveryAssignment, DeliveryMan

# def new_orders(request):
#     delivery_man = DeliveryMan.objects.get(email=request.user.email)
#     orders = DeliveryAssignment.objects.filter(delivery_man=delivery_man, status='SHIPPED')
    
#     # Fetching addresses for the orders
#     addresses = {}
#     for assignment in orders:
#         addresses[assignment.pk] = assignment.user  # Assuming user attribute in DeliveryAssignment model holds UserProfile instance
    
#     context = {
#         'pending_assignments': orders,
#         'addresses': addresses,
#     }
    
#     return render(request, 'out_for_delivery.html', context)


# from django.shortcuts import render
# from .models import DeliveryAssignment, DeliveryMan, UserProfile

# def new_orders(request):
#     # Get the delivery man based on the logged-in user's email
#     delivery_man = DeliveryMan.objects.get(email=request.user.email)

#     # Get the orders assigned to the delivery man with status 'SHIPPED'
#     orders = DeliveryAssignment.objects.filter(delivery_man=delivery_man, status='SHIPPED')

#     context = {
#         'pending_assignments': orders,
#     }

#     return render(request, 'new_orders.html', context)





# from .models import DeliveryAssignment, DeliveryMan, UserProfile, DeliveryAssignment1

# def new_orders(request):
#     # Get the delivery man based on the logged-in user's email
#     delivery_man = DeliveryMan.objects.get(email=request.user.email)

#     # Get the orders assigned to the delivery man with status 'SHIPPED'
#     orders = DeliveryAssignment.objects.filter(delivery_man=delivery_man, status='SHIPPED')
#     orders1 = DeliveryAssignment1.objects.filter(delivery_man=delivery_man, status='SHIPPED')

#     context = {
#         'pending_assignments': orders.union(orders1),
#     }

#     return render(request, 'new_orders.html', context)



# from django.shortcuts import render
# from .models import DeliveryAssignment, DeliveryAssignment1, DeliveryMan
# from django.shortcuts import render
# from .models import DeliveryAssignment, DeliveryAssignment1, UserProfile

# def new_orders(request):
#     # Get the delivery man based on the logged-in user's email
#     delivery_man = DeliveryMan.objects.get(email=request.user.email)

#     # Get the orders assigned to the delivery man with status 'SHIPPED' for DeliveryAssignment (Pets)
#     orders_delivery = DeliveryAssignment.objects.filter(delivery_man=delivery_man, status='SHIPPED')

#     # Get the orders assigned to the delivery man with status 'SHIPPED' for DeliveryAssignment1 (Aquarium)
#     orders_aquarium = DeliveryAssignment1.objects.filter(delivery_man=delivery_man, status='SHIPPED')

#     context = {
#         'pending_assignments_delivery': orders_delivery,
#         'pending_assignments_aquarium': orders_aquarium,
#     }

#     return render(request, 'new_orders.html', context)



from django.shortcuts import render
from .models import DeliveryAssignment, DeliveryAssignment1
from django.db.models import F, Value, IntegerField
from django.db.models import Subquery, OuterRef
def new_orders(request):
    # Get the delivery man based on the logged-in user's email
    delivery_man = DeliveryMan.objects.get(email=request.user.email)

    # Get the orders assigned to the delivery man with status 'SHIPPED' for DeliveryAssignment (Pets)
    orders_delivery = DeliveryAssignment.objects.filter(delivery_man=delivery_man, status='SHIPPED')

    # Get the orders assigned to the delivery man with status 'SHIPPED' for DeliveryAssignment1 (Aquarium)
    orders_aquarium = DeliveryAssignment1.objects.filter(delivery_man=delivery_man, status='SHIPPED')

    # Prepare a list to store the user profiles for each delivery assignment
    user_profiles_delivery = []
    user_profiles_aquarium = []

    # Fetch the related UserProfile objects for all assignments in one go
    user_profiles = UserProfile.objects.filter(user__in=[assignment.user for assignment in orders_delivery])
    # Now iterate through the orders_delivery queryset and assign the userprofile attribute to each assignment
    order_delivery = []
    for assignment in orders_delivery:
        # Find the corresponding UserProfile object for the current assignment
        user_profile = user_profiles.get(user=assignment.user)
        # Assign the userprofile attribute to the current assignment

    print()
    # # Iterate through each delivery assignment to get the related user profile
    # for assignment in orders_delivery:
    #     assignment = assignment.annotate(
    #         userprofile = Subquery(UserProfile.objects.get(
    #             user=assignment.user
    #         ))
    #     )
        # user_profile = UserProfile.objects.get(user=assignment.user)
        # user_profiles_delivery.append(user_profile)

    for assignment in orders_aquarium:
        user_profile = assignment.user
        user_profiles_aquarium.append(user_profile) 

    print(user_profiles_delivery)
    context = {
        'pending_assignments_delivery': orders_delivery,
        'pending_assignments_aquarium': orders_aquarium,
        'user_profiles' :user_profiles,
        'user_profiles_delivery': user_profiles_delivery,
        'user_profiles_aquarium': user_profiles_aquarium,
    }

    return render(request, 'new_orders.html', context)


# def new_orders(request):
#     # Get the delivery man based on the logged-in user's email
#     delivery_man = DeliveryMan.objects.get(email=request.user.email)

#     # Get the orders assigned to the delivery man with status 'SHIPPED' for pets
#     orders_pets = DeliveryAssignment.objects.filter(delivery_man=delivery_man, status='SHIPPED')

#     # Get the orders assigned to the delivery man with status 'SHIPPED' for aquarium
#     orders_aquarium = DeliveryAssignment1.objects.filter(delivery_man=delivery_man, status='SHIPPED')

#     context = {
#         'pending_assignments_delivery': orders_pets,
#         'pending_assignments_aquarium': orders_aquarium,
#     }

#     return render(request, 'new_orders.html', context)





from django.shortcuts import render
from .models import DeliveryAssignment, DeliveryMan,DeliveryOTP






# # # views.py
# import random
# from django.contrib.auth.models import User
# from .models import DeliveryAssignment, DeliveryMan
# from django.http import HttpResponse
# from django.shortcuts import render
# from .models import DeliveryAssignment, DeliveryOTP

# def out_for_delivery(request):
#     # Get the delivery man based on the logged-in user's email
#     user = request.user
#     try:
#         delivery_man = DeliveryMan.objects.get(email=user.email)
#     except DeliveryMan.DoesNotExist:
#         # Handle the case if the user is not a deliveryman
#         return HttpResponse("Unauthorized access")

#     # Filter orders assigned to the delivery man with status 'OUT'
#     orders = DeliveryAssignment.objects.filter(delivery_man=delivery_man, status='OUT')

#     addresses = {}
#     for assignment in orders:
#         # Retrieve the address associated with the user in the delivery assignment
#         address = UserProfile.objects.filter(user=assignment.user).first()
#         if address:
#             addresses[assignment.id] = address

#     context = {
#         'pending_assignments': orders,
#         'addresses': addresses
#     }

#     if request.method == 'POST':
#         # Generate 6-digit OTP
#         otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

#         # Send email to customer
#         delivery_assignment_id = request.POST.get('delivery_assignment_id')
#         delivery_assignment = DeliveryAssignment.objects.get(pk=delivery_assignment_id)
#         customer_email = delivery_assignment.user.email
#         product_name = delivery_assignment.product

#         message = f'Your {product_name} is out for delivery.'
#         send_mail(
#             'Your Order is Out for Delivery',
#             f'Your {product_name} is out for delivery. Your OTP is: {otp}',
#             'roshangeorge2k66@gmail.com',  # Sender's email
#             [customer_email],  # List of recipient emails
#             fail_silently=False,
#         )

#         # Store OTP in the database
#         otp_instance = DeliveryOTP.objects.create(assignment=delivery_assignment, otp=otp)
#         # delivery_assignment.status = 'OUT'
#         delivery_assignment.save() 

#         return render(request, 'out_for_delivery.html', {'otp_sent': True})
#     else:
#         return render(request, 'out_for_delivery.html', context)


# from django.shortcuts import render
# from .models import DeliveryAssignment, DeliveryOTP, DeliveryMan, UserProfile

# def out_for_delivery(request):
#     # Assuming delivery man is authenticated and fetched properly
#     delivery_man = DeliveryMan.objects.get(email=request.user.email)

#     # Retrieve pending delivery assignments for the current delivery man
#     pending_assignments = DeliveryAssignment.objects.filter(delivery_man=delivery_man, status='OUT')

#     context = {
#         'pending_assignments': pending_assignments,
#     }

#     if request.method == 'POST':
#         # Assuming you're sending OTPs as described earlier
#         # Generate OTP, send email, and save OTP in the database
#         # Once the delivery status is updated, set status to 'OUT'
#         # Update the assignment status to 'OUT'
#         delivery_assignment_id = request.POST.get('delivery_assignment_id')
#         delivery_assignment = DeliveryAssignment.objects.get(pk=delivery_assignment_id)
#         otp = generate_otp()  # You need to implement a function to generate OTP
#         DeliveryOTP.objects.create(assignment=delivery_assignment, otp=otp)
#         delivery_assignment.status = 'OUT'
#         delivery_assignment.save()

#         # You can add a success message or any other logic you need
#         return render(request, 'out_for_delivery.html', {'otp_sent': True})
#     else:
#         return render(request, 'out_for_delivery.html', context)




#latest
# from django.shortcuts import render
# from .models import DeliveryAssignment, DeliveryOTP, DeliveryMan, UserProfile,DeliveryOTP1

# def out_for_delivery(request):
#     # Assuming delivery man is authenticated and fetched properly
#     delivery_man = DeliveryMan.objects.get(email=request.user.email)

#     # Retrieve pending delivery assignments for the current delivery man
#     pending_assignments = DeliveryAssignment.objects.filter(delivery_man=delivery_man, status='OUT')

#     context = {
#         'pending_assignments': pending_assignments,
#     }

#     if request.method == 'POST':
#         # Assuming you're sending OTPs as described earlier
#         # Generate OTP, send email, and save OTP in the database
#         # Once the delivery status is updated, set status to 'OUT'
#         # Update the assignment status to 'OUT'
#         delivery_assignment_id = request.POST.get('delivery_assignment_id')
#         delivery_assignment = DeliveryAssignment.objects.get(pk=delivery_assignment_id)
#         otp = generate_otp()  # You need to implement a function to generate OTP
#         DeliveryOTP.objects.create(assignment=delivery_assignment, otp=otp)
#         delivery_assignment.status = 'OUT'
#         delivery_assignment.save()

#         # You can add a success message or any other logic you need
#         return render(request, 'out_for_delivery.html', {'otp_sent': True})
#     else:
#         return render(request, 'out_for_delivery.html', context)


# from .models import DeliveryAssignment1

# def out_for_deliveryaq(request):
#     # Assuming delivery man is authenticated and fetched properly
#     delivery_man = DeliveryMan.objects.get(email=request.user.email)

#     # Retrieve pending delivery assignments for the current delivery man
#     pending_assignmentss = DeliveryAssignment1.objects.filter(delivery_man=delivery_man, status='OUT')

#     context = {
#         'pending_assignmentss': pending_assignmentss,
#     }

#     if request.method == 'POST':
#         # Assuming you're sending OTPs as described earlier
#         # Generate OTP, send email, and save OTP in the database
#         # Once the delivery status is updated, set status to 'OUT'
#         # Update the assignment status to 'OUT'
#         delivery_assignment_id = request.POST.get('delivery_assignment_id')
#         delivery_assignment = DeliveryAssignment1.objects.get(pk=delivery_assignment_id)
#         otp = generate_otp()  # You need to implement a function to generate OTP
#         DeliveryOTP1.objects.create(assignment=delivery_assignment, otp=otp)
#         delivery_assignment.status = 'OUT'
#         delivery_assignment.save()

#         # You can add a success message or any other logic you need
#         return render(request, 'out_for_delivery.html', {'otp_sent': True})
#     else:
#         return render(request, 'out_for_delivery.html', context)
    




# from django.shortcuts import render
# from .models import DeliveryAssignment, DeliveryAssignment1

# def out_for_delivery(request):
#     # Assuming delivery man is authenticated and fetched properly
#     delivery_man = DeliveryMan.objects.get(email=request.user.email)

#     # Retrieve pending delivery assignments for the current delivery man
#     pending_assignments = DeliveryAssignment.objects.filter(delivery_man=delivery_man, status='OUT')

#     context = {
#         'pending_assignments': pending_assignments,
#     }

#     if request.method == 'POST':
#         # Assuming you're sending OTPs as described earlier
#         # Generate OTP, send email, and save OTP in the database
#         # Once the delivery status is updated, set status to 'OUT'
#         # Update the assignment status to 'OUT'
#         delivery_assignment_id = request.POST.get('delivery_assignment_id')
#         delivery_assignment = DeliveryAssignment.objects.get(pk=delivery_assignment_id)
#         otp = ''.join ([str(random.randint(0,9)) for _ in range(6)]) # You need to implement a function to generate OTP
#         DeliveryOTP.objects.create(assignment=delivery_assignment, otp=otp)
#         customer_email = delivery_assignment.user.email
#         delivery_assignment.status = 'OUT'
#         message = f'Your  is out for delivery.'
#         # Notification.objects.create(user=delivery_assignment.user, message=message)
#         send_mail(
#             'Your Order is Out for Delivery',
#             f'Your product is out for delivery. Your OTP is: {otp}',
#             'roshangeorge2k66@gmail.com',  # Sender's email
#             [customer_email],  # List of recipient emails
#             fail_silently=False,
#         )

#         # Store OTP in the database
#         otp_instance = otp.objects.create(delivery_assignment=delivery_assignment, otp=otp)
#         delivery_assignment.status='OUT'
#         delivery_assignment.save()

#         # You can add a success message or any other logic you need
#         return render(request, 'out_for_delivery.html', {'otp_sent': True})
#     else:
#         return render(request, 'out_for_delivery.html', context)

from django.shortcuts import render
from .models import DeliveryAssignment, DeliveryOTP  # Import DeliveryOTP model
import random
from django.core.mail import send_mail

def out_for_delivery(request):
    # Assuming delivery man is authenticated and fetched properly
    delivery_man = DeliveryMan.objects.get(email=request.user.email)

    # Retrieve pending delivery assignments for the current delivery man
    pending_assignments = DeliveryAssignment.objects.filter(delivery_man=delivery_man, status='OUT')

    context = {
        'pending_assignments': pending_assignments,
    }

    if request.method == 'POST':
        # Assuming you're sending OTPs as described earlier
        # Generate OTP, send email, and save OTP in the database
        # Once the delivery status is updated, set status to 'OUT'
        # Update the assignment status to 'OUT'
        delivery_assignment_id = request.POST.get('delivery_assignment_id')
        delivery_assignment = DeliveryAssignment.objects.get(pk=delivery_assignment_id)
        generated_otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate OTP
        DeliveryOTP.objects.create(assignment=delivery_assignment, otp=generated_otp)  # Create DeliveryOTP object
        customer_email = delivery_assignment.user.email
        delivery_assignment.status = 'OUT'
        message = f'Your order is out for delivery.'
        # Notification.objects.create(user=delivery_assignment.user, message=message)
        send_mail(
            'Your Order is Out for Delivery',
            f'Your product is out for delivery. Your OTP is: {generated_otp}',
            'roshangeorge2k66@gmail.com',  # Sender's email
            [customer_email],  # List of recipient emails
            fail_silently=False,
        )

        # Update the assignment status to 'OUT'
        delivery_assignment.status = 'OUT'
        delivery_assignment.save()

        # You can add a success message or any other logic you need
        return render(request, 'out_for_delivery.html', {'otp_sent': True})
    else:
        return render(request, 'out_for_delivery.html', context)

    



# def verify_otp(request):
#      if request.method == 'POST':
#         delivery_assignment_id = request.POST.get('delivery_assignment_id')
#         entered_otp = request.POST.get('otp')
#         try:
#             otp_instance = otp.objects.get(delivery_assignment_id=delivery_assignment_id)
#         except otp.DoesNotExist:
#             return HttpResponse('OTP not found.', status=400)

#         if entered_otp == otp_instance.otp:
#             delivery_assignment = DeliveryAssignment.objects.get(id=delivery_assignment_id)
#             delivery_assignment.status='DELIVERED'
#             delivery_assignment.save()
            

           
#             # otp_instance.delete()  
#             return HttpResponse('Delivery successful!')
#         else:
#             # OTP doesn't match
#             return HttpResponse('Invalid OTP.', status=400)


from django.shortcuts import HttpResponse
from .models import DeliveryOTP, DeliveryAssignment
from django.contrib import messages

def verify_otp(request):
    if request.method == 'POST':
        delivery_assignment_id = request.POST.get('delivery_assignment_id')
        print (delivery_assignment_id)
        entered_otp = request.POST.get('otp')
        try:
            otp_instance = DeliveryOTP.objects.filter(assignment_id=delivery_assignment_id).first()
        except DeliveryOTP.DoesNotExist:
            #return HttpResponse('OTP not found.', status=400)
            messages.error(request, 'This is an error message.')
            return redirect('out_for_delivery')
        if entered_otp == otp_instance.otp:
            try:
                delivery_assignment = DeliveryAssignment.objects.get(id=delivery_assignment_id)
            except DeliveryAssignment.DoesNotExist:
                # return HttpResponse('Delivery assignment not found.', status=400)
                messages.success(request, 'Delivery assignment not found..')
                return redirect('out_for_delivery')

            if delivery_assignment.status != 'OUT':
                # return HttpResponse('Delivery assignment is not out for delivery.', status=400)
                return redirect('out_for_delivery')
            delivery_assignment.status = 'DELIVERED'
            delivery_assignment.save()
            
            otp_instance.delete()  # Delete OTP after successful verification
            messages.success(request, 'Delivery successful!')
            # return HttpResponse('Delivery successful!')
            return redirect('out_for_delivery')
        else:
            # OTP doesn't match
            messages.error(request, 'Invalid OTP.')
            return redirect('out_for_delivery')
            # return HttpResponse('Invalid OTP.', status=400)


from django.shortcuts import render
from .models import DeliveryMan, DeliveryAssignment1, DeliveryOTP1

from django.shortcuts import render
from .models import DeliveryAssignment1
# from .utils import generate_otp  # Assuming you have a function to generate OTP in utils.py

from django.shortcuts import render
from .models import DeliveryAssignment1
# from .utils import generate_otp  # Assuming you have a function to generate OTP in utils.py

def out_for_deliveryaq(request):
    # Assuming delivery man is authenticated and fetched properly
    delivery_man = DeliveryMan.objects.get(email=request.user.email)

    # Retrieve pending delivery assignments for the current delivery man
    pending_assignments = DeliveryAssignment1.objects.filter(delivery_man=delivery_man, status='OUT')

    context = {
        'pending_assignments': pending_assignments,
    }

    if request.method == 'POST':
        # Assuming you're sending OTPs as described earlier
        # Generate OTP, send email, and save OTP in the database
        # Once the delivery status is updated, set status to 'OUT'
        # Update the assignment status to 'OUT'
        delivery_assignment_id = request.POST.get('delivery_assignment_id')
        delivery_assignment = DeliveryAssignment1.objects.get(pk=delivery_assignment_id)
        # otp = generate_otp()  # You need to implement a function to generate OTP
        DeliveryOTP1.objects.create(assignment=delivery_assignment)
        delivery_assignment.status = 'OUT'
        delivery_assignment.save()

        # You can add a success message or any other logic you need
        context['otp_sent'] = True

    return render(request, 'out_for_deliveryaq.html', context)











def mark_as_shipped(request, assignment_id):
    if request.method == 'POST':
        assignment = DeliveryAssignment.objects.get(id=assignment_id)
        assignment.status = 'SHIPPED'
        assignment.save()
    return redirect('ship_order')


# from django.shortcuts import get_object_or_404, redirect
# from .models import DeliveryAssignment, DeliveryAssignment1

# def mark_as_shipped(request, assignment_id):
#     if request.method == 'POST':
#         try:
#             # Try to get the DeliveryAssignment object
#             assignment = DeliveryAssignment1.objects.get(id=assignment_id)
#         except DeliveryAssignment1.DoesNotExist:
#             try:
#                 # If DeliveryAssignment doesn't exist, try to get DeliveryAssignment1 object
#                 assignment = DeliveryAssignment1.objects.get(id=assignment_id)
#             except DeliveryAssignment1.DoesNotExist:
#                 # If neither DeliveryAssignment nor DeliveryAssignment1 exist, return a 404 error
#                 return redirect('page_not_found')

#         # If either assignment is found, mark it as shipped
#         assignment.status = 'SHIPPED'
#         assignment.save()

#     return redirect('ship_order')










# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .models import DeliveryAssignment, DeliveryAssignment1, DeliveryMan

# def out_for_delivery(request):
#     # Assuming delivery man is authenticated and fetched properly
#     delivery_man = DeliveryMan.objects.get(email=request.user.email)

#     # Retrieve pending delivery assignments for Pets and Aquariums
#     pending_assignments_pets = DeliveryAssignment.objects.filter(delivery_man=delivery_man, status='OUT')
#     pending_assignments_aquariums = DeliveryAssignment1.objects.filter(delivery_man=delivery_man, status='OUT')

#     context = {
#         'pending_assignments_pets': pending_assignments_pets,
#         'pending_assignments_aquariums': pending_assignments_aquariums,
#     }

#     if request.method == 'POST':
#         # Handle POST request (generating OTP, updating status, etc.)
#         delivery_assignment_id = request.POST.get('delivery_assignment_id')
#         assignment_type = request.POST.get('assignment_type')

#         if delivery_assignment_id and assignment_type:
#             try:
#                 if assignment_type == 'pet':
#                     assignment = DeliveryAssignment.objects.get(pk=delivery_assignment_id)
#                 elif assignment_type == 'aquarium':
#                     assignment = DeliveryAssignment1.objects.get(pk=delivery_assignment_id)
                
#                 # Implement logic to generate OTP, update status, etc.
#                 # For now, just mark the assignment as delivered
#                 assignment.status = 'DELIVERED'
#                 assignment.save()

#                 return HttpResponse("Assignment marked as delivered successfully")
#             except (DeliveryAssignment.DoesNotExist, DeliveryAssignment1.DoesNotExist):
#                 return HttpResponse("Invalid assignment ID")
#         else:
#             return HttpResponse("Invalid request")

#     else:
#         return render(request, 'out_for_delivery.html', context)





# import random
# def generate_otp():
#     # Generate a random 6-digit OTP
#       return ''.join([str(random.randint(0, 9)) for _ in range(6)])


# def generate_otp(request):
#     if request.method == 'POST':
#         out_for_delivery = request.POST.get('out_for_delivery')
#         email = request.POST.get('email')

#         # Generate OTP
#         otp = ''.join(random.choices(string.digits, k=6))

#         # Send email with OTP
#         send_mail(
#             'Your OTP for Delivery',
#             f'Your OTP for the delivery is: {otp}',
#             'roshangeorge2k66@gmail.com',  # Replace with your sender email
#             [email],
#             fail_silently=False,
#         )

#         # Save OTP to database with the correct assignment_id
#         otp_instance = DeliveryOTP.objects.create(
#             otp=otp,
#             assignment_id=out_for_delivery,
#         )

#         assignment = DeliveryAssignment.objects.get(id=out_for_delivery)
#         assignment.status = 'OUT_FOR_DELIVERY'
#         assignment.save()

#         return redirect('out_for_delivery')


#         # Save OTP to database
#         otp_instance = DeliveryOTP.objects.create(
#             otp=otp,
#             assignment_id=out_for_delivery,  # Replace with the correct assignment ID
#         )

#         assignment = DeliveryAssignment.objects.get(id=out_for_delivery)
#         assignment.status = 'OUT_FOR_DELIVERY'
#         assignment.save()

#         return redirect('out_for_delivery')



