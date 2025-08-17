# crm/seed_db.py
import os
import django
import random
from faker import Faker

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql.settings")
django.setup()

from crm.models import Customer, Product  # Import your models

fake = Faker()


def seed_customers(n=20):
    print(f"Seeding {n} customers...")
    for _ in range(n):
        Customer.objects.create(
            name=fake.name,
            email=fake.unique.email(),
            phone=fake.phone_number()
        )
    print("✅ Customers seeded!")


def seed_products(n=10):
    print(f"Seeding {n} products...")
    for _ in range(n):
        Product.objects.create(
            name=fake.word().capitalize(),
            price=round(random.uniform(10.0, 1000.0), 2),
            stock=random.randint(0, 100)
        )
    print("✅ Products seeded!")


def run():
    seed_customers(20)
    seed_products(10)


if __name__ == "__main__":
    run()
