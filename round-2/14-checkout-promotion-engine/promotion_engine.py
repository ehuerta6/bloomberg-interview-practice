class PromotionEngine:
    def __init__(self, store):
        self.store = store

    def discount(self, lines, code, subtotal):
        promotion = self.store.promotion(code) if code else None
        if promotion is None or subtotal < promotion.minimum_cents:
            return 0
        eligible = sum(qty * price for sku, qty, price in lines
                       if not promotion.eligible_skus or sku in promotion.eligible_skus)
        if promotion.eligible_skus and eligible == 0:
            return 0
        amount = subtotal * promotion.value // 100 if promotion.kind == "percent" else promotion.value
        return min(max(0, amount), subtotal)
