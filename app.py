import streamlit as st
import yfinance as yf
import plotly.express as px

# ------------------------
# Page Config
# ------------------------
st.set_page_config(
    page_title="Stock Intelligence Platform",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Intelligence Platform")
st.markdown("Helping retail investors make data-driven investment decisions.")

# ------------------------
# Suggested Stocks
# ------------------------
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

# ------------------------
# Sidebar
# ------------------------
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

compare_stock = st.sidebar.selectbox(
    "Compare With",
    ["None", "AAPL", "MSFT", "NVDA", "AMZN", "TSLA", "META"]
)

# ------------------------
# Helper Functions
# ------------------------
def format_market_cap(value):
    if isinstance(value, (int, float)):
        if value >= 1_000_000_000_000:
            return f"${value/1_000_000_000_000:.2f}T"
        elif value >= 1_000_000_000:
            return f"${value/1_000_000_000:.2f}B"
        elif value >= 1_000_000:
            return f"${value/1_000_000:.2f}M"
    return "N/A"


def calculate_risk(hist):
    volatility = hist["Close"].pct_change().std()

    if volatility < 0.015:
        return "🟢 Low"
    elif volatility < 0.03:
        return "🟡 Medium"
    else:
        return "🔴 High"


# ------------------------
# Main App
# ------------------------
try:

    stock = yf.Ticker(ticker_input)

    info = stock.info
    hist = stock.history(period=period)

    if hist.empty:
        st.error("No stock data found.")
        st.stop()

    current_price = info.get("currentPrice", "N/A")
    market_cap = info.get("marketCap", "N/A")
    high_52 = info.get("fiftyTwoWeekHigh", "N/A")
    low_52 = info.get("fiftyTwoWeekLow", "N/A")

    company_name = info.get("longName", ticker_input)

    st.subheader(company_name)

    # Daily Change %
    if len(hist) > 1:
        daily_change = (
            (hist["Close"].iloc[-1] - hist["Close"].iloc[-2])
            / hist["Close"].iloc[-2]
        ) * 100
    else:
        daily_change = 0

    # ------------------------
    # Metrics
    # ------------------------
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Current Price",
        f"${current_price}"
    )

    col2.metric(
        "Daily Change %",
        f"{daily_change:.2f}%"
    )

    col3.metric(
        "Market Cap",
        format_market_cap(market_cap)
    )

    col4.metric(
        "52W High",
        high_52
    )

    col5.metric(
        "52W Low",
        low_52
    )

    st.markdown("---")

    # ------------------------
    # Health Score
    # ------------------------
    latest_close = hist["Close"].iloc[-1]
    first_close = hist["Close"].iloc[0]

    return_pct = ((latest_close - first_close) / first_close) * 100

    score = max(min(int(return_pct + 50), 100), 0)

    st.subheader("📊 Stock Health Score")

    st.progress(score)

    st.write(f"Health Score: **{score}/100**")

    # ------------------------
    # Risk Analysis
    # ------------------------
    risk_level = calculate_risk(hist)

    st.subheader("⚠️ Risk Analysis")
    st.write(f"Risk Level: **{risk_level}**")

    # ------------------------
    # AI Insight
    # ------------------------
    st.subheader("🤖 AI Investment Insight")

    if return_pct > 15:
        insight = (
            f"{company_name} has shown strong performance with a "
            f"return of {return_pct:.2f}% during the selected period. "
            f"The stock is demonstrating bullish momentum."
        )
    elif return_pct > 5:
        insight = (
            f"{company_name} has delivered moderate gains of "
            f"{return_pct:.2f}% during the selected period."
        )
    elif return_pct > -5:
        insight = (
            f"{company_name} has traded relatively sideways "
            f"during the selected period."
        )
    else:
        insight = (
            f"{company_name} has declined by "
            f"{abs(return_pct):.2f}% during the selected period. "
            f"Investors should analyze the reasons carefully."
        )

    st.info(insight)

    # ------------------------
    # Company Description
    # ------------------------
    summary = info.get("longBusinessSummary", "")

    if summary:
        st.subheader("🏢 About the Company")
        st.write(summary[:700] + "...")

    # ------------------------
    # Price Chart
    # ------------------------
    st.subheader("📈 Stock Price Trend")

    fig = px.line(
        hist,
        x=hist.index,
        y="Close",
        title=f"{ticker_input} Price Trend"
    )

    # Comparison Stock
    if compare_stock != "None":

        compare_hist = yf.Ticker(compare_stock).history(
            period=period
        )

        if not compare_hist.empty:

            fig.add_scatter(
                x=compare_hist.index,
                y=compare_hist["Close"],
                mode="lines",
                name=compare_stock
            )

    fig.update_layout(
        template="plotly_white",
        height=600,
        xaxis_title="Date",
        yaxis_title="Price"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ------------------------
    # Recent Data
    # ------------------------
    st.subheader("📋 Recent Data")

    st.dataframe(
        hist.tail(10),
        use_container_width=True
    )

except Exception as e:
    st.error(f"Error loading stock data: {e}")
