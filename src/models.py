"""Data models for Product domain entity."""
from decimal import Decimal
import logging

logger = logging.getLogger("ecommerce.models")


class Product:
    """Represents an e-commerce product in stock."""

    def __init__(self, product_id: str, name: str, price: Decimal | float | str, stock_quantity: int):
        if not product_id or not isinstance(product_id, str):
            raise ValueError("Product ID must be a non-empty string.")

        if not name or not isinstance(name, str):
            raise ValueError("Product name must be a non-empty string.")

        try:
            decimal_price = Decimal(str(price))
        except Exception as err:
            raise ValueError(f"Invalid price format: {price}") from err

        if decimal_price <= Decimal("0.00"):
            raise ValueError(
                "Product price must be strictly greater than zero.")

        if not isinstance(stock_quantity, int) or stock_quantity < 0:
            raise ValueError("Stock quantity must be a non-negative integer.")

        self.product_id = product_id
        self.name = name
        self.price = decimal_price.quantize(Decimal("0.01"))
        self.stock_quantity = stock_quantity

        logger.debug("Initialized Product: %s (%s) @ $%s, stock=%d",
                     self.name, self.product_id, self.price, self.stock_quantity)

    def reduce_stock(self, quantity: int) -> None:
        """Deducts stock quantity after validation."""
        if quantity <= 0:
            raise ValueError("Quantity to reduce must be greater than zero.")
        if quantity > self.stock_quantity:
            raise ValueError(
                f"Insufficient stock for {self.name}. Available: {self.stock_quantity}, requested: {quantity}")
        self.stock_quantity -= quantity
        logger.info("Stock reduced for %s. New stock: %d",
                    self.product_id, self.stock_quantity)

    def restore_stock(self, quantity: int) -> None:
        """Restores stock quantity."""
        if quantity <= 0:
            raise ValueError("Quantity to restore must be greater than zero.")
        self.stock_quantity += quantity
        logger.info("Stock restored for %s. New stock: %d",
                    self.product_id, self.stock_quantity)
