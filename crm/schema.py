import graphene
from graphene_django.types import DjangoObjectType
from .models import Customer, Product, Order
from django.db import transaction
from django.core.exceptions import ValidationError

# Object Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

# Mutations
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created successfully")

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(lambda: CustomerInput, required=True)

    customers_created = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @staticmethod
    @transaction.atomic
    def mutate(root, info, customers):
        created = []
        errors = []
        for cust in customers:
            try:
                customer = Customer(name=cust.name, email=cust.email, phone=cust.phone)
                customer.full_clean()
                customer.save()
                created.append(customer)
            except Exception as e:
                errors.append(f"{cust.name}: {str(e)}")
        return BulkCreateCustomers(customers_created=created, errors=errors)

class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int()

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise ValidationError("Price must be positive")
        if stock < 0:
            raise ValidationError("Stock cannot be negative")
        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product)

class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids):
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise ValidationError("Customer ID is invalid")
        if not product_ids:
            raise ValidationError("At least one product must be selected")

        order = Order(customer=customer)
        order.save()
        products = Product.objects.filter(id__in=product_ids)
        order.products.set(products)
        order.total_amount = sum([p.price for p in products])
        order.save()
        return CreateOrder(order=order)

# Combine Mutations
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()  
    
class Query(graphene.ObjectType):
    all_customers = graphene.List(lambda: CustomerType)

    def resolve_all_customers(root, info):
        return Customer.objects.all()