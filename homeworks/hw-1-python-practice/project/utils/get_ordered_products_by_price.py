def get_ordered_products_by_price(products):
    return sorted(products, key=(lambda product: product.price), reverse=True)
