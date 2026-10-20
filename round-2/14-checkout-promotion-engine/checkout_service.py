from dataclasses import dataclass


@dataclass
class Quote:
    subtotal: int
    discount: int
    tax: int
    total: int


class CheckoutService:
    def __init__(self, store, promotions):
        self.store, self.promotions = store, promotions

    def quote(self, lines, code=None, tax_rate=0):
        if any(qty <= 0 or price < 0 for _, qty, price in lines):
            raise ValueError("invalid line")
        subtotal = sum(qty * price for _, qty, price in lines)
        discount = self.promotions.discount(lines, code, subtotal)
        taxable = subtotal - discount
        tax = round(taxable * tax_rate)
        return Quote(subtotal, discount, tax, taxable + tax)
