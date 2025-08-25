from django.contrib import admin
from travelapp.models import Flight,Airline,Hotel,City,TouristAttraction,FlightBooking,HotelBooking,PackageBooking,BookingPayment

# Register your models here.
admin.site.register(Flight)
admin.site.register(Airline)
admin.site.register(Hotel)
admin.site.register(City)
admin.site.register(TouristAttraction)
admin.site.register(FlightBooking)
admin.site.register(HotelBooking)
admin.site.register(PackageBooking)
admin.site.register(BookingPayment)

