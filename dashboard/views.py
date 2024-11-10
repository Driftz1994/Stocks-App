from django.shortcuts import render, redirect
import yfinance as yf 
# Create your views here.

tickers = ["AAPL", "NVDA", "GOOGL", "MSFT", "BAC", "META", "AMZN", "NFLX", "ADBE", "TSLA", "JPM", "CRM", "NKE", "QCOM"]

names = ['Apple Inc.', 'NVIDIA Corporation', 'Alphabet Inc.', 'Microsoft Corporation',
         'Bank of America Corporation', 'Meta Platforms, Inc.', 'Amazon.com, Inc.', 
         'Netflix, Inc.', 'Adobe Inc', 'Tesla, Inc', 'JPMorgan Chase & Co.',
         'Salesforce, Inc', 'Cisco Systems, Inc.', 'Nike, Inc.', 'QUALCOMM Incorporated']

def home(request):
    return redirect("dashboard:display_ticker", "AAPL")

def retrieve_data(ticker):
    ticker_obj = yf.Ticker(ticker)
    ticker_info = ticker_obj.info
    ## Historical Data
    hist_df = ticker_obj.history(period="1y")
    hist_df = hist_df.reset_index() 
    ## News Data
    news_data = [{"title": entry["title"], "link": entry["link"], "publisher": entry["publisher"]}\
                 for entry in ticker_obj.news]
    
    return hist_df, ticker_info, news_data

def display_ticker(request, ticker):
    hist_df, info, news_data = retrieve_data(ticker)
    hist_data = hist_df.to_json(orient="records")
    p1, p2 = hist_df["Close"].values[-1], hist_df["Close"].values[-2]
    change, prcnt_change = (p2-p1), (p2-p1)  / p1

    return render(request, "dashboard/main.html", {
                                                "ticker": zip(tickers, names),
                                                "names": names, 
                                                "ticker": ticker,
                                                "hist_data": hist_data,
                                                "news": news_data,
                                                "name": info["longName"],
                                                "industry": info["industry"],
                                                "sector": info["sector"],
                                                "summary": info["longBusinessSummary"],
                                                "close": f"{p1: .2f} USD",
                                                "change": f"{change: .2f}",
                                                "pct_change": f"{prcnt_change*100: .2f}%"
                                                })