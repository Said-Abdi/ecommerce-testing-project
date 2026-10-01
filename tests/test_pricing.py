from decimal import Decimal
import pytest
from src.pricing import PricingEngine


def test_pricing_basic_calculations():
    # Basic discount test
    discount = PricingEngine.calculate_discount(Decimal("100.00"), 10)
    assert discount == Decimal("10.00")

    # Free shipping test
    shipping = PricingEngine.calculate_shipping(Decimal("60.00"))
    assert shipping == Decimal("0.00")

    # Standard shipping test
    shipping_std = PricingEngine.calculate_shipping(Decimal("30.00"))
    assert shipping_std == Decimal("10.00")


def test_pricing_missing_coverage():
    # 1. Negative subtotal in calculate_discount
    with pytest.raises(ValueError, match="Subtotal cannot be negative."):
        PricingEngine.calculate_discount(Decimal("-10.00"), 10)

    # 2. Invalid discount percentage format
    with pytest.raises(ValueError, match="Invalid discount percentage format"):
        PricingEngine.calculate_discount(Decimal("100.00"), "invalid_pct")

    # 3. Negative subtotal in calculate_shipping
    with pytest.raises(ValueError, match="Subtotal cannot be negative."):
        PricingEngine.calculate_shipping(Decimal("-5.00"))
