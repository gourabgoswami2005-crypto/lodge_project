from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from .models import RoomType, Reservation, Offer
from .forms import RoomTypeForm, OfferForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def is_admin_user(user):
    return user.is_authenticated and user.is_superuser


def home_view(request):
    rooms = RoomType.objects.filter(is_available=True)
    offers = Offer.objects.filter(is_active=True)
    return render(request, 'home.html', {
        'rooms': rooms,
        'offers': offers,
    })


def booking_view(request):
    rooms = RoomType.objects.filter(is_available=True)
    return render(request, 'booking.html', {'rooms': rooms})


@user_passes_test(is_admin_user, login_url='signin')
def manage_lodge_view(request):
    room_form = RoomTypeForm(prefix='room')
    offer_form = OfferForm(prefix='offer')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'add_room':
            room_form = RoomTypeForm(request.POST, prefix='room')
            if room_form.is_valid():
                room_form.save()
                messages.success(request, 'New room type and price added!')
                return redirect('manage_lodge')

        elif form_type == 'add_offer':
            offer_form = OfferForm(request.POST, prefix='offer')
            if offer_form.is_valid():
                offer_form.save()
                messages.success(request, 'New offer added!')
                return redirect('manage_lodge')

    rooms = RoomType.objects.all()
    offers = Offer.objects.all()

    return render(request, 'manage.html', {
        'room_form': room_form,
        'offer_form': offer_form,
        'rooms': rooms,
        'offers': offers,
    })


@csrf_exempt  # <-- Add this decorator to disable CSRF blocking for API POST requests
def book_room_api(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            check_in_str = data.get('checkInDate')
            check_out_str = data.get('checkOutDate')
            room_type = data.get('roomType')
            user_email = data.get('emailId')
            full_name = data.get('fullName')

            if not check_in_str or not check_out_str or not room_type:
                return JsonResponse({'status': 'error', 'message': 'Missing required booking fields.'}, status=400)

            d1 = datetime.strptime(check_in_str, '%Y-%m-%d')
            d2 = datetime.strptime(check_out_str, '%Y-%m-%d')
            nights = (d2 - d1).days

            if nights <= 0:
                return JsonResponse({'status': 'error', 'message': 'Invalid stay duration. Check-out must be after check-in.'}, status=400)

            try:
                room = RoomType.objects.get(name=room_type, is_available=True)
            except RoomType.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Selected room type does not exist.'}, status=400)

            total_price = float(room.price_per_night) * nights

            reservation = Reservation.objects.create(
                full_name=full_name,
                mobile_number=data.get('mobileNumber'),
                aadhaar_card=data.get('aadhaarCard', '').strip(),
                email_id=user_email,
                voter_card=data.get('voterCard', ''),
                check_in_date=check_in_str,
                check_out_date=check_out_str,
                adults=int(data.get('adults', 2)),
                children=int(data.get('children', 0)),
                room_type=room_type,
                ac_preference=data.get('acPreference', 'AC'),
                total_price=total_price
            )

            # --- SEND EMAIL NOTIFICATION FOR BOOKING ---
            if user_email:
                try:
                    # Email to User
                    send_mail(
                        subject=f'Booking Confirmation #{reservation.id} - Mountain Retreat Lodge',
                        message=f'Dear {full_name},\n\nYour reservation for {room_type} from {check_in_str} to {check_out_str} has been confirmed!\nTotal Price: ₹{total_price}\n\nThank you for booking with us!',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user_email],
                    )
                    # Email to Admin
                    send_mail(
                        subject=f'[New Reservation #{reservation.id}]',
                        message=f'A new booking was made!\nGuest: {full_name}\nEmail: {user_email}\nRoom: {room_type}\nCheck-In: {check_in_str}\nCheck-Out: {check_out_str}\nTotal: ₹{total_price}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.ADMIN_EMAIL],
                    )
                except Exception as e:
                    print(f"Booking email error: {e}")

            return JsonResponse({
                'status': 'success',
                'booking_id': reservation.id,
                'total_price': total_price
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid HTTP method'}, status=405)


# user login/signup

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return redirect('signup')

        # Create user using email as the username for clean login handling
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()

        # --- SEND EMAIL NOTIFICATION FOR SIGN UP ---
        try:
            # Email to User
            send_mail(
                subject='Welcome to Mountain Retreat Lodge!',
                message=f'Hello {name},\n\nYour account has been successfully created using {email}.\n\nThank you for joining us!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            # Email to Admin
            send_mail(
                subject='[New User Registration]',
                message=f'A new user has registered:\nName: {name}\nEmail: {email}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
            )
        except Exception as e:
            print(f"Signup email error: {e}")

        messages.success(request, 'Account created successfully! Please sign in.')
        return redirect('signin')

    return render(request, 'signup.html')


def signin_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate using email as the username
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # --- SEND EMAIL NOTIFICATION FOR LOGIN ---
            try:
                # Email to User
                send_mail(
                    subject='Login Alert - Mountain Retreat Lodge',
                    message=f'Hello {user.first_name},\n\nWe noticed a successful login to your account from email: {email}.\nTime: {datetime.now()}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )
                # Email to Admin
                send_mail(
                    subject='[User Login Activity]',
                    message=f'User logged into their account:\nEmail: {email}\nTime: {datetime.now()}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                )
            except Exception as e:
                print(f"Login email error: {e}")

            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('signin')

    return render(request, 'signin.html')


def logout_view(request):
    logout(request)
    return redirect('home')