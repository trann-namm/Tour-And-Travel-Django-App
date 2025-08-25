from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import (
    Flight,
    Hotel,
    PackageBooking,
    FlightBooking,
    HotelBooking,
    TouristAttraction,
    City,
    Airline,
)
import datetime
from decimal import Decimal


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "d-form form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "d-form form-control", "placeholder": "Last Name"}
        ),
    )
    email = forms.EmailField(
        max_length=254,
        help_text="Required. Inform a valid email address.",
        widget=forms.EmailInput(
            attrs={"class": "d-form form-control", "placeholder": "Email Address"}
        ),
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "d-form form-control", "placeholder": "Username"}
        ),
    )
    password1 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={"class": "d-form form-control", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={"class": "d-form form-control", "placeholder": "Confirm Password"}
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password and confirm password do not match.")
        return cleaned_data


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={"class": "d-form form-control", "placeholder": "Username or Email"}
        ),
    )
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={"class": "d-form form-control", "placeholder": "Password"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "password")


class FlightSearchForm(forms.Form):
    TRIP_TYPE_CHOICES = [
        ("one_way", "One Way"),
        ("round_trip", "Round Trip"),
    ]

    CLASS_CHOICES = [
        ("ECONOMY", "Economy"),
        ("BUSINESS", "Business"),
    ]

    trip_type = forms.ChoiceField(
        choices=TRIP_TYPE_CHOICES,
        initial="one_way",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    source_city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Select Source City",
        widget=forms.Select(
            attrs={"class": "fs-form form-control", "placeholder": "Source City"}
        ),
    )

    destination_city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Select Destination City",
        widget=forms.Select(
            attrs={"class": "fds-forms form-control", "placeholder": "Destination City"}
        ),
    )

    departure_date = forms.DateField(
        initial=datetime.date.today,
        widget=forms.DateInput(
            attrs={
                "class": "fd-form form-control",
                "type": "date",
                "min": datetime.date.today().strftime("%Y-%m-%d"),
            }
        ),
    )

    return_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "fd-form form-control", "type": "date"}),
    )

    passengers = forms.IntegerField(
        initial=1,
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Number of Passengers"}
        ),
    )

    travel_class = forms.ChoiceField(
        choices=CLASS_CHOICES,
        initial="ECONOMY",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        source_city = cleaned_data.get("source_city")
        destination_city = cleaned_data.get("destination_city")
        departure_date = cleaned_data.get("departure_date")
        return_date = cleaned_data.get("return_date")
        trip_type = cleaned_data.get("trip_type")

        if source_city and destination_city and source_city == destination_city:
            raise ValidationError("Source and destination cities cannot be the same.")

        if departure_date and departure_date < datetime.date.today():
            raise ValidationError("Departure date cannot be in the past.")

        if trip_type == "round_trip" and not return_date:
            raise ValidationError("Return date is required for round trip.")

        if return_date and departure_date and return_date <= departure_date:
            raise ValidationError("Return date must be after departure date.")

        return cleaned_data


class HotelSearchForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Select City",
        widget=forms.Select(attrs={"class": "fs-form form-control"}),
    )

    check_in_date = forms.DateField(
        initial=datetime.date.today,
        widget=forms.DateInput(
            attrs={
                "class": "fd-form form-control",
                "type": "date",
                "min": datetime.date.today().strftime("%Y-%m-%d"),
            }
        ),
    )

    check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "fd-form form-control", "type": "date"})
    )

    guests = forms.IntegerField(
        initial=1,
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Number of Guests"}
        ),
    )

    rooms = forms.IntegerField(
        initial=1,
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Number of Rooms"}
        ),
    )

    min_rating = forms.ChoiceField(
        choices=[(i, f"{i} Star{'s' if i != 1 else ''}") for i in range(1, 6)],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    max_price = forms.DecimalField(
        required=False,
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Max Price per Night"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")

        if check_in_date and check_in_date < datetime.date.today():
            raise ValidationError("Check-in date cannot be in the past.")

        if check_in_date and check_out_date and check_out_date <= check_in_date:
            raise ValidationError("Check-out date must be after check-in date.")

        return cleaned_data


class FlightBookingForm(forms.ModelForm):
    class Meta:
        model = FlightBooking
        fields = ["passenger_count", "travel_class"]
        widgets = {
            "passenger_count": forms.NumberInput(
                attrs={
                    "class": "fs-form form-control",
                    "placeholder": "Number of Passengers",
                    "min": "1",
                    "max": "10",
                }
            ),
            "travel_class": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.flight = kwargs.pop("flight", None)
        super().__init__(*args, **kwargs)

    def clean_passenger_count(self):
        passenger_count = self.cleaned_data.get("passenger_count")
        if self.flight and passenger_count > self.flight.available_seats:
            raise ValidationError(
                f"Only {self.flight.available_seats} seats available."
            )
        return passenger_count


class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = [
            "check_in_date",
            "check_out_date",
            "rooms_count",
            "guests_count",
            "special_requests",
        ]
        widgets = {
            "check_in_date": forms.DateInput(
                attrs={"class": "fd-form form-control", "type": "date"}
            ),
            "check_out_date": forms.DateInput(
                attrs={"class": "fd-form form-control", "type": "date"}
            ),
            "rooms_count": forms.NumberInput(
                attrs={
                    "class": "fs-form form-control",
                    "placeholder": "Number of Rooms",
                    "min": "1",
                    "max": "5",
                }
            ),
            "guests_count": forms.NumberInput(
                attrs={
                    "class": "fs-form form-control",
                    "placeholder": "Number of Guests",
                    "min": "1",
                    "max": "10",
                }
            ),
            "special_requests": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Any special requests...",
                    "rows": "3",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.hotel = kwargs.pop("hotel", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")
        rooms_count = cleaned_data.get("rooms_count")

        if check_in_date and check_in_date < datetime.date.today():
            raise ValidationError("Check-in date cannot be in the past.")

        if check_in_date and check_out_date and check_out_date <= check_in_date:
            raise ValidationError("Check-out date must be after check-in date.")

        if self.hotel and rooms_count and rooms_count > self.hotel.available_rooms:
            raise ValidationError(f"Only {self.hotel.available_rooms} rooms available.")

        return cleaned_data


class PackageBookingForm(forms.ModelForm):
    class Meta:
        model = PackageBooking
        fields = ["package_discount"]
        widgets = {
            "package_discount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Package Discount %",
                    "min": "0",
                    "max": "50",
                    "step": "0.01",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        self.flight_booking = kwargs.pop("flight_booking", None)
        self.hotel_booking = kwargs.pop("hotel_booking", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        package = super().save(commit=False)
        if self.flight_booking:
            package.flight_booking = self.flight_booking
        if self.hotel_booking:
            package.hotel_booking = self.hotel_booking

        # Calculate total price with discount
        flight_price = (
            self.flight_booking.total_price if self.flight_booking else Decimal("0.00")
        )
        hotel_price = (
            self.hotel_booking.total_price if self.hotel_booking else Decimal("0.00")
        )
        subtotal = flight_price + hotel_price
        discount_amount = subtotal * (package.package_discount / Decimal("100"))
        package.total_price = subtotal - discount_amount

        if commit:
            package.save()
        return package


class CitySearchForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Select City",
        widget=forms.Select(attrs={"class": "fs-form form-control"}),
    )


class AttractionFilterForm(forms.Form):
    CATEGORY_CHOICES = [("", "All Categories")] + TouristAttraction.CATEGORY_CHOICES

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        empty_label="All Cities",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    max_entry_fee = forms.DecimalField(
        required=False,
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Max Entry Fee"}
        ),
    )


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Your Email"}
        )
    )

    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Subject"}
        ),
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Your Message...",
                "rows": "5",
            }
        )
    )


class PaymentForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ("CREDIT_CARD", "Credit Card"),
        ("DEBIT_CARD", "Debit Card"),
        ("PAYPAL", "PayPal"),
        ("BANK_TRANSFER", "Bank Transfer"),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    card_number = forms.CharField(
        max_length=19,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Card Number",
                "pattern": r"\d{4}\s\d{4}\s\d{4}\s\d{4}",
            }
        ),
    )

    expiry_month = forms.ChoiceField(
        choices=[(i, f"{i:02d}") for i in range(1, 13)],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    expiry_year = forms.ChoiceField(
        choices=[
            (i, str(i))
            for i in range(datetime.date.today().year, datetime.date.today().year + 11)
        ],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    cvv = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "CVV", "maxlength": "4"}
        ),
    )

    cardholder_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Cardholder Name"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get("payment_method")

        if payment_method in ["CREDIT_CARD", "DEBIT_CARD"]:
            required_fields = [
                "card_number",
                "expiry_month",
                "expiry_year",
                "cvv",
                "cardholder_name",
            ]
            for field in required_fields:
                if not cleaned_data.get(field):
                    raise ValidationError(
                        f"{field.replace('_', ' ').title()} is required for card payments."
                    )

        return cleaned_data
