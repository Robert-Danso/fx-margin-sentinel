import streamlit as st
import pandas as pd
from main import fetch_rates, add_buffer

st.set_page_config(page_title="FX Margin Sentinel", page_icon="📈", layout="centered")

st.title("📈 FX Margin Sentinel")
st.caption("Dynamic Hedging & Import Volatility Protection Engine")

st.markdown("---")

# User inputs: Buffer slider & order volume
col1, col2 = st.columns(2)
with col1:
    buffer_val = st.slider("Safety Hedge Buffer (%)", min_value=1.0, max_value=12.0, value=5.0, step=0.5)
with col2:
    order_usd = st.number_input("Invoice Size (USD)", min_value=100, max_value=100000, value=2500, step=100)

buffer_decimal = buffer_val / 100.0

if st.button("Calculate Hedge Rates", type="primary"):
    with st.spinner("Querying live FX markets..."):
        try:
            raw_rates = fetch_rates()
            df = add_buffer(raw_rates, buffer_percent=buffer_decimal)
            
            st.subheader("Current Market & Hedged Rates")
            st.dataframe(df, use_container_width=True)
            
            # Dollar-specific exposure breakdown
            usd_spot = raw_rates.get("USD_GHS", 0.0)
            usd_hedged = round(usd_spot * (1 + buffer_decimal), 4)
            unhedged_cost = round(order_usd * usd_spot, 2)
            hedged_cost = round(order_usd * usd_hedged, 2)
            buffer_pool = round(hedged_cost - unhedged_cost, 2)
            
            st.markdown("---")
            st.subheader(f"Invoice Exposure Analysis (${order_usd:,})")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Spot Cost (GHS)", f"GH₵ {unhedged_cost:,.2f}")
            m2.metric(f"Hedged (+{buffer_val}%)", f"GH₵ {hedged_cost:,.2f}")
            m3.metric("Safety Buffer Pool", f"GH₵ {buffer_pool:,.2f}")
            
            st.success("Target pricing locked. Re-run prior to supplier invoice settlement.")
        except Exception as e:
            st.error(f"Error fetching live data: {e}")