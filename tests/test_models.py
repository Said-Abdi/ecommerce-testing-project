from decimal import Decimal
import pytest
from src.models import Product


def test_models_full_coverage():
    # 1. Invalid price format
    with pytest.raises(ValueError, match="Invalid price format"):
        Product(product_id="P1", name="Test Product",
                price="invalid_price", stock_quantity=10)

    product = Product(product_id="P1", name="Laptop",
                      price=Decimal("100.00"), stock_quantity=10)

    # 2. reduce_stock() normal & edge cases
    product.reduce_stock(3)
    assert product.stock_quantity == 7

    with pytest.raises(ValueError, match="Quantity to reduce must be greater than zero."):
        product.reduce_stock(0)

    with pytest.raises(ValueError, match="Insufficient stock"):
        product.reduce_stock(20)

    # 3. restore_stock() normal & edge cases
    product.restore_stock(5)
    assert product.stock_quantity == 12

    with pytest.raises(ValueError, match="Quantity to restore must be greater than zero."):
        product.restore_stock(-1)
