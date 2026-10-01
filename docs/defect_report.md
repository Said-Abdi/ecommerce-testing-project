# Defect Report: DEF-001

| Field | Details |
|---|---|
| **Defect ID** | DEF-001 |
| **Title** | Decimal price is incorrectly truncated during checkout |
| **Severity** | High (Financial inaccuracy affecting revenue and user receipts) |
| **Priority** | High |
| **Component** | `src/checkout.py` (`CheckoutService.process_checkout`) |
| **Environment** | Python 3.11+, Pytest 7.4+ |

## Summary
When processing a checkout order where the discounted price contains fractional cent values (e.g., $89.99), the checkout service incorrectly cast intermediate monetary values to integer (`int()`), resulting in the loss of decimal cents ($89.00).

## Steps to Reproduce
1. Create a Product with price `$99.99`.
2. Add 1 item to `ShoppingCart`.
3. Process checkout applying a `10%` discount.
4. Inspect `CheckoutReceipt.final_total`.

## Expected Result
- Subtotal: `$99.99`
- Discount (10%): `$10.00`
- Shipping: `$0.00`
- **Final Total: `$89.99`**

## Actual Result
- **Final Total: `$89.00`** (Truncated `.99` cents).

## Root Cause
The legacy/faulty implementation executed integer type casting:
```python
final_price = int(subtotal - discount)