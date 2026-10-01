import streamlit as st
from decimal import Decimal
from src.models import Product
from src.cart import ShoppingCart
from src.checkout import CheckoutService
from unittest.mock import Mock
from src.payment import PaymentProcessor, StripePaymentGateway

st.set_page_config(page_title="E-Commerce Testing App", layout="wide")
st.title("🛒 E-Commerce System & Payment Interface")

# State Management (Khadka keydinta session-ka)
if "cart" not in st.session_state:
    st.session_state.cart = ShoppingCart()

if "products" not in st.session_state:
    st.session_state.products = {
        "P1": Product("P1", "Laptop HP", Decimal("750.00"), 5),
        "P2": Product("P2", "Wireless Mouse", Decimal("25.00"), 10),
        "P3": Product("P3", "Mechanical Keyboard", Decimal("60.00"), 8),
    }

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📦 Alaabta Diyarka Ah (Inventory)")
    for p_id, prod in st.session_state.products.items():
        c1, c2, c3, c4 = st.columns([2, 2, 2, 2])
        c1.write(f"**{prod.name}**")
        c2.write(f"${prod.price}")
        c3.write(f"Stock: {prod.stock_quantity}")
        if c4.button(f"Ku dar Cart", key=p_id):
            try:
                st.session_state.cart.add_item(prod, 1)
                st.success(f"{prod.name} waa lagu daray cart-ka!")
                st.rerun()
            except Exception as e:
                st.error(str(e))

with col2:
    st.subheader("🛍️ Kaanbadhkaaga (Shopping Cart)")
    cart_items = st.session_state.cart.items
    if not cart_items:
        st.info("Cart-ku waa eber.")
    else:
        for p_id, item in cart_items.items():
            st.write(
                f"• **{item.product.name}** x {item.quantity} = **${item.total_price}**")

        st.markdown("---")
        subtotal = st.session_state.cart.calculate_subtotal()
        st.write(f"**Subtotal:** ${subtotal}")

        # Payment Mock UI
        st.subheader("💳 Lacag Bixinta (Mock Payment)")
        card_token = st.text_input("Card Token", value="tok_visa_valid")
        discount_pct = st.number_input(
            "Discount %", min_value=0, max_value=100, value=0)

        if st.button("Bixi Lacagta & Bixi Order-ka"):
            mock_gateway = Mock(spec=StripePaymentGateway)
            mock_gateway.charge.return_value = {
                "status": "succeeded", "id": "tx_123456789"}

            processor = PaymentProcessor(gateway=mock_gateway)
            pay_result = processor.process_payment(subtotal, card_token)

            if pay_result["success"]:
                st.balloons()
                st.success(
                    f"✅ Lacagtu waxay ku bixtay guul! Transaction ID: {pay_result['transaction_id']}")
                st.session_state.cart.clear()
            else:
                st.error(
                    f"❌ Lacag bixintu waxay ku guuldarraysatay: {pay_result['error']}")
