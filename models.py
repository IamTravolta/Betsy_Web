from peewee import *

# Models go here
# Initialize the database
db = MySQLDatabase('betsy', user='root', password='',
                   host='localhost', port=3306)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    address = TextField()
    billing_info = TextField()


class Tag(BaseModel):
    name = CharField(unique=True)


class Product(BaseModel):
    name = CharField()
    description = TextField()
    price_per_unit = DecimalField(decimal_places=2)
    quantity_in_stock = IntegerField()
    tags = ManyToManyField(Tag)
    user = ForeignKeyField(User)


class Transaction(BaseModel):
    buyer = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    quantity_purchased = IntegerField()


def create_tables():
    with db:
        db.create_tables([User, Tag, Product, Product.tags.get_through_model(), Transaction])


def populate_test_database():
    create_tables()

    user1 = User.create(
        name='John Doe',
        address='Lodewijk 123, Rotterdam',
        billing_info='Card ending in 1234'
    )
    user2 = User.create(
        name='Jane Smith',
        address='Meerlaan 456, Amstedram',
        billing_info='Card ending in 5678'
    )

    tag1 = Tag.create(name='Handmade')
    tag2 = Tag.create(name='Vintage')

    product1 = Product.create(
        name='Handmade Sweater',
        description='Cozy handmade sweater',
        price_per_unit=50.00,
        quantity_in_stock=10,
        user=user1
    )
    product1.tags.add(tag1)

    product2 = Product.create(
        name='Vintage Vase',
        description='Beautiful vintage vase',
        price_per_unit=30.00,
        quantity_in_stock=5,
        user=user2
    )
    product2.tags.add(tag2)

    Transaction.create(
        buyer=user1,
        product=product1,
        quantity_purchased=2
    )
    Transaction.create(
        buyer=user2,
        product=product2,
        quantity_purchased=1
    )
