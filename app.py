import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Invoice Generator",
    page_icon="🧾",
    layout="wide"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
.main{
    background-color:#0E1117;
}
.hero{
    padding:20px;
    border-radius:15px;
    background:linear-gradient(135deg,#2563EB,#7C3AED);
    color:white;
    text-align:center;
    margin-bottom:20px;
}
.card{
    background:#1E293B;
    padding:20px;
    border-radius:12px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="hero">
<h1>🧾 Smart Invoice Generator</h1>
<p>Generate GST Invoices with Discounts & Billing Summary</p>
</div>
""", unsafe_allow_html=True)

# ---------- Customer Details ----------
st.subheader("👤 Customer Details")

col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")

with col2:
    address = st.text_area("Address")
    gst_no = st.text_input("GST Number")

invoice_no = st.number_input("Invoice Number", min_value=1)

st.divider()

# ---------- Product Entry ----------
st.subheader("📦 Product Details")

num_items = st.number_input(
    "Number of Items",
    min_value=1,
    value=1
)

items = []

for i in range(num_items):
    st.markdown(f"### Item {i+1}")

    c1, c2, c3 = st.columns(3)

    with c1:
        item_name = st.text_input(
            f"Item Name {i}",
            key=f"name{i}"
        )

    with c2:
        quantity = st.number_input(
            f"Quantity {i}",
            min_value=1,
            value=1,
            key=f"qty{i}"
        )

    with c3:
        rate = st.number_input(
            f"Rate {i}",
            min_value=0.0,
            key=f"rate{i}"
        )

    total = quantity * rate

    items.append(
        [item_name, quantity, rate, total]
    )

st.divider()

# ---------- Payment ----------
st.subheader("💳 Payment Method")

payment = st.radio(
    "Select Payment Method",
    ["UPI", "Card", "Cash"]
)

discount_rate = {
    "UPI": 0.10,
    "Card": 0.07,
    "Cash": 0.03
}

carry_bag = st.checkbox(
    "Add Carry Bag (₹10)"
)

# ---------- Generate Invoice ----------
if st.button("Generate Invoice"):

    df = pd.DataFrame(
        items,
        columns=[
            "Item",
            "Qty",
            "Rate",
            "Amount"
        ]
    )

    subtotal = df["Amount"].sum()

    discount = subtotal * discount_rate[payment]

    after_discount = subtotal - discount

    gst = after_discount * 0.18

    bag_cost = 10 if carry_bag else 0

    grand_total = (
        after_discount
        + gst
        + bag_cost
        + 1
    )

    st.success("Invoice Generated Successfully!")

    st.subheader("📄 Invoice")

    st.write(
        f"**Customer:** {customer_name}"
    )

    st.write(
        f"**Invoice No:** {invoice_no}"
    )

    st.markdown("### 📦 Purchased Items")

    st.table(df)
    st.markdown("### Billing Summary")

st.markdown("## 💰 Billing Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Subtotal", f"₹{subtotal:,.2f}")

with c2:
    st.metric("Discount", f"₹{discount:,.2f}")

with c3:
    st.metric("GST (18%)", f"₹{gst:,.2f}")

with c4:
    st.metric("Grand Total", f"₹{grand_total:,.2f}")