from django.core.management.base import BaseCommand
from listings.models import Listing
from datetime import date

class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def handle(self, *args, **kwargs):
        listings_data = [
            {
                "title": "Beach Resort",
                "description": "Luxury beach resort with ocean view",
                "price_per_night": 250.00,
                "location": "Lagos, Nigeria",
                "available_from": date(2025, 8, 1),
                "available_to": date(2025, 12, 31),
            },
            {
                "title": "Mountain Cabin",
                "description": "Cozy cabin in the mountains",
                "price_per_night": 150.00,
                "location": "Jos, Nigeria",
                "available_from": date(2025, 9, 15),
                "available_to": date(2026, 3, 15),
            }
        ]

        for listing_data in listings_data:
            Listing.objects.create(**listing_data)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
