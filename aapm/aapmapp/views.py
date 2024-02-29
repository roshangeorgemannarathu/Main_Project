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

    # Render the template with the updated pet and aquarium status
    return render(request, 'customer_account.html', {'pets': pets, 'aquariums': aquariums})

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

def purchase_item(request):
    if request.method == 'POST':
        # Handle the purchase logic here
        # For example, you can process the purchase and redirect the user to a thank you page
        return redirect('thank_you_page')  # Replace 'thank_you_page' with the actual URL name for your thank you page
    else:
        # Handle GET requests (optional)
        pass

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
        # Assuming you have a form to add items to the cart
        # Retrieve item data from the form submission
        item_id = request.POST.get('item_id')
        item_category = request.POST.get('item_category')
        quantity = int(request.POST.get('quantity'))
        
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


def pet_details(request, pet_id):
    request.session['pet_id'] = pet_id
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
    return render(request, 'pet_details.html', context=context)




from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
 
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Pet
from django.utils import timezone



@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)

            pet_id = request.session.pop('pet_id', None)
            pet = get_object_or_404(Pet, id=pet_id)
            pet.status = "inactive"  # Set the status to "inactive"
            pet.save()

            if result is not None:
                try:
                    # Save payment details to Userpayment table
                    current_datetime = timezone.now()
                    user_payment_instance = Userpayment.objects.create(
                        user=request.user,  # Adjust as per your user model
                        cart=1,  # Adjust as per your requirement
                        amount=pet.price,
                        datetime=current_datetime,
                        order_id_data=razorpay_order_id,
                        payment_id_data=payment_id,
                        item=pet 
                    )
                    # render success page on successful capture of payment
                    return render(request, 'payment_success.html')
                except Exception as e:
                    # Log the exception or handle it as appropriate
                    print(e)  # Print the exception for debugging
                    return HttpResponse("fail: {}".format(str(e)))
            else:
                # if signature verification fails.
                return HttpResponse("signature fail")
        except Exception as e:
            # if we don't find the required parameters in POST data
            print(e)  # Print the exception for debugging
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()
# 


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import razorpay


def aquarium_details(request, aquarium_id):
    request.session['item_id'] = aquarium_id
    request.session['item_type'] = 'aquarium'

    aquarium = get_object_or_404(Aquarium, id=aquarium_id)
    currency = 'INR'

    # Ensure amount is at least 100 paise (1 INR)
    amount = max(int(math.ceil(aquarium.price * 100)), 100)

    # Ensure amount is a multiple of 100 paise
    amount = (amount // 100) * 100

    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler1/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['aquarium'] = aquarium
    return render(request, 'aquarium_details.html', context=context)


@csrf_exempt
def paymenthandler1(request):
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)

            item_id = request.session.pop('item_id', None)
            item_type = request.session.pop('item_type', None)

            if result is not None:
                try:
                    current_datetime = timezone.now()
                    if item_type == 'pet':
                        item = get_object_or_404(Pet, id=item_id)
                    elif item_type == 'aquarium':
                        item = get_object_or_404(Aquarium, id=item_id)
                    else:
                        # Handle invalid item type
                        return HttpResponseBadRequest("Invalid item type")

                    # Save payment details to Userpayment_aquarium table
                    user_payment_instance = Userpayment_aquarium.objects.create(
                        user=request.user,
                        cart=1,
                        amount=item.price,
                        datetime=current_datetime,
                        order_id_data=razorpay_order_id,
                        payment_id_data=payment_id,
                        item=item  # Associate the payment with the correct item
                    )
                    # render success page on successful capture of payment
                    return render(request, 'payment_success.html')
                except Exception as e:
                    # Log the exception or handle it as appropriate
                    print(e)
                    return HttpResponse("fail: {}".format(str(e)))
            else:
                # if signature verification fails.
                return HttpResponse("signature fail")
        except Exception as e:
            # if we don't find the required parameters in POST data
            print(e)
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()














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
    
def deliveryman_account(request):
    # Your view logic here
     return render(request, 'deliveryman_account.html')
    
   

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
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        full_name = user_profile.fullname
        if user_profile.photo:
            photo_url = user_profile.photo.url
        else:
            # Provide a default photo URL or handle it accordingly
            photo_url = '/path/to/default/photo.jpg'  # Adjust this path as needed
    except UserProfile.DoesNotExist:
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

# def add_delivery_man(request):
    
#     return render(request, 'add_delivery_man.html')





# def add_delivery_man(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         house_name = request.POST.get('house_name')
#         district = request.POST.get('district')
#         city = request.POST.get('city')
#         pincode = request.POST.get('pincode')
#         vehicle_type = request.POST.get('vehicle_type')
#         vehicle_no = request.POST.get('vehicle_no')

        

#         # Create delivery man instance
#         delivery_man = DeliveryMan.objects.create(
#             name=name,
#             email=email,
#             phone=phone,
#             house_name=house_name,
#             district=district,
#             city=city,
#             pincode=pincode,
#             vehicle_type=vehicle_type,
#             vehicle_no=vehicle_no
#         )
    
#         # Redirect to a success page after saving the delivery man
#         return redirect('Delivery_successfully_registerd')  # Provide the name of your success URL

#     return render(request, 'add_delivery_man.html')


# from django.shortcuts import render, redirect
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.conf import settings
# import threading
# import random  # Import the random module
# import string

# def add_delivery_man(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         house_name = request.POST.get('house_name')
#         district = request.POST.get('district')
#         city = request.POST.get('city')
#         pincode = request.POST.get('pincode')
#         vehicle_type = request.POST.get('vehicle_type')
#         vehicle_no = request.POST.get('vehicle_no')

#         # Generate random password
#         random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

#         try:
#             # Create delivery man instance
#             # Create delivery man instance
#             user = dealer.objects.create_user(
            
#                 username=email,
#                 email=email,
#                 password=random_password,
#                 role='deliveryman'  # Assuming 'deliveryman' is a string representing the role
#             )
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
            
#             # Send email to the deliveryman
#             subject = 'Welcome to the Delivery Service'
#             message = f"Hello {name},\n\nWelcome to the Delivery Service. Your login credentials are:\nUsername: {email}\nPassword: {random_password}\n\nLogin here: [http://127.0.0.1:8000/]\n\nThank you."
#             send_mail(subject, message, 'your_email@example.com', [email])

#             # Redirect to a success page after saving the delivery man
#             return redirect('Delivery_successfully_registerd')  # Provide the name of your success URL

#         except Exception as e:
#             # Handle any exceptions
#             print(f"Error: {e}")
#             # Redirect to an error page or display an error message
#             return redirect('Delivery_successfully_registerd') 

#     return render(request, 'add_delivery_man.html')

import csv
import traceback
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from .models import DeliveryMan
import random
import string

def add_delivery_man(request):
    if request.method == 'POST':
        if 'csvFile' in request.FILES:  # If CSV file is uploaded
            try:
                csv_file = request.FILES['csvFile']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    try:
                        print("Reading CSV row:", row)  # Print the row being read
                        delivery_man = DeliveryMan.objects.create(
                            name=row['name'],
                            email=row['email'],
                            phone=row['phone'],
                            house_name=row['house_name'],
                            district=row['district'],
                            city=row['city'],
                            pincode=row['pincode'],
                            vehicle_type=row['vehicle_type'],
                            vehicle_no=row['vehicle_no']
                        )
                        print("Delivery man created:", delivery_man)  # Print the created delivery man object
                    except Exception as e:
                        print("Error creating delivery man:", e)  # Print any error that occurs during creation
                        traceback.print_exc()  # Print the traceback for detailed error information
                        error_message = str(e)
                        return render(request, 'add_delivery_man.html', {'error_message': error_message})
                return redirect('Delivery_successfully_registerd')  # Redirect to success page after all data is inserted
            except Exception as e:
                print("Error processing CSV file:", e)  # Print any error that occurs during CSV processing
                traceback.print_exc()  # Print the traceback for detailed error information
                error_message = str(e)
                return render(request, 'add_delivery_man.html', {'error_message': error_message})
        else:  # If form submission
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            house_name = request.POST.get('house_name')
            district = request.POST.get('district')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            vehicle_type = request.POST.get('vehicle_type')
            vehicle_no = request.POST.get('vehicle_no')

            # Generate random password
            random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            try:
                # Create user and delivery man instances
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=random_password,
                    role='deliveryman'  # Assuming 'deliveryman' is a string representing the role
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

                # Send email to the deliveryman
                subject = 'Welcome to the Delivery Service'
                message = f"Hello {name},\n\nWelcome to the Delivery Service. Your login credentials are:\nUsername: {email}\nPassword: {random_password}\n\nLogin here: [http://127.0.0.1:8000/]\n\nThank you."
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

                # Redirect to a success page after saving the delivery man
                return redirect('Delivery_successfully_registerd')  # Provide the name of your success URL

            except Exception as e:
                # Handle any exceptions
                print("Error creating delivery man:", e)  # Print any error that occurs during creation
                traceback.print_exc()  # Print the traceback for detailed error information
                error_message = str(e)
                # Render the form page with the error message
                return render(request, 'add_delivery_man.html', {'error_message': error_message})

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
