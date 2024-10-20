import requests
from django.shortcuts import render
from .models import StockData
from datetime import datetime
import pandas as pd
from .forms import BacktestForm
from django.http import JsonResponse
from .predictions import predict_stock_prices
import pandas as pd
from .models import StockData
from .reports import generate_performance_report
from django.conf import settings

API_KEY = '4CX4W3MUHEUTPYSA'  #Alpha Vantage API key

def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    time_series = data.get('Time Series (Daily)', {})
    for date, daily_data in time_series.items():
        open_price = daily_data['1. open']
        high_price = daily_data['2. high']
        low_price = daily_data['3. low']
        close_price = daily_data['4. close']
        volume = daily_data['5. volume']
        timestamp = datetime.strptime(date, '%Y-%m-%d')

        # Save data to the database
        StockData.objects.create(
            symbol=symbol,
            open_price=open_price,
            high_price=high_price,
            low_price=low_price,
            close_price=close_price,
            volume=volume,
            timestamp=timestamp
        )
from django.http import HttpResponse

def fetch_and_store(request):
    fetch_stock_data('AAPL')  # Fetch data for Apple (AAPL)
    return HttpResponse("Stock data fetched and stored!")

def homepage(request):
    return render(request, 'homepage.html')

def stock_data_list(request):
    # Fetch all stock data from the database
    stock_data = StockData.objects.all()
    return render(request, 'stockapp/stock_data_list.html', {'stock_data': stock_data})

def backtest(request):
    result = None
    if request.method == 'POST':
        form = BacktestForm(request.POST)
        if form.is_valid():
            initial_investment = form.cleaned_data['initial_investment']
            short_ma = form.cleaned_data['moving_average_short']
            long_ma = form.cleaned_data['moving_average_long']

            # Fetch the stock data (you can modify the query as needed)
            stock_data = StockData.objects.all().order_by('timestamp')
            df = pd.DataFrame(list(stock_data.values()))

            # Ensure timestamp is in datetime format
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)

            # Calculate moving averages
            df['short_ma'] = df['close_price'].rolling(window=short_ma).mean()
            df['long_ma'] = df['close_price'].rolling(window=long_ma).mean()

            # Drop rows with NaN values in close_price, short_ma, or long_ma
            df.dropna(subset=['close_price', 'short_ma', 'long_ma'], inplace=True)

            # Initialize backtesting variables
            cash = initial_investment
            shares = 0
            trades = 0
            buy_price = 0
            buy_dates = []

            for index, row in df.iterrows():
                # Buy condition
                if row['close_price'] < row['short_ma'] and cash > 0:
                    shares = cash / row['close_price']
                    cash = 0
                    buy_price = row['close_price']
                    buy_dates.append(index)

                # Sell condition
                elif row['close_price'] > row['long_ma'] and shares > 0:
                    cash = shares * row['close_price']
                    shares = 0
                    trades += 1

            # Calculate returns and metrics
            total_value = cash + shares * row['close_price'] if shares > 0 else cash
            total_return = round(total_value - initial_investment, 2)
            max_drawdown = (buy_price - df['close_price'].min()) if buy_price else 0
            result = {
                'total_return': total_return,
                'max_drawdown': max_drawdown,
                'trades_executed': trades,
            }
    else:
        form = BacktestForm()

    return render(request, 'stockapp/backtest.html', {'form': form, 'result': result})

def predict_prices(request):
    symbol = request.GET.get('symbol', None)
    if not symbol:
        return JsonResponse({'error': 'Stock symbol is required'}, status=400)

    predictions = predict_stock_prices(symbol)
    predictions_dict = predictions.to_dict(orient='index')  # Convert DataFrame to dictionary

    # Render the predictions in HTML and pass the current symbol
    return render(request, 'stockapp/predict.html', {
        'predictions': predictions_dict,
        'current_symbol': symbol  # Pass the current symbol to the template
    })

def performance_report(request):
    symbol = request.GET.get('symbol', None)
    if not symbol:
        return JsonResponse({'error': 'Stock symbol is required'}, status=400)
    
    # Assume you have methods to get actual and predicted data
    actual_queryset = StockData.objects.filter(symbol=symbol).order_by('timestamp')
    actual_data = pd.DataFrame.from_records(actual_queryset.values())

    # Ensure that your DataFrame has 'timestamp' as the index
    actual_data['timestamp'] = pd.to_datetime(actual_data['timestamp'])
    actual_data.set_index('timestamp', inplace=True)

    predicted_data = predict_stock_prices(symbol)
    
    # Ensure predicted_data is also a DataFrame with 'timestamp' as the index
    if isinstance(predicted_data, dict):
        predicted_data = pd.DataFrame.from_dict(predicted_data, orient='index')
        predicted_data.columns = ['predicted_price']
        predicted_data.index = pd.to_datetime(predicted_data.index)

    # Generate report
    pdf_path, plot_path = generate_performance_report(predicted_data, actual_data, symbol)
    
    # Build absolute URLs for the generated reports
    report_url = request.build_absolute_uri(settings.MEDIA_URL + f'reports/{symbol}_performance_report.pdf')
    plot_url = request.build_absolute_uri(settings.MEDIA_URL + f'reports/{symbol}_performance_report.png')

    return JsonResponse({'report_link': report_url, 'plot_link': plot_url})