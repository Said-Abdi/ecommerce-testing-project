"""Functional tests for end-to-end checkout scenarios & Defect DEF-001 verification."""
from decimal import Decimal
import pytest
from src.models import Product
from src.cart import ShoppingCart
from src.checkout import CheckoutService


@pytest.fixture
def checkout_service():
    return CheckoutService()


@pytest.mark.functional
def test_scenario_1_normal_purchase_below_free_shipping(checkout_service):
    """Scenario 1: Normal purchase below $50 threshold."""
    cart = ShoppingCart()
    p1 = Product("P1", "Mouse", "20.00", 10)
    cart.add_product(p1, 1)

    receipt = checkout_service.process_checkout(cart, discount_percentage=0)
    assert receipt.subtotal == Decimal("20.00")
    assert receipt.discount_amount == Decimal("0.00")
    assert receipt.shipping_fee == Decimal("10.00")
    assert receipt.final_total == Decimal("30.00")
    assert p1.stock_quantity == 9


@pytest.mark.functional
def test_scenario_2_purchase_with_discount(checkout_service):
    """Scenario 2: Purchase with 20% discount applied."""
    cart = ShoppingCart()
    p1 = Product("P2", "Headset", "100.00", 5)
    cart.add_product(p1, 1)

    receipt = checkout_service.process_checkout(cart, discount_percentage=20)
    assert receipt.subtotal == Decimal("100.00")
    assert receipt.discount_amount == Decimal("20.00")
    assert receipt.shipping_fee == Decimal("0.00")  # $100 >= $50
    assert receipt.final_total == Decimal("80.00")


@pytest.mark.functional
def test_scenario_3_purchase_above_free_shipping(checkout_service):
    """Scenario 3: Purchase equal or above $50 free shipping threshold."""
    cart = ShoppingCart()
    p1 = Product("P3", "Desk Lamp", "50.00", 5)
    cart.add_product(p1, 1)

    receipt = checkout_service.process_checkout(cart, discount_percentage=0)
    assert receipt.shipping_fee == Decimal("0.00")
    assert receipt.final_total == Decimal("50.00")


@pytest.mark.functional
def test_scenario_4_multiple_products_checkout(checkout_service):
    """Scenario 5: Checkout with multiple items."""
    cart = ShoppingCart()
    p1 = Product("P1", "Item 1", "15.00", 10)
    p2 = Product("P2", "Item 2", "25.00", 10)
    cart.add_product(p1, 2)  # 30.00
    cart.add_product(p2, 1)  # 25.00 -> total 55.00

    receipt = checkout_service.process_checkout(cart, discount_percentage=10)
    # subtotal=55.00, discount=5.50, shipping=0.00 -> 49.50
    assert receipt.subtotal == Decimal("55.00")
    assert receipt.discount_amount == Decimal("5.50")
    assert receipt.shipping_fee == Decimal("0.00")
    assert receipt.final_total == Decimal("49.50")


@pytest.mark.regression
@pytest.mark.functional
def test_def_001_decimal_truncation_detection_and_fix(checkout_service):
    """
    Demonstrates DEF-001: Decimal price truncation defect.
    Expected: $89.99
    Buggy behavior (with truncation): $89.00
    Correct behavior: $89.99
    """
    cart = ShoppingCart()
    product = Product("P_DECIMAL", "Monitor", "99.99", stock_quantity=10)
    cart.add_product(product, 1)

    # 1. Reproduce Defect with flag enabled
    buggy_receipt = checkout_service.process_checkout(
        cart, discount_percentage=10, enable_buggy_truncation=True)
    # 99.99 - 10.00 (10% discount = 10.00) + 0.00 = 89.99
    assert buggy_receipt.final_total == Decimal(
        "89.00")  # Truncated bug verified!

    # Reset product stock for clean rerun
    product.restore_stock(1)

    # 2. Verify Fixed Behavior (Production Mode)
    fixed_receipt = checkout_service.process_checkout(
        cart, discount_percentage=10, enable_buggy_truncation=False)
    assert fixed_receipt.final_total == Decimal(
        "89.99")  # Decimal cents preserved!
