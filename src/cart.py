"""Shopping Cart and Cart Item domain entities."""
from decimal import Decimal
import logging
from typing import Dict
from src.models import Product

logger = logging.getLogger("ecommerce.cart")


class CartItem:
    """Represents an item within a shopping cart."""

    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Item quantity must be greater than zero.")
        if quantity > product.stock_quantity:
            raise ValueError(
                f"Requested quantity {quantity} exceeds available stock {product.stock_quantity}.")

        self.product = product
        self.quantity = quantity

    @property
    def subtotal(self) -> Decimal:
        """Calculates total price for this cart item line."""
        return (self.product.price * Decimal(self.quantity)).quantize(Decimal("0.01"))


class ShoppingCart:
    """Manages shopping cart operations: add, remove, update, and subtotal calculation."""

    def __init__(self):
        self._items: Dict[str, CartItem] = {}
        logger.debug("Initialized new empty ShoppingCart.")

    @property
    def items(self) -> Dict[str, CartItem]:
        return dict(self._items)

    def add_product(self, product: Product, quantity: int = 1) -> None:
        """Adds a product or increases its quantity in the cart."""
        if not isinstance(product, Product):
            raise TypeError("Invalid product object provided.")
        if quantity <= 0:
            raise ValueError("Quantity to add must be greater than zero.")

        current_qty = self._items[product.product_id].quantity if product.product_id in self._items else 0
        new_qty = current_qty + quantity

        if new_qty > product.stock_quantity:
            logger.warning("Failed to add %d of %s: Stock limit (%d) exceeded.",
                           quantity, product.product_id, product.stock_quantity)
            raise ValueError(
                f"Cannot add {quantity} units. Total requested ({new_qty}) exceeds stock ({product.stock_quantity}).")

        if product.product_id in self._items:
            self._items[product.product_id].quantity = new_qty
        else:
            self._items[product.product_id] = CartItem(product, new_qty)

        logger.info("Added %d x %s to cart. Total in cart: %d",
                    quantity, product.name, new_qty)

    def remove_product(self, product_id: str) -> None:
        """Removes a product completely from the cart."""
        if product_id not in self._items:
            raise KeyError(f"Product '{product_id}' non-existent in cart.")
        removed = self._items.pop(product_id)
        logger.info("Removed product %s (%s) from cart.",
                    removed.product.name, product_id)

    def update_quantity(self, product_id: str, new_quantity: int) -> None:
        """Updates the quantity of an existing product in the cart."""
        if product_id not in self._items:
            raise KeyError(f"Product '{product_id}' non-existent in cart.")
        if new_quantity <= 0:
            raise ValueError(
                "New quantity must be greater than zero. Use remove_product to drop item.")

        cart_item = self._items[product_id]
        if new_quantity > cart_item.product.stock_quantity:
            raise ValueError(
                f"Requested quantity {new_quantity} exceeds stock ({cart_item.product.stock_quantity}).")

        cart_item.quantity = new_quantity
        logger.info("Updated product %s quantity to %d.",
                    product_id, new_quantity)

    def calculate_subtotal(self) -> Decimal:
        """Calculates total value of items before discounts and shipping."""
        subtotal = sum(
            (item.subtotal for item in self._items.values()), Decimal("0.00"))
        return subtotal.quantize(Decimal("0.01"))

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def clear(self) -> None:
        self._items.clear()
        logger.info("Shopping cart cleared.")
