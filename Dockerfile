FROM python:latest

WORKDIR /app/GetStockData

COPY script.py /app/GetStockData

RUN pip install requests pandas yfinance

CMD python script.py