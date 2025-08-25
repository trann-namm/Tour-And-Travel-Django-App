from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    airport_code = models.CharField(
        max_length=3, unique=True, null=True, help_text="IATA airport code"
    )
    best_link = models.URLField(blank=True, null=True)
    week_get_links = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}, {self.country}"


class Airline(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True, help_text="IATA airline code")

    def __str__(self):
        return self.name


class Flight(models.Model):
    FLIGHT_STATUS_CHOICES = [
        ("SCHEDULED", "Scheduled"),
        ("DELAYED", "Delayed"),
        ("CANCELLED", "Cancelled"),
        ("BOARDING", "Boarding"),
        ("DEPARTED", "Departed"),
        ("ARRIVED", "Arrived"),
    ]

    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    source_city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="departing_flights"
    )
    destination_city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="arriving_flights"
    )
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    flight_date = models.DateField()
    economy_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    business_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=FLIGHT_STATUS_CHOICES, default="SCHEDULED"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["flight_date", "departure_time"]
        unique_together = ["flight_number", "flight_date"]

    def __str__(self):
        return f"{self.flight_number} - {self.source_city} to {self.destination_city}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.available_seats > self.total_seats:
            raise ValidationError("Available seats cannot exceed total seats")


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="hotels")
    address = models.TextField()
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    star_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars",
    )
    amenities = models.TextField(help_text="Comma-separated list of amenities")
    distance_from_airport = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Distance in kilometers",
    )
    total_rooms = models.PositiveIntegerField()
    available_rooms = models.PositiveIntegerField()
    main_image = models.ImageField(upload_to="hotels/", null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.city.name}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.available_rooms > self.total_rooms:
            raise ValidationError("Available rooms cannot exceed total rooms")


class TouristAttraction(models.Model):
    CATEGORY_CHOICES = [
        ("HISTORICAL", "Historical Site"),
        ("MUSEUM", "Museum"),
        ("PARK", "Park/Garden"),
        ("RELIGIOUS", "Religious Site"),
        ("ENTERTAINMENT", "Entertainment"),
        ("SHOPPING", "Shopping"),
        ("RESTAURANT", "Restaurant"),
        ("OTHER", "Other"),
    ]

    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="attractions")
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="OTHER"
    )
    description = models.TextField()
    image = models.ImageField(upload_to="attractions/", null=True, blank=True)
    address = models.TextField(blank=True)
    opening_hours = models.CharField(max_length=200, blank=True)
    entry_fee = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.city.name}"


class FlightBooking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
        ("COMPLETED", "Completed"),
    ]

    CLASS_CHOICES = [
        ("ECONOMY", "Economy"),
        ("BUSINESS", "Business"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="flight_bookings"
    )
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="bookings"
    )
    booking_reference = models.CharField(max_length=10, unique=True)
    passenger_count = models.PositiveIntegerField(default=1)
    travel_class = models.CharField(
        max_length=10, choices=CLASS_CHOICES, default="ECONOMY"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=BOOKING_STATUS_CHOICES, default="PENDING"
    )
    booking_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-booking_date"]

    def __str__(self):
        return f"Booking {self.booking_reference} - {self.user.username}"


class HotelBooking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
        ("CHECKED_IN", "Checked In"),
        ("CHECKED_OUT", "Checked Out"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hotel_bookings"
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="bookings")
    booking_reference = models.CharField(max_length=10, unique=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    rooms_count = models.PositiveIntegerField(default=1)
    guests_count = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=BOOKING_STATUS_CHOICES, default="PENDING"
    )
    special_requests = models.TextField(blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-booking_date"]

    def __str__(self):
        return f"Booking {self.booking_reference} - {self.user.username}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.check_in_date >= self.check_out_date:
            raise ValidationError("Check-out date must be after check-in date")

    @property
    def nights_count(self):
        return (self.check_out_date - self.check_in_date).days


class PackageBooking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
        ("COMPLETED", "Completed"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="package_bookings"
    )
    flight_booking = models.OneToOneField(FlightBooking, on_delete=models.CASCADE)
    hotel_booking = models.OneToOneField(HotelBooking, on_delete=models.CASCADE)
    booking_reference = models.CharField(max_length=10, unique=True)
    package_discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00, help_text="Discount percentage"
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=BOOKING_STATUS_CHOICES, default="PENDING"
    )
    booking_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-booking_date"]

    def __str__(self):
        return f"Package {self.booking_reference} - {self.user.username}"


class BookingPayment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("CREDIT_CARD", "Credit Card"),
        ("DEBIT_CARD", "Debit Card"),
        ("PAYPAL", "PayPal"),
        ("BANK_TRANSFER", "Bank Transfer"),
    ]

    # Generic foreign keys to handle different booking types
    flight_booking = models.ForeignKey(
        FlightBooking, on_delete=models.CASCADE, null=True, blank=True
    )
    hotel_booking = models.ForeignKey(
        HotelBooking, on_delete=models.CASCADE, null=True, blank=True
    )
    package_booking = models.ForeignKey(
        PackageBooking, on_delete=models.CASCADE, null=True, blank=True
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="PENDING"
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.amount}"
