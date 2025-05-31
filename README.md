# ALX Travel App - Database Modeling and Data Seeding

This project implements database models and seeders for a travel booking application.

## Models

1. **Listing**: Represents properties available for booking
2. **Booking**: Represents guest bookings for properties
3. **Review**: Represents guest reviews of properties

## Setup

1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Seed the database: `python manage.py seed`

## API Endpoints

- Listings: `/listings/`
- Bookings: `/bookings/`
- Reviews: `/reviews/`
- Swagger Docs: `/swagger/`
