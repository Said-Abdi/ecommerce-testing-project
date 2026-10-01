"""Boundary Value Analysis (BVA) and Equivalence Partitioning (EP) tests."""
from decimal import Decimal
import pytest
from src.models import Product
from src.cart import ShoppingCart
from src.pricing import PricingEngine


@pytest.mark.boundary
@pytest.mark.parametrize("quantity,should_pass", [
    (0, False),    # Boundary below min valid (Invalid)
    (1, True),     # Minimum valid quantity
    (2, True),     # Nominal valid
    (10, True),    # Maximum available stock limit
    (11, False),   # Boundary above max stock limit (Invalid)
])
def test_bva_product_quantity(quantity, should_pass):
    cart = ShoppingCart()
    product = Product("P_BVA", "BVA Item", price="10.00", stock_quantity=10)

    if should_pass:
        cart.add_product(product, quantity)
        assert cart.items["P_BVA"].quantity == quantity
    else:
        with pytest.raises(ValueError):
            cart.add_product(product, quantity)


@pytest.mark.boundary
@pytest.mark.parametrize("discount,should_pass", [
    (-1, False),   # Boundary below 0 (Invalid)
    (0, True),     # Lower boundary (0%)
    (1, True),     # Just above lower boundary
    (99, True),    # Just below upper boundary
    (100, True),   # Upper boundary (100%)
    (101, False),  # Boundary above 100 (Invalid)
])
def test_bva_discount_percentages(discount, should_pass):
    subtotal = Decimal("100.00")
    if should_pass:
        amt = PricingEngine.calculate_discount(subtotal, discount)
        assert amt == Decimal(str(discount))
    else:
        with pytest.raises(ValueError):
            PricingEngine.calculate_discount(subtotal, discount)


@pytest.mark.boundary
@pytest.mark.parametrize("subtotal,expected_shipping", [
    # $0.01 below free shipping threshold
    (Decimal("49.99"), Decimal("10.00")),
    (Decimal("50.00"), Decimal("0.00")),  # Exact threshold value ($50.00)
    (Decimal("50.01"), Decimal("0.00")),  # $0.01 above free shipping threshold
])
def test_bva_free_shipping_threshold(subtotal, expected_shipping):
    shipping = PricingEngine.calculate_shipping(subtotal)
    assert shipping == expected_shipping
