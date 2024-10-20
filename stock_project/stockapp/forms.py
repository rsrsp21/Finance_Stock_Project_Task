from django import forms

class BacktestForm(forms.Form):
    initial_investment = forms.DecimalField(label='Initial Investment Amount', min_value=0.01)
    moving_average_short = forms.IntegerField(label='Short Moving Average (e.g., 50)', min_value=1)
    moving_average_long = forms.IntegerField(label='Long Moving Average (e.g., 200)', min_value=1)