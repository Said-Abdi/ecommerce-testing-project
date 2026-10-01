"""Pricing engine for discount and shipping calculations."""
from decimal import Decimal
import logging

logger = logging.getLogger("ecommerce.pricing")


class PricingEngine:
    """Handles discount and shipping calculation rules."""

    FREE_SHIPPING_THRESHOLD = Decimal("50.00")
    STANDARD_SHIPPING_FEE = Decimal("10.00")

    @staticmethod
    def calculate_discount(subtotal: Decimal, discount_percentage: Decimal | float | int) -> Decimal:
        """Calculates monetary discount amount based on subtotal and percentage."""
        if subtotal < Decimal("0.00"):
            raise ValueError("Subtotal cannot be negative.")

        try:
            pct = Decimal(str(discount_percentage))
        except Exception as err:
            raise ValueError(
                f"Invalid discount percentage format: {discount_percentage}") from err

        if pct < Decimal("0.00") or pct > Decimal("100.00"):
            raise ValueError(
                f"Discount percentage must be between 0 and 100. Got: {pct}")

        discount_amount = (subtotal * (pct / Decimal("100.00"))
                           ).quantize(Decimal("0.01"))
        logger.debug("Discount calculated: subtotal=$%s, percentage=%s%% -> discount=$%s",
                     subtotal, pct, discount_amount)
        return discount_amount

    @staticmethod
    def calculate_shipping(subtotal: Decimal) -> Decimal:
        """Calculates shipping costs based on order subtotal threshold."""
        if subtotal < Decimal("0.00"):
            raise ValueError("Subtotal cannot be negative.")

        if subtotal >= PricingEngine.FREE_SHIPPING_THRESHOLD:
            logger.debug("Free shipping applied for subtotal $%s (>= $%s)",
                         subtotal, PricingEngine.FREE_SHIPPING_THRESHOLD)
            return Decimal("0.00")

        logger.debug("Standard shipping fee $%s applied for subtotal $%s (< $%s)",
                     PricingEngine.STANDARD_SHIPPING_FEE, subtotal, PricingEngine.FREE_SHIPPING_THRESHOLD)
        return PricingEngine.STANDARD_SHIPPING_FEE
