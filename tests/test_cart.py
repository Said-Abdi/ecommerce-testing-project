from decimal import Decimal
import pytest
from src.cart import ShoppingCart, CartItem
from src.models import Product


def test_cart_item_operations():
    product = Product(product_id="P1", name="Laptop",
                      price=Decimal("100.00"), stock_quantity=10)
    item = CartItem(product, quantity=2)

    assert item.subtotal == Decimal("200.00")

    # Exceptions for CartItem
    with pytest.raises(ValueError):
        CartItem(product, quantity=0)

    with pytest.raises(ValueError):
        CartItem(product, quantity=15)


def test_shopping_cart_full_coverage():
    cart = ShoppingCart()
    product1 = Product(product_id="P1", name="Mouse",
                       price=Decimal("20.00"), stock_quantity=5)
    product2 = Product(product_id="P2", name="Keyboard",
                       price=Decimal("50.00"), stock_quantity=3)

    # 1. Properties and empty check
    assert cart.is_empty() is True
    assert cart.items == {}

    # 2. Add products (Normal flow)
    cart.add_product(product1, quantity=2)
    # Increase existing quantity (Line 68-69)
    cart.add_product(product1, quantity=1)
    assert cart.is_empty() is False

    # 3. Add invalid product type or quantity
    with pytest.raises(TypeError):
        cart.add_product("NotAProduct", 1)

    with pytest.raises(ValueError):
        cart.add_product(product1, quantity=0)

    # Exceed stock on add (Line 57)
    with pytest.raises(ValueError):
        cart.add_product(product1, quantity=10)

    # 4. Calculate subtotal
    cart.add_product(product2, quantity=1)
    assert cart.calculate_subtotal() == Decimal("110.00")  # (3 * 20) + (1 * 50)

    # 5. Update quantity
    cart.update_quantity("P1", 2)
    with pytest.raises(KeyError):
        cart.update_quantity("NON_EXISTENT", 2)

    with pytest.raises(ValueError):
        cart.update_quantity("P1", 0)

    with pytest.raises(ValueError):
        cart.update_quantity("P1", 20)  # Exceed stock

    # 6. Remove product
    cart.remove_product("P2")
    with pytest.raises(KeyError):
        cart.remove_product("P2")

    # 7. Clear cart (Lines 99-100)
    cart.clear()
    assert cart.is_empty() is True
