from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
from faker import Faker
import random
from datetime import datetime, timedelta

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Seeds the database with sample listings, bookings, and reviews'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Create admin user if not exists
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@alxtravelapp.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create regular users
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'user{i + 1}',
                defaults={
                    'email': f'user{i + 1}@example.com',
                    'is_staff': False
                }
            )
            if created:
                user.set_password(f'user{i + 1}123')
                user.save()
                users.append(user)
                self.stdout.write(self.style.SUCCESS(f'Created user {user.username}'))

        # Create listings
        property_types = [x[0] for x in Listing.PROPERTY_TYPES]
        listings = []
        for i in range(10):
            listing = Listing.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=5),
                address=fake.street_address(),
                city=fake.city(),
                state=fake.state(),
                country=fake.country(),
                price_per_night=random.randint(50, 500),
                property_type=random.choice(property_types),
                num_bedrooms=random.randint(1, 5),
                num_bathrooms=random.randint(1, 3),
                max_guests=random.randint(2, 10),
                amenities=', '.join(fake.words(nb=random.randint(3, 10))),
                is_available=random.choice([True, False]),
                owner=admin if i < 5 else random.choice(users)
            )
            listings.append(listing)
            self.stdout.write(self.style.SUCCESS(f'Created listing {listing.title}'))

        # Create bookings
        statuses = [x[0] for x in Booking.STATUS_CHOICES]
        for i in range(20):
            start_date = fake.date_between(start_date='-30d', end_date='+30d')
            end_date = start_date + timedelta(days=random.randint(1, 14))
            listing = random.choice(listings)
            total_price = (end_date - start_date).days * listing.price_per_night

            Booking.objects.create(
                listing=listing,
                user=random.choice(users),
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status=random.choice(statuses)
            )
            self.stdout.write(self.style.SUCCESS(f'Created booking for {listing.title}'))

        # Create reviews
        for i in range(15):
            listing = random.choice(listings)
            user = random.choice(users)

            Review.objects.create(
                listing=listing,
                user=user,
                rating=random.randint(1, 5),
                comment=fake.paragraph(nb_sentences=2)
            )
            self.stdout.write(self.style.SUCCESS(f'Created review by {user.username} for {listing.title}'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))