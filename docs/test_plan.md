# Test Plan — E-Commerce Checkout System

## 1. Objective
The objective of this test plan is to define the testing strategy, test scope, and quality engineering standards for the E-Commerce Checkout System to ensure functional correctness, decimal precision, and error resiliency.

## 2. Scope
### In Scope
- Product stock management and validation
- Shopping cart CRUD operations (add, remove, update quantity, clear)
- Subtotal, discount percentage (0–100%), and shipping fee calculations
- Final checkout receipt generation and decimal precision preservation
- Boundary Value Analysis (BVA) & Equivalence Partitioning (EP)
- Defect detection and regression verification for Decimal Truncation (DEF-001)

### Out of Scope
- Web UI & REST API controllers
- Database persistence layer
- Payment gateway integrations (Stripe/PayPal)

## 3. Testing Strategy
- **Framework:** Pytest with `pytest-cov`
- **Test Categories:** Unit, Functional, Negative, Boundary Value, Regression
- **Quality Gate:** Minimum 90% code coverage across `src/`

## 4. Entry and Exit Criteria
- **Entry Criteria:** Complete requirement specification and source code implementation.
- **Exit Criteria:** 100% test execution pass rate, >= 90% coverage, and resolution of all critical defects (DEF-001 verified fixed).