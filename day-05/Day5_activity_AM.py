class Product:
    # Class variable (shared by all instances)
    VAT_RATE = 0.15

    def __init__(self, code: str, name: str, price: float):
        if not isinstance(code, str) or not code.strip():
            raise ValueError("Code must be a non-empty string.")
        if not isinstance(name, str):
            raise ValueError("Name must be a string.")
        if price < 0:
            raise ValueError("Price cannot be negative.")

        self.code = code.upper() # Make code uppercase for consistency
        self.name = name.strip() # Remove accidental whitespace
        self.price = price

    def __str__(self):
        # User-friendly string representation
        return f"{self.code} - {self.name}: R{self.price:,.2f}"

    def __repr__(self):
        # Developer-friendly representation for debugging
        return f"Product(code='{self.code}', name='{self.name}', price={self.price})"

    # Using @property allows us to access this like an attribute: product1.vat
    @property
    def vat(self):
        return self.price * self.VAT_RATE

    @property
    def price_including_vat(self):
        return self.price + self.vat

    def apply_discount(self, percentage: float) -> float:
        if not (0 <= percentage <= 100):
            raise ValueError("Discount percentage must be between 0 and 100.")
        discount_amount = self.price * (percentage / 100)
        return self.price - discount_amount


def main():
    try:
        # 1. Create products
        product1 = Product("P001", "Keyboard", 200.00)
        product2 = Product("P002", "Mouse", 150.00)

        # 2. Print products (calls __str__)
        print("-" * 30)
        print("PRODUCT LIST:")
        print(product1)
        print(product2)
        print("-" * 30)

        # 3. Calculations using the new @property (no parentheses needed!)
        print(f"VAT on {product1.name}: R{product1.vat:.2f}")
        print(f"Total Price (Incl VAT): R{product1.price_including_vat:.2f}")
        
        # 4. Discount calculation
        discount_price = product1.apply_discount(10)
        print(f"Price after 10% discount: R{discount_price:.2f}")
        print("-" * 30)

        # 5. Demonstrating the class variable usage
        print(f"Current VAT Rate: {Product.VAT_RATE * 100}%")

    except ValueError as e:
        print(f"Error creating product: {e}")

if __name__ == "__main__":
    main()