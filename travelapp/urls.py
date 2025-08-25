from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from .forms import UserLoginForm
from django.conf.urls.static import static

urlpatterns = [
    # Home & static pages
    path("", views.IndexView, name="index"),
    path("about/", views.AboutView, name="about"),
    path("contact/", views.ContactView, name="contact"),
    # Authentication
    path("register/", views.registerView, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    
    # urls.py
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Dashboard
    path("dashboard/", views.Dashboard, name="dashboard"),
    # Flight search & booking
    path("flights/", views.FlightView, name="flights"),
    path("flights/book/<int:flight_id>/", views.FlightBookView, name="book_flight"),
    # Hotel search & booking
    path("hotels/", views.HotelView, name="hotels"),
    path("hotels/book/<int:hotel_id>/", views.HotelBookView, name="book_hotel"),
    # Package search & booking
    path("package/", views.PackageView, name="package"),
    path("package/book/", views.PackageBookView, name="book_package"),
    # Tourist attractions
    path("places/", views.PlacesView, name="places"),
    path(
        "places/<int:attraction_id>/",
        views.AttractionDetailView,
        name="attraction_detail",
    ),
    # Booking payment & cancellation
    path(
        "payment/<str:booking_type>/<int:booking_id>/",
        views.PaymentView,
        name="payment",
    ),
    path(
        "cancel/<str:booking_type>/<int:booking_id>/",
        views.CancelBookingView,
        name="cancel_booking",
    ),
    # AJAX endpoints
    path("ajax/get-cities/", views.get_cities_ajax, name="get_cities_ajax"),
    path(
        "ajax/check-availability/",
        views.check_availability_ajax,
        name="check_availability_ajax",
    ),
]

# Custom error handlers
handler404 = "yourapp.views.handler404"  # replace 'yourapp' with the actual app name
handler500 = "yourapp.views.handler500"
