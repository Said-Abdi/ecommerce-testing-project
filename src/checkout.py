"""Checkout service facilitating transaction execution and receipt generation."""
from decimal import Decimal
import logging
from dataclasses import dataclass
from typing import Dict
from src.cart import ShoppingCart
from src.pricing import PricingEngine

logger = logging.getLogger("ecommerce.checkout")


@dataclass
class CheckoutReceipt:
    """Immutable checkout summary receipt data structure."""
    item_count: int
    subtotal: Decimal
    discount_percentage: Decimal
    discount_amount: Decimal
    shipping_fee: Decimal
    final_total: Decimal


class CheckoutService:
    """Orchestrates checkout processing and stock reconciliation."""

    def __init__(self, pricing_engine: PricingEngine | None = None):
        self.pricing_engine = pricing_engine or PricingEngine()

    def process_checkout(
        self,
        cart: ShoppingCart,
        discount_percentage: Decimal | float | int = 0,
        enable_buggy_truncation: bool = False
    ) -> CheckoutReceipt:
        """Processes shopping cart checkout and returns an itemized receipt.

        Note:
            `enable_buggy_truncation` is included specifically for testing/demonstration
            of DEF-001 (Decimal Truncation Defect). Production flow must default to False.
        """
        if cart.is_empty():
            logger.error("Checkout attempt on empty cart rejected.")
            raise ValueError("Cannot checkout with an empty cart.")

        subtotal = cart.calculate_subtotal()
        discount_pct = Decimal(str(discount_percentage))
        discount_amount = self.pricing_engine.calculate_discount(
            subtotal, discount_pct)
        shipping_fee = self.pricing_engine.calculate_shipping(subtotal)

        raw_total = subtotal - discount_amount + shipping_fee

        if enable_buggy_truncation:
            # INTENTIONAL BUG REPRODUCTION (DEF-001):
            # Casting intermediate value to int() truncates decimal cents (e.g., 89.99 -> 89.00)
            final_total = Decimal(int(raw_total)).quantize(Decimal("0.01"))
            logger.warning(
                "DEF-001 BUG TRIGGERED: Truncated $%s to $%s", raw_total, final_total)
        else:
            # CORRECT IMPLEMENTATION:
            # Decimal precision maintained throughout monetary arithmetic
            final_total = raw_total.quantize(Decimal("0.01"))

        # Deduct stock for all purchased items
        for cart_item in cart.items.values():
            cart_item.product.reduce_stock(cart_item.quantity)

        receipt = CheckoutReceipt(
            item_count=sum(item.quantity for item in cart.items.values()),
            subtotal=subtotal,
            discount_percentage=discount_pct,
            discount_amount=discount_amount,
            shipping_fee=shipping_fee,
            final_total=final_total
        )

        logger.info(
            "Checkout successfully processed. Receipt total: $%s", receipt.final_total)
        return receipt
