def extract_prices(products):
    return list(map((lambda product: product.price), products))
