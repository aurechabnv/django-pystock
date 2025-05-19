import pytest

from apps.catalog.models import Product, Category
from apps.inventory.models import Company, Location, Stock, Movement


@pytest.fixture
def product_gpu():
    product = Product.objects.create(
        sku='gpu-radeon-rx-9070-xt',
        name='RADEON RX 9070 XT',
        price=700.0,
        stock_threshold=10,
        vat=0.30,
    )
    category1 = Category.objects.create(name='Composants PC')
    category2 = Category.objects.create(name='Cartes graphiques')
    product.categories.set((category1, category2))
    return product


@pytest.fixture
def company():
    return Company.objects.create(
        name='Great Place for Computer Parts',
        siret='12345678912345',
    )


@pytest.fixture
def shop(company):
    return Location.objects.create(
        company=company,
        type=Location.LocationType.SHOP,
        name='GPCP Montpellier',
        city='Montpellier',
        zip_code='34000',
        address='45 rue des peupliers',
    )


@pytest.fixture
def warehouse(company):
    return Location.objects.create(
        company=company,
        type=Location.LocationType.WAREHOUSE,
        name='Entrepot des tilleuls',
        city='Orléans',
        zip_code='45000',
        address='12 avenue de tilleuls',
    )


@pytest.fixture
def stock_in_shop(product_gpu, shop):
    return Stock.objects.create(
        location=shop,
        product=product_gpu,
        quantity=60,
    )


@pytest.fixture
def stock_in_warehouse(product_gpu, warehouse):
    return Stock.objects.create(
        location=warehouse,
        product=product_gpu,
        quantity=120,
    )


@pytest.fixture
def movement_transfer(product_gpu, shop, warehouse):
    return Movement.objects.create(
        product=product_gpu,
        from_location=warehouse,
        to_location=shop,
        quantity=20,
        type=Movement.MovementType.TRANSFER,
    )


@pytest.fixture
def movement_inbound(product_gpu, warehouse):
    return Movement.objects.create(
        product=product_gpu,
        to_location=warehouse,
        quantity=100,
        type=Movement.MovementType.INBOUND,
    )


@pytest.fixture
def movement_outbound(product_gpu, shop):
    return Movement.objects.create(
        product=product_gpu,
        from_location=shop,
        quantity=35,
        type=Movement.MovementType.OUTBOUND,
    )
