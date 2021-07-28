from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import io
import base64
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_prices(ticker):
    end = pd.Timestamp.now()
    start = end - pd.Timedelta(31, 'D')
    
    period1 = (start - pd.Timestamp("1970-01-1"))\
                    // pd.Timedelta('1s')
    period2 = (end - pd.Timestamp("1970-01-1"))\
                    // pd.Timedelta('1s')
    
    url = 'https://finance.yahoo.com/'\
            + f'quote/{ticker}/history?'\
            + f'period1={period1}&period2={period2}'\
            + '&interval=1d&filter=history&frequency=1d'
    response = requests.get(url)
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.text)
    prices = []
    for row in soup.find_all('table',
            attrs={'data-test': 
                   'historical-prices'})[0]\
                .find_all('tr')[1:-1]:
        try:
            prices.append(float(row.find_all('td')[1].text))
        except:
            pass
    prices = prices[::-1]
    prices = np.array(prices)
    prices = ((prices / prices[0]) - 1) * 100
    return prices


@app.get("/")
async def root(request: Request, message='Hello, Coursera students'):
    # return {"message": "Hello World"}
    return templates.TemplateResponse("index.html",
                        {"request": request,
                        "message": message})

@app.post("/show_plot")
async def show_plot(request: Request,
                    ticker_1: str = Form(...),
                    ticker_2: str = Form(...)):
    prices1 = get_prices(ticker_1)
    prices2 = get_prices(ticker_2)

    fig = plt.figure()
    plt.plot(prices1)
    plt.plot(prices2)
    plt.ylabel('proft, %')
    plt.xlabel('day number')
    plt.legend([ticker_1, ticker_2])

    pngImage = io.BytesIO()
    fig.savefig(pngImage)
    pngImageB64String\
        = base64.b64encode(pngImage.getvalue()).decode('ascii')

    score_1, score_2 = prices1[-1], prices2[-1]
    return templates.TemplateResponse("plot.html",
                                {"request": request,
                                "picture": pngImageB64String,
                                "ticker_1": ticker_1,
                                "ticker_2": ticker_2,
                                "score_1": score_1,
                                "score_2": score_2})
