def select_products_by_category(products, category):
    return list(filter((lambda product: product.category == category), products))
