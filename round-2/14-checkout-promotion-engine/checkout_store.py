class CheckoutStore:
    def __init__(self):
        self.promotions = {}

    def add_promotion(self, code, kind, value, minimum_cents=0, eligible_skus=None):
        from promotion import Promotion
        self.promotions[code] = Promotion(code, kind, value, minimum_cents, eligible_skus or set())

    def promotion(self, code):
        return self.promotions.get(code)
