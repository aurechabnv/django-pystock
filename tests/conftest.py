import pytest
from django.contrib.auth import get_user_model

from apps.catalog.models import Product, Category
from apps.inventory.models import Stock, Movement
from apps.management.models import Company, Location

User = get_user_model()


@pytest.fixture
def product1():
    product = Product.objects.create(
        sku='gpu-radeon-rx-9070-xt',
        name='RADEON RX 9070 XT',
        price=700.0,
        stock_threshold=100,
    )
    category1 = Category.objects.create(name='Composants PC')
    category2 = Category.objects.create(name='Cartes graphiques')
    product.categories.set((category1, category2,))
    return product


@pytest.fixture
def product2():
    product = Product.objects.create(
        sku="my-other-product",
        name="My other product",
        price=59.99,
        stock_threshold=20,
        vat=0.1,
    )
    return product


@pytest.fixture
def company1():
    company = Company.objects.create(
        name='Great Place for Computer Parts',
        siret='12345678912345',
    )
    return company


@pytest.fixture
def company2():
    company = Company.objects.create(
        name='Another Great Company',
        siret='45634626643446',
    )
    return company


@pytest.fixture
def location1(company1):
    return Location.objects.create(
        company=company1,
        type=Location.LocationType.SHOP,
        name='GPCP Montpellier',
        city='Montpellier',
        zip_code='34000',
        address_line_1='45 rue des peupliers',
    )


@pytest.fixture
def location2(company1):
    return Location.objects.create(
        company=company1,
        type=Location.LocationType.WAREHOUSE,
        name='Entrepot des tilleuls',
        city='Orléans',
        zip_code='45000',
        address_line_1='12 avenue de tilleuls',
        address_line_2='ZAE Sud',
    )


@pytest.fixture
def location3(company2):
    return Location.objects.create(
        company=company2,
        type=Location.LocationType.SHOP,
        name='Whatisit',
        city='Montpellier',
        zip_code='34000',
        address_line_1='28 rue Edmond Dantes',
    )


@pytest.fixture
def stock1(product1, location1):
    return Stock.objects.create(
        location=location1,
        product=product1,
        quantity=60,
    )


@pytest.fixture
def stock2(product1, location2):
    return Stock.objects.create(
        location=location2,
        product=product1,
        quantity=120,
    )


@pytest.fixture
def stock3(product1, location3):
    return Stock.objects.create(
        location=location3,
        product=product1,
        quantity=55,
    )


@pytest.fixture
def movement1_tr(product1, location1, location2):
    return Movement.objects.create(
        product=product1,
        from_location=location2,
        to_location=location1,
        quantity=20,
        type=Movement.MovementType.TRANSFER,
        synced=True,
    )


@pytest.fixture
def movement2_in(product1, location2):
    return Movement.objects.create(
        product=product1,
        to_location=location2,
        quantity=100,
        type=Movement.MovementType.INBOUND,
        synced=True,
    )


@pytest.fixture
def movement3_out(product1, location1):
    return Movement.objects.create(
        product=product1,
        from_location=location1,
        quantity=35,
        type=Movement.MovementType.OUTBOUND,
        synced=True,
    )


@pytest.fixture
def movement4(product1, location3):
    return Movement.objects.create(
        product=product1,
        from_location=location3,
        quantity=75,
        type=Movement.MovementType.INBOUND,
        synced=True,
    )


@pytest.fixture
def user1(company1):
    user = User.objects.create_user(
        username='user1',
        email='user1@example.com',
        password='azerty123*',
    )
    user.companies.add(company1)
    return user


@pytest.fixture
def user2():
    return User.objects.create_user(
        username='user2',
        email='user2@example.com',
        password='azerty123*',
        is_staff=True,
    )
