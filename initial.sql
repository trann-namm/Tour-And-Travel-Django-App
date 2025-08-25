-- Insert sample data for all tables in the travel booking system

-- 1. Cities
INSERT INTO travelapp_city (name, country, airport_code, best_link, week_get_links, created_at, updated_at) VALUES
('New York', 'USA', 'JFK', 'https://visitnyc.com', 'https://deals.nyc.com', '2025-01-01 10:00:00', '2025-01-01 10:00:00'),
('Los Angeles', 'USA', 'LAX', 'https://visitla.com', 'https://deals.la.com', '2025-01-01 11:00:00', '2025-01-01 11:00:00'),
('London', 'UK', 'LHR', 'https://visitlondon.com', 'https://deals.london.com', '2025-01-01 12:00:00', '2025-01-01 12:00:00'),
('Paris', 'France', 'CDG', 'https://visitparis.com', 'https://deals.paris.com', '2025-01-01 13:00:00', '2025-01-01 13:00:00'),
('Tokyo', 'Japan', 'NRT', 'https://visittokyo.com', 'https://deals.tokyo.com', '2025-01-01 14:00:00', '2025-01-01 14:00:00'),
('Dubai', 'UAE', 'DXB', 'https://visitdubai.com', 'https://deals.dubai.com', '2025-01-01 15:00:00', '2025-01-01 15:00:00');

-- 2. Airlines
INSERT INTO travelapp_airline (name, code) VALUES
('American Airlines', 'AA'),
('Delta Air Lines', 'DL'),
('United Airlines', 'UA'),
('British Airways', 'BA'),
('Air France', 'AF'),
('Japan Airlines', 'JL'),
('Emirates', 'EK'),
('Lufthansa', 'LH');

-- 3. Flights
INSERT INTO travelapp_flight (flight_number, airline_id, source_city_id, destination_city_id, departure_time, arrival_time, flight_date, economy_price, business_price, total_seats, available_seats, status, created_at, updated_at) VALUES
('AA101', 1, 1, 2, '08:00:00', '11:30:00', '2025-08-25', 299.99, 899.99, 180, 45, 'SCHEDULED', '2025-01-01 10:00:00', '2025-01-01 10:00:00'),
('DL205', 2, 2, 1, '14:00:00', '22:15:00', '2025-08-25', 349.99, 1099.99, 200, 67, 'SCHEDULED', '2025-01-01 11:00:00', '2025-01-01 11:00:00'),
('BA301', 4, 1, 3, '20:00:00', '08:30:00', '2025-08-26', 599.99, 1899.99, 250, 89, 'SCHEDULED', '2025-01-01 12:00:00', '2025-01-01 12:00:00'),
('AF401', 5, 3, 4, '10:30:00', '12:00:00', '2025-08-26', 149.99, 599.99, 150, 34, 'SCHEDULED', '2025-01-01 13:00:00', '2025-01-01 13:00:00'),
('JL501', 6, 4, 5, '16:45:00', '10:30:00', '2025-08-27', 799.99, 2499.99, 300, 112, 'SCHEDULED', '2025-01-01 14:00:00', '2025-01-01 14:00:00'),
('EK601', 7, 5, 6, '02:15:00', '06:45:00', '2025-08-27', 459.99, 1299.99, 380, 156, 'SCHEDULED', '2025-01-01 15:00:00', '2025-01-01 15:00:00');

-- 4. Hotels
INSERT INTO travelapp_hotel (name, city_id, address, price_per_night, star_rating, amenities, distance_from_airport, total_rooms, available_rooms, main_image, phone, email, website, created_at, updated_at) VALUES
('The Plaza Hotel', 1, '768 5th Ave, New York, NY 10019', 599.00, 5, 'WiFi, Pool, Spa, Restaurant, Room Service, Concierge', 25.5, 282, 34, 'hotels/plaza_nyc.jpg', '+1-212-759-3000', 'reservations@theplaza.com', 'https://theplaza.com', '2025-01-01 10:00:00', '2025-01-01 10:00:00'),
('Beverly Hills Hotel', 2, '9641 Sunset Blvd, Beverly Hills, CA 90210', 799.00, 5, 'WiFi, Pool, Spa, Restaurant, Valet Parking, Tennis Court', 18.2, 210, 45, 'hotels/beverly_hills.jpg', '+1-310-276-2251', 'info@beverlyhillshotel.com', 'https://beverlyhillshotel.com', '2025-01-01 11:00:00', '2025-01-01 11:00:00'),
('The Ritz London', 3, '150 Piccadilly, St. James, London W1J 9BR', 899.00, 5, 'WiFi, Restaurant, Bar, Concierge, Business Center, Fitness Center', 24.8, 136, 23, 'hotels/ritz_london.jpg', '+44-20-7493-8181', 'enquire@theritzlondon.com', 'https://theritzlondon.com', '2025-01-01 12:00:00', '2025-01-01 12:00:00'),
('Hotel de Crillon', 4, '10 Place de la Concorde, 75008 Paris', 1299.00, 5, 'WiFi, Spa, Restaurant, Bar, Room Service, Business Center', 35.6, 124, 18, 'hotels/crillon_paris.jpg', '+33-1-44-71-15-00', 'reservations@crillon.com', 'https://crillon.com', '2025-01-01 13:00:00', '2025-01-01 13:00:00'),
('The Peninsula Tokyo', 5, '1-8-1 Yurakucho, Chiyoda City, Tokyo 100-0006', 699.00, 5, 'WiFi, Pool, Spa, Restaurant, Business Center, Fitness Center', 65.4, 314, 67, 'hotels/peninsula_tokyo.jpg', '+81-3-6270-2888', 'reservations@peninsula.com', 'https://peninsula.com/tokyo', '2025-01-01 14:00:00', '2025-01-01 14:00:00'),
('Burj Al Arab', 6, 'Jumeirah St, Dubai', 2499.00, 5, 'WiFi, Pool, Spa, Multiple Restaurants, Butler Service, Helipad', 22.3, 202, 34, 'hotels/burj_al_arab.jpg', '+971-4-301-7777', 'baa.reservations@jumeirah.com', 'https://jumeirah.com/burj-al-arab', '2025-01-01 15:00:00', '2025-01-01 15:00:00');

-- 5. Tourist Attractions
INSERT INTO travelapp_touristattraction (name, city_id, category, description, image, address, opening_hours, entry_fee, website, created_at) VALUES
('Statue of Liberty', 1, 'HISTORICAL', 'Iconic statue symbolizing freedom and democracy, located on Liberty Island.', 'attractions/statue_of_liberty.jpg', 'Liberty Island, New York, NY 10004', '9:30 AM - 5:00 PM', 25.50, 'https://nps.gov/stli', '2025-01-01 10:00:00'),
('Central Park', 1, 'PARK', 'Large public park in Manhattan offering recreational activities and beautiful landscapes.', 'attractions/central_park.jpg', 'New York, NY 10024', '6:00 AM - 1:00 AM', 0.00, 'https://centralparknyc.org', '2025-01-01 11:00:00'),
('Hollywood Walk of Fame', 2, 'ENTERTAINMENT', 'Famous sidewalk with stars honoring celebrities in the entertainment industry.', 'attractions/hollywood_walk.jpg', 'Hollywood Blvd, Hollywood, CA 90028', '24 hours', 0.00, 'https://walkoffame.com', '2025-01-01 12:00:00'),
('Tower of London', 3, 'HISTORICAL', 'Historic castle and former royal residence, home to the Crown Jewels.', 'attractions/tower_london.jpg', 'St Katharine & Wapping, London EC3N 4AB', '9:00 AM - 5:30 PM', 34.80, 'https://hrp.org.uk/tower-of-london', '2025-01-01 13:00:00'),
('Eiffel Tower', 4, 'HISTORICAL', 'Iconic iron lattice tower and symbol of Paris, offering panoramic city views.', 'attractions/eiffel_tower.jpg', 'Champ de Mars, 75007 Paris', '9:30 AM - 11:45 PM', 29.40, 'https://toureiffel.paris', '2025-01-01 14:00:00'),
('Senso-ji Temple', 5, 'RELIGIOUS', 'Ancient Buddhist temple and Tokyo oldest temple, located in Asakusa district.', 'attractions/sensoji_temple.jpg', '2 Chome-3-1 Asakusa, Taito City, Tokyo 111-0032', '6:00 AM - 5:00 PM', 0.00, 'https://sensoji.jp', '2025-01-01 15:00:00'),
('Burj Khalifa', 6, 'ENTERTAINMENT', 'World tallest building offering observation decks with stunning city views.', 'attractions/burj_khalifa.jpg', '1 Sheikh Mohammed bin Rashid Blvd, Dubai', '8:30 AM - 11:00 PM', 149.00, 'https://burjkhalifa.ae', '2025-01-01 16:00:00');

-- 6. Users (Django auth_user table - you might need to adjust this based on your user setup)
-- Note: In a real scenario, you would create users through Django admin or registration forms
INSERT INTO auth_user (username, first_name, last_name, email, is_staff, is_active, is_superuser, date_joined, password) VALUES
('john_doe', 'John', 'Doe', 'john.doe@email.com', 0, 1, 0, '2025-01-01 10:00:00', 'pbkdf2_sha256$260000$dummy_hash_value'),
('jane_smith', 'Jane', 'Smith', 'jane.smith@email.com', 0, 1, 0, '2025-01-01 11:00:00', 'pbkdf2_sha256$260000$dummy_hash_value'),
('mike_johnson', 'Mike', 'Johnson', 'mike.johnson@email.com', 0, 1, 0, '2025-01-01 12:00:00', 'pbkdf2_sha256$260000$dummy_hash_value');

-- 7. Flight Bookings
INSERT INTO travelapp_flightbooking (user_id, flight_id, booking_reference, passenger_count, travel_class, total_price, status, booking_date, updated_at) VALUES
(1, 1, 'FL001A', 2, 'ECONOMY', 599.98, 'CONFIRMED', '2025-08-20 10:30:00', '2025-08-20 10:30:00'),
(2, 3, 'FL002B', 1, 'BUSINESS', 1899.99, 'CONFIRMED', '2025-08-21 14:15:00', '2025-08-21 14:15:00'),
(3, 5, 'FL003C', 4, 'ECONOMY', 3199.96, 'PENDING', '2025-08-22 09:45:00', '2025-08-22 09:45:00');

-- 8. Hotel Bookings
INSERT INTO travelapp_hotelbooking (user_id, hotel_id, booking_reference, check_in_date, check_out_date, rooms_count, guests_count, total_price, status, special_requests, booking_date, updated_at) VALUES
(1, 1, 'HT001A', '2025-08-25', '2025-08-28', 1, 2, 1797.00, 'CONFIRMED', 'Late check-in requested', '2025-08-20 11:00:00', '2025-08-20 11:00:00'),
(2, 3, 'HT002B', '2025-08-26', '2025-08-29', 1, 1, 2697.00, 'CONFIRMED', 'High floor room preferred', '2025-08-21 15:30:00', '2025-08-21 15:30:00'),
(3, 5, 'HT003C', '2025-08-27', '2025-08-31', 2, 4, 5592.00, 'PENDING', 'Connecting rooms requested', '2025-08-22 10:15:00', '2025-08-22 10:15:00');

-- 9. Package Bookings
INSERT INTO travelapp_packagebooking (user_id, flight_booking_id, hotel_booking_id, booking_reference, package_discount, total_price, status, booking_date, updated_at) VALUES
(1, 1, 1, 'PK001A', 10.00, 2157.28, 'CONFIRMED', '2025-08-20 12:00:00', '2025-08-20 12:00:00');

-- 10. Booking Payments
INSERT INTO travelapp_bookingpayment (flight_booking_id, hotel_booking_id, package_booking_id, amount, payment_method, transaction_id, status, payment_date, updated_at) VALUES
(NULL, NULL, 1, 2157.28, 'CREDIT_CARD', 'TXN001A2025', 'COMPLETED', '2025-08-20 12:15:00', '2025-08-20 12:15:00'),
(2, NULL, NULL, 1899.99, 'PAYPAL', 'TXN002B2025', 'COMPLETED', '2025-08-21 14:30:00', '2025-08-21 14:30:00'),
(NULL, 2, NULL, 2697.00, 'DEBIT_CARD', 'TXN003C2025', 'COMPLETED', '2025-08-21 15:45:00', '2025-08-21 15:45:00'),
(3, NULL, NULL, 3199.96, 'CREDIT_CARD', 'TXN004D2025', 'PENDING', '2025-08-22 09:50:00', '2025-08-22 09:50:00'),
(NULL, 3, NULL, 5592.00, 'BANK_TRANSFER', 'TXN005E2025', 'PROCESSING', '2025-08-22 10:20:00', '2025-08-22 10:20:00');

-- Additional sample data for more realistic scenarios

-- More flights for different routes
INSERT INTO travelapp_flight (flight_number, airline_id, source_city_id, destination_city_id, departure_time, arrival_time, flight_date, economy_price, business_price, total_seats, available_seats, status, created_at, updated_at) VALUES
('UA701', 3, 3, 6, '12:00:00', '23:45:00', '2025-08-28', 689.99, 2199.99, 280, 98, 'SCHEDULED', '2025-01-01 16:00:00', '2025-01-01 16:00:00'),
('LH801', 8, 6, 3, '05:30:00', '10:15:00', '2025-08-29', 599.99, 1799.99, 320, 145, 'SCHEDULED', '2025-01-01 17:00:00', '2025-01-01 17:00:00');

-- More budget-friendly hotels
INSERT INTO travelapp_hotel (name, city_id, address, price_per_night, star_rating, amenities, distance_from_airport, total_rooms, available_rooms, main_image, phone, email, website, created_at, updated_at) VALUES
('Holiday Inn Express', 1, '232 W 29th St, New York, NY 10001', 189.00, 3, 'WiFi, Breakfast, Fitness Center, Business Center', 15.8, 168, 87, 'hotels/holiday_inn_nyc.jpg', '+1-212-695-7200', 'reservations@hiexpress.com', 'https://ihg.com', '2025-01-01 16:00:00', '2025-01-01 16:00:00'),
('Premier Inn', 3, '85 York Rd, London SE1 7NJ', 125.00, 3, 'WiFi, Restaurant, 24h Reception', 32.1, 203, 76, 'hotels/premier_inn_london.jpg', '+44-871-527-9222', 'london@premierinn.com', 'https://premierinn.com', '2025-01-01 17:00:00', '2025-01-01 17:00:00');