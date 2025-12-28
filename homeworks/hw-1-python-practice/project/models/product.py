class Product:
    def __init__(self, name: str, category: str, price: int):
        self.name = name
        self.category = category
        self.price = price
        self.sale = 0

    def edit_category(self, new_category: str):
        self.category = new_category

    def edit_price(self, new_price: int):
        self.price = new_price

    def set_sale(self, sale: int):
        self.sale = sale

    def cancel_sale(self):
        self.sale = 0

    def get_price(self) -> int:
        # Это не тупо геттер - тут надо учесть скидку и еще то, что скидка указана в процентах
        if self.sale == 0:
            return self.price
        else:
            return self.price * (100 - self.sale) / 100

    def __repr__(self):
        return f'Product {self.name} in {self.category} costs {self.get_price()}'
