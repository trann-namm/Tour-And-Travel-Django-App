from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from decimal import Decimal
import uuid
import datetime

from .forms import *
from .models import (
    Flight,
    Hotel,
    TouristAttraction,
    FlightBooking,
    HotelBooking,
    City,
    PackageBooking,
    Airline,
    BookingPayment,
)


def IndexView(request):
    """Homepage view with quick search forms"""
    flight_form = FlightSearchForm()
    hotel_form = HotelSearchForm()

    # Get featured content
    featured_cities = City.objects.all()[:6]
    popular_attractions = TouristAttraction.objects.all()[:8]

    context = {
        "flight_form": flight_form,
        "hotel_form": hotel_form,
        "featured_cities": featured_cities,
        "popular_attractions": popular_attractions,
    }
    return render(request, "index.html", context)


def PackageView(request):
    """Package search and booking view"""
    form = FlightSearchForm()

    if request.method == "POST":
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            source_city = form.cleaned_data["source_city"]
            destination_city = form.cleaned_data["destination_city"]
            departure_date = form.cleaned_data["departure_date"]
            passengers = form.cleaned_data["passengers"]
            travel_class = form.cleaned_data["travel_class"]

            # Search for flights
            flights = Flight.objects.filter(
                source_city=source_city,
                destination_city=destination_city,
                flight_date=departure_date,
                available_seats__gte=passengers,
                status="SCHEDULED",
            ).select_related("airline", "source_city", "destination_city")

            # Search for hotels in destination city
            hotels = Hotel.objects.filter(
                city=destination_city, available_rooms__gt=0
            ).select_related("city")

            # Get tourist attractions
            attractions = TouristAttraction.objects.filter(city=destination_city)[:6]

            context = {
                "form": form,
                "flights": flights,
                "hotels": hotels,
                "attractions": attractions,
                "search_performed": True,
                "source_city": source_city,
                "destination_city": destination_city,
                "departure_date": departure_date,
                "passengers": passengers,
                "travel_class": travel_class,
            }
            return render(request, "package.html", context)

    return render(request, "package.html", {"form": form})


def registerView(request):
    """User registration view"""
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Registration successful! Welcome to our travel platform."
            )
            return redirect("dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()

    return render(request, "registration/register.html", {"form": form})


def HotelView(request):
    """Hotel search view"""
    form = HotelSearchForm()
    hotels = None

    if request.method == "POST":
        form = HotelSearchForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data["city"]
            check_in_date = form.cleaned_data["check_in_date"]
            check_out_date = form.cleaned_data["check_out_date"]
            guests = form.cleaned_data["guests"]
            rooms = form.cleaned_data["rooms"]
            min_rating = form.cleaned_data.get("min_rating")
            max_price = form.cleaned_data.get("max_price")

            # Build query
            hotels = Hotel.objects.filter(
                city=city, available_rooms__gte=rooms
            ).select_related("city")

            if min_rating:
                hotels = hotels.filter(star_rating__gte=min_rating)

            if max_price:
                hotels = hotels.filter(price_per_night__lte=max_price)

            hotels = hotels.order_by("-star_rating", "price_per_night")

            # Pagination
            paginator = Paginator(hotels, 12)
            page_number = request.GET.get("page")
            hotels = paginator.get_page(page_number)

    context = {
        "form": form,
        "hotels": hotels,
        "search_performed": hotels is not None,
    }
    return render(request, "hotels.html", context)


def FlightView(request):
    """Flight search view"""
    form = FlightSearchForm()
    flights = None

    if request.method == "POST":
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            source_city = form.cleaned_data["source_city"]
            destination_city = form.cleaned_data["destination_city"]
            departure_date = form.cleaned_data["departure_date"]
            passengers = form.cleaned_data["passengers"]
            travel_class = form.cleaned_data["travel_class"]

            flights = (
                Flight.objects.filter(
                    source_city=source_city,
                    destination_city=destination_city,
                    flight_date=departure_date,
                    available_seats__gte=passengers,
                    status="SCHEDULED",
                )
                .select_related("airline", "source_city", "destination_city")
                .order_by("departure_time")
            )

            # Pagination
            paginator = Paginator(flights, 10)
            page_number = request.GET.get("page")
            flights = paginator.get_page(page_number)

    context = {
        "form": form,
        "flights": flights,
        "search_performed": flights is not None,
    }
    return render(request, "flights.html", context)


@login_required
def Dashboard(request):
    """User dashboard with booking history"""
    user = request.user

    # Get user's bookings
    flight_bookings = (
        FlightBooking.objects.filter(user=user)
        .select_related("flight", "flight__airline")
        .order_by("-booking_date")
    )

    hotel_bookings = (
        HotelBooking.objects.filter(user=user)
        .select_related("hotel", "hotel__city")
        .order_by("-booking_date")
    )

    package_bookings = (
        PackageBooking.objects.filter(user=user)
        .select_related("flight_booking__flight", "hotel_booking__hotel")
        .order_by("-booking_date")
    )

    context = {
        "flight_bookings": flight_bookings,
        "hotel_bookings": hotel_bookings,
        "package_bookings": package_bookings,
    }
    return render(request, "dashboard.html", context)


@login_required
def FlightBookView(request, flight_id):
    """Flight booking view"""
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == "POST":
        form = FlightBookingForm(request.POST, flight=flight)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.flight = flight
            booking.booking_reference = generate_booking_reference()

            # Calculate total price
            passenger_count = booking.passenger_count
            if booking.travel_class == "ECONOMY":
                booking.total_price = flight.economy_price * passenger_count
            else:
                booking.total_price = flight.business_price * passenger_count

            booking.save()

            # Update available seats
            flight.available_seats -= passenger_count
            flight.save()

            messages.success(
                request,
                f"Flight booked successfully! Booking reference: {booking.booking_reference}",
            )
            return redirect("payment", booking_type="flight", booking_id=booking.id)
    else:
        form = FlightBookingForm(flight=flight)

    context = {
        "flight": flight,
        "form": form,
    }
    return render(request, "bookflight.html", context)


@login_required
def HotelBookView(request, hotel_id):
    """Hotel booking view"""
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == "POST":
        form = HotelBookingForm(request.POST, hotel=hotel)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.hotel = hotel
            booking.booking_reference = generate_booking_reference()

            # Calculate total price
            nights = (booking.check_out_date - booking.check_in_date).days
            booking.total_price = hotel.price_per_night * nights * booking.rooms_count

            booking.save()

            # Update available rooms
            hotel.available_rooms -= booking.rooms_count
            hotel.save()

            messages.success(
                request,
                f"Hotel booked successfully! Booking reference: {booking.booking_reference}",
            )
            return redirect("payment", booking_type="hotel", booking_id=booking.id)
    else:
        form = HotelBookingForm(hotel=hotel)

    context = {
        "hotel": hotel,
        "form": form,
    }
    return render(request, "bookhotel.html", context)


@login_required
def PackageBookView(request):
    """Package booking view"""
    flight_id = request.GET.get("flight_id")
    hotel_id = request.GET.get("hotel_id")

    if not flight_id or not hotel_id:
        messages.error(
            request, "Please select both flight and hotel for package booking."
        )
        return redirect("package_view")

    flight = get_object_or_404(Flight, id=flight_id)
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == "POST":
        flight_form = FlightBookingForm(request.POST, flight=flight, prefix="flight")
        hotel_form = HotelBookingForm(request.POST, hotel=hotel, prefix="hotel")
        package_form = PackageBookingForm(request.POST, prefix="package")

        if flight_form.is_valid() and hotel_form.is_valid() and package_form.is_valid():
            # Create flight booking
            flight_booking = flight_form.save(commit=False)
            flight_booking.user = request.user
            flight_booking.flight = flight
            flight_booking.booking_reference = generate_booking_reference()

            passenger_count = flight_booking.passenger_count
            if flight_booking.travel_class == "ECONOMY":
                flight_booking.total_price = flight.economy_price * passenger_count
            else:
                flight_booking.total_price = flight.business_price * passenger_count

            flight_booking.save()

            # Create hotel booking
            hotel_booking = hotel_form.save(commit=False)
            hotel_booking.user = request.user
            hotel_booking.hotel = hotel
            hotel_booking.booking_reference = generate_booking_reference()

            nights = (hotel_booking.check_out_date - hotel_booking.check_in_date).days
            hotel_booking.total_price = (
                hotel.price_per_night * nights * hotel_booking.rooms_count
            )

            hotel_booking.save()

            # Create package booking
            package_booking = package_form.save(commit=False)
            package_booking.user = request.user
            package_booking.flight_booking = flight_booking
            package_booking.hotel_booking = hotel_booking
            package_booking.booking_reference = generate_booking_reference()

            # Calculate package price with discount
            subtotal = flight_booking.total_price + hotel_booking.total_price
            discount_amount = subtotal * (
                package_booking.package_discount / Decimal("100")
            )
            package_booking.total_price = subtotal - discount_amount

            package_booking.save()

            # Update availability
            flight.available_seats -= passenger_count
            flight.save()
            hotel.available_rooms -= hotel_booking.rooms_count
            hotel.save()

            messages.success(
                request,
                f"Package booked successfully! Booking reference: {package_booking.booking_reference}",
            )
            return redirect(
                "payment", booking_type="package", booking_id=package_booking.id
            )
    else:
        flight_form = FlightBookingForm(flight=flight, prefix="flight")
        hotel_form = HotelBookingForm(hotel=hotel, prefix="hotel")
        package_form = PackageBookingForm(prefix="package")

    context = {
        "flight": flight,
        "hotel": hotel,
        "flight_form": flight_form,
        "hotel_form": hotel_form,
        "package_form": package_form,
    }
    return render(request, "bookpackage.html", context)


@login_required
def PaymentView(request, booking_type, booking_id):
    """Payment processing view"""
    booking = None

    if booking_type == "flight":
        booking = get_object_or_404(FlightBooking, id=booking_id, user=request.user)
    elif booking_type == "hotel":
        booking = get_object_or_404(HotelBooking, id=booking_id, user=request.user)
    elif booking_type == "package":
        booking = get_object_or_404(PackageBooking, id=booking_id, user=request.user)

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Create payment record
            payment = BookingPayment()
            payment.amount = booking.total_price
            payment.payment_method = form.cleaned_data["payment_method"]
            payment.transaction_id = generate_transaction_id()
            payment.status = "COMPLETED"  # In real app, this would be 'PROCESSING'

            # Link to appropriate booking
            if booking_type == "flight":
                payment.flight_booking = booking
            elif booking_type == "hotel":
                payment.hotel_booking = booking
            elif booking_type == "package":
                payment.package_booking = booking

            payment.save()

            # Update booking status
            booking.status = "CONFIRMED"
            booking.save()

            messages.success(
                request, f"Payment successful! Transaction ID: {payment.transaction_id}"
            )
            return redirect("dashboard")
    else:
        form = PaymentForm()

    context = {
        "booking": booking,
        "booking_type": booking_type,
        "form": form,
    }
    return render(request, "payment.html", context)


@login_required
def CancelBookingView(request, booking_type, booking_id):
    """Booking cancellation view"""
    booking = None

    if booking_type == "flight":
        booking = get_object_or_404(FlightBooking, id=booking_id, user=request.user)
    elif booking_type == "hotel":
        booking = get_object_or_404(HotelBooking, id=booking_id, user=request.user)
    elif booking_type == "package":
        booking = get_object_or_404(PackageBooking, id=booking_id, user=request.user)

    if request.method == "POST":
        if booking_type == "flight":
            # Restore available seats
            booking.flight.available_seats += booking.passenger_count
            booking.flight.save()
        elif booking_type == "hotel":
            # Restore available rooms
            booking.hotel.available_rooms += booking.rooms_count
            booking.hotel.save()
        elif booking_type == "package":
            # Restore both seats and rooms
            booking.flight_booking.flight.available_seats += (
                booking.flight_booking.passenger_count
            )
            booking.flight_booking.flight.save()
            booking.hotel_booking.hotel.available_rooms += (
                booking.hotel_booking.rooms_count
            )
            booking.hotel_booking.hotel.save()

        # Update booking status
        booking.status = "CANCELLED"
        booking.save()

        messages.success(request, "Booking cancelled successfully.")
        return redirect("dashboard")

    context = {
        "booking": booking,
        "booking_type": booking_type,
    }
    return render(request, "cancel_booking.html", context)


def PlacesView(request):
    """Tourist attractions view"""
    form = AttractionFilterForm()
    attractions = None

    if request.method == "POST":
        form = AttractionFilterForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data.get("city")
            category = form.cleaned_data.get("category")
            max_entry_fee = form.cleaned_data.get("max_entry_fee")

            attractions = TouristAttraction.objects.all().select_related("city")

            if city:
                attractions = attractions.filter(city=city)

            if category:
                attractions = attractions.filter(category=category)

            if max_entry_fee is not None:
                attractions = attractions.filter(
                    Q(entry_fee__lte=max_entry_fee) | Q(entry_fee__isnull=True)
                )

            attractions = attractions.order_by("city__name", "name")

            # Pagination
            paginator = Paginator(attractions, 12)
            page_number = request.GET.get("page")
            attractions = paginator.get_page(page_number)

    context = {
        "form": form,
        "attractions": attractions,
        "search_performed": attractions is not None,
    }
    return render(request, "places.html", context)


def AttractionDetailView(request, attraction_id):
    """Individual attraction detail view"""
    attraction = get_object_or_404(TouristAttraction, id=attraction_id)

    # Get other attractions in the same city
    related_attractions = TouristAttraction.objects.filter(
        city=attraction.city
    ).exclude(id=attraction_id)[:4]

    context = {
        "attraction": attraction,
        "related_attractions": related_attractions,
    }
    return render(request, "attraction_detail.html", context)


def ContactView(request):
    """Contact form view"""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Here you would typically send an email or save to database
            messages.success(
                request, "Thank you for your message. We will get back to you soon!"
            )
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def AboutView(request):
    """About page view"""
    return render(request, "about.html")


# AJAX Views for dynamic content
def get_cities_ajax(request):
    """AJAX view to get cities for autocomplete"""
    query = request.GET.get("q", "")
    cities = City.objects.filter(name__icontains=query)[:10]
    data = [{"id": city.id, "text": f"{city.name}, {city.country}"} for city in cities]
    return JsonResponse({"results": data})


def check_availability_ajax(request):
    """AJAX view to check real-time availability"""
    booking_type = request.GET.get("type")
    item_id = request.GET.get("id")
    quantity = int(request.GET.get("quantity", 1))

    if booking_type == "flight":
        flight = get_object_or_404(Flight, id=item_id)
        available = flight.available_seats >= quantity
        return JsonResponse(
            {
                "available": available,
                "available_quantity": flight.available_seats,
                "price": float(flight.economy_price),
            }
        )
    elif booking_type == "hotel":
        hotel = get_object_or_404(Hotel, id=item_id)
        available = hotel.available_rooms >= quantity
        return JsonResponse(
            {
                "available": available,
                "available_quantity": hotel.available_rooms,
                "price": float(hotel.price_per_night),
            }
        )

    return JsonResponse({"error": "Invalid request"})


# Utility functions
def generate_booking_reference():
    """Generate unique booking reference"""
    return str(uuid.uuid4()).upper()[:10]


def generate_transaction_id():
    """Generate unique transaction ID"""
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    return f"TXN{timestamp}{str(uuid.uuid4())[:8].upper()}"


# Error handling views
def handler404(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)
