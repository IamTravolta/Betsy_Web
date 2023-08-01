from models import User, Product, Tag, Transaction, create_tables, populate_test_database
from peewee import MySQLDatabase

__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"



def search_products_by_term(term):
    return Product.select().where(Product.name ** f'%{term}%')


def list_user_products(user_id):
    return Product.select().join(User).where(User.id == user_id)


def list_products_per_tag(tag_name):
    tag = Tag.get(Tag.name == tag_name)
    return tag.products


def add_product_to_catalog(user_id, product_data):
    user = User.get_by_id(user_id)
    return Product.create(user=user, **product_data)


def remove_product(user_id, product_id):
    user = User.get_by_id(user_id)
    product = Product.get_by_id(product_id)

    if product.user == user:
        product.tags.clear()
        Transaction.delete().where(Transaction.product == product).execute()
        product.delete_instance()


def update_stock(product_id, new_stock_quantity):
    product = Product.get_by_id(product_id)
    product.quantity_in_stock = new_stock_quantity
    product.save()


def purchase_product(buyer_id, product_id, quantity_purchased):
    buyer = User.get_by_id(buyer_id)
    product = Product.get_by_id(product_id)
    if product.quantity_in_stock >= quantity_purchased:
        transaction = Transaction.create(buyer=buyer, product=product, quantity_purchased=quantity_purchased)
        product.quantity_in_stock -= quantity_purchased
        product.save()
        return transaction
    else:
        return None




db = MySQLDatabase('betsy', user='your_username', password='your_password',
                   host='your_host', port=3306)

if __name__ == '__main__':
    create_tables()

    populate_test_database()

    # Search products by term
    search_term = 'vintage'
    results = search_products_by_term(search_term)
    print(f"Products containing '{search_term}':")
    for product in results:
        print(f"Product: {product.name}, Description: {product.description}")

    # View products of a user
    user_id = 1
    user_products = list_user_products(user_id)
    print(f"Products of user with ID {user_id}:")
    for product in user_products:
        print(f"Product: {product.name}, Description: {product.description}")

    # View products by tag
    tag_name = 'Handmade'
    tag_products = list_products_per_tag(tag_name)
    print(f"Products with tag '{tag_name}':")
    for product in tag_products:
        print(f"Product: {product.name}, Description: {product.description}")

    # Add a product to a user
    user_id = 1
    product_data = {
        'name': 'New Product',
        'description': 'A new product',
        'price_per_unit': 10.00,
        'quantity_in_stock': 5
    }
    added_product = add_product_to_catalog(user_id, product_data)
    print("Product added to user:", added_product.name)

    # Remove a product from a user
    user_id = 1
    product_id = 1
    remove_product(user_id, product_id)
    print("Product removed from user.")

    # Update product stock
    product_id = 2
    new_stock_quantity = 3
    update_stock(product_id, new_stock_quantity)
    print("Product stock updated.")

    # Handle a purchase
    buyer_id = 2
    product_id = 2
    quantity_purchased = 2
    transaction = purchase_product(buyer_id, product_id, quantity_purchased)
    if transaction:
        print("Purchase successful. Transaction ID:", transaction.id)
    else:
        print("Purchase failed. Insufficient stock.")





