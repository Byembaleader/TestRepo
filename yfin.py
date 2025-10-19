import yfinance as yf, requests, pandas as pd
from bs4 import BeautifulSoup
import plotly.graph_objects as go

def get_revenue(url):
    s = BeautifulSoup(requests.get(url).text,"html.parser")
    df = pd.read_html(str(s.find_all("table")[1]))[0]
    df.columns = ["Date","Revenue"]
    df["Revenue"] = df["Revenue"].str.replace(r"\$|,","",regex=True)
    return df[df["Revenue"]!=""]

# Stock data
tsla, gme = yf.Ticker("TSLA").history(period="max").reset_index(), yf.Ticker("GME").history(period="max").reset_index()
# Revenue data
tsla_rev, gme_rev = get_revenue("https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"), get_revenue("https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue")

# Dashboards
for stock, rev, name in [(tsla, tsla_rev,"Tesla"), (gme, gme_rev,"GameStop")]:
    fig = go.Figure([go.Scatter(x=stock["Date"],y=stock["Close"],name=f"{name} Stock"),
                     go.Bar(x=rev["Date"],y=rev["Revenue"],name=f"{name} Revenue")])
    fig.update_layout(title=f"{name} Stock Price vs Revenue", xaxis_title="Date", yaxis_title="USD")
    fig.show()
