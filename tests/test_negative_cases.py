"""Negative tests covering error handling and safety constraints."""
from decimal import Decimal
import pytest
from src.models import Product
from src.cart import ShoppingCart
from src.pricing import PricingEngine
from src.checkout import CheckoutService


@pytest.mark.negative
def test_product_creation_invalid_id():
    with pytest.raises(ValueError, match="Product ID must be a non-empty string"):
        Product(product_id="", name="Valid", price="10.00", stock_quantity=5)


@pytest.mark.negative
def test_product_creation_invalid_name():
    with pytest.raises(ValueError, match="Product name must be a non-empty string"):
        Product(product_id="P1", name="", price="10.00", stock_quantity=5)


@pytest.mark.negative
def test_product_creation_negative_price():
    with pytest.raises(ValueError, match="must be strictly greater than zero"):
        Product(product_id="P1", name="Product",
                price="-10.00", stock_quantity=5)


@pytest.mark.negative
def test_product_creation_zero_price():
    with pytest.raises(ValueError, match="must be strictly greater than zero"):
        Product(product_id="P1", name="Product",
                price="0.00", stock_quantity=5)


@pytest.mark.negative
def test_product_creation_negative_stock():
    with pytest.raises(ValueError, match="must be a non-negative integer"):
        Product(product_id="P1", name="Product",
                price="10.00", stock_quantity=-5)


@pytest.mark.negative
def test_cart_add_negative_quantity():
    cart = ShoppingCart()
    p = Product("P1", "Item", "10.00", 10)
    with pytest.raises(ValueError, match="Quantity to add must be greater than zero"):
        cart.add_product(p, quantity=-1)


@pytest.mark.negative
def test_cart_add_zero_quantity():
    cart = ShoppingCart()
    p = Product("P1", "Item", "10.00", 10)
    with pytest.raises(ValueError, match="Quantity to add must be greater than zero"):
        cart.add_product(p, quantity=0)


@pytest.mark.negative
def test_cart_add_exceeding_stock():
    cart = ShoppingCart()
    p = Product("P1", "Item", "10.00", stock_quantity=3)
    with pytest.raises(ValueError, match="exceeds stock"):
        cart.add_product(p, quantity=5)


@pytest.mark.negative
def test_cart_remove_non_existent_product():
    cart = ShoppingCart()
    with pytest.raises(KeyError, match="non-existent in cart"):
        cart.remove_product("NON_EXISTENT_ID")


@pytest.mark.negative
def test_cart_update_non_existent_product():
    cart = ShoppingCart()
    with pytest.raises(KeyError, match="non-existent in cart"):
        cart.update_quantity("NON_EXISTENT_ID", 2)


@pytest.mark.negative
def test_cart_update_quantity_exceeding_stock():
    cart = ShoppingCart()
    p = Product("P1", "Item", "10.00", stock_quantity=3)
    cart.add_product(p, 2)
    with pytest.raises(ValueError, match="exceeds stock"):
        cart.update_quantity("P1", 10)


@pytest.mark.negative
def test_discount_negative_percentage():
    with pytest.raises(ValueError, match="must be between 0 and 100"):
        PricingEngine.calculate_discount(Decimal("100.00"), -10)


@pytest.mark.negative
def test_discount_exceeding_100_percent():
    with pytest.raises(ValueError, match="must be between 0 and 100"):
        PricingEngine.calculate_discount(Decimal("100.00"), 105)


@pytest.mark.negative
def test_checkout_empty_cart():
    cart = ShoppingCart()
    checkout = CheckoutService()
    with pytest.raises(ValueError, match="Cannot checkout with an empty cart"):
        checkout.process_checkout(cart)
