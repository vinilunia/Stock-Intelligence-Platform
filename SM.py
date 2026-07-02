import streamlit as st
import yfinance as yf
import plotly.express as px

st.set_page_config(
    page_title="Global Equity Explorer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Global Equity Explorer")
st.markdown("Track stocks worldwide using Yahoo Finance")

popular_stocks = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Google": "GOOGL",
    "Meta": "META",
    "Reliance Industries": "RELIANCE.NS",
    "Tata Consultancy Services": "TCS.NS",
    "Infosys": "INFY.NS"
}

st.sidebar.header("Stock Selection")

suggestion = st.sidebar.selectbox(
    "Suggested Stocks",
    list(popular_stocks.keys())
)

ticker_input = st.sidebar.text_input(
    "Or Enter Stock Symbol",
    value=popular_stocks[suggestion]
)

period = st.sidebar.selectbox(
    "Select Time Period",
    ["1mo", "3mo", "6mo", "1y", "5y"]
)

try:
    stock = yf.Ticker(ticker_input)

    info = stock.info
    hist = stock.history(period=period)

    current_price = info.get("currentPrice", "N/A")
    market_cap = info.get("marketCap", "N/A")
    high_52 = info.get("fiftyTwoWeekHigh", "N/A")
    low_52 = info.get("fiftyTwoWeekLow", "N/A")

    st.subheader(f"{info.get('longName', ticker_input)}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Current Price",
        f"${current_price}"
    )

    col2.metric(
        "Market Cap",
        f"{market_cap:,}" if isinstance(market_cap, int) else market_cap
    )

    col3.metric(
        "52W High",
        high_52
    )

    col4.metric(
        "52W Low",
        low_52
    )

    st.markdown("---")

    fig = px.line(
        hist,
        x=hist.index,
        y="Close",
        title=f"{ticker_input} Price Trend"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Recent Data")

    st.dataframe(
        hist.tail(10),
        use_container_width=True
    )

except Exception as e:
    st.error(f"Error loading stock data: {e}")
