import matplotlib.pyplot as plt
from django.core.files import File
from io import BytesIO
from django.conf import settings
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from dateutil import parser

def parse_datetime(timestamp_str):
    return pd.to_datetime(timestamp_str, format='%b. %d, %Y, midnight')

def generate_performance_report(predicted_data, actual_data, symbol):
    plt.figure(figsize=(10, 6))

    # Convert index to datetime
    actual_data.index = actual_data.index.map(parse_datetime)
    predicted_data.index = predicted_data.index.map(parse_datetime)

    # Remove duplicates by keeping the last occurrence
    actual_data = actual_data[~actual_data.index.duplicated(keep='last')]
    predicted_data = predicted_data[~predicted_data.index.duplicated(keep='last')]

    # Plotting actual and predicted prices
    plt.plot(actual_data.index, actual_data['close_price'], label='Actual Prices', color='blue')
    plt.plot(predicted_data.index, predicted_data['predicted_price'], label='Predicted Prices', color='orange')
    
    plt.title(f'Stock Price Prediction for {symbol}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    
    # Save the plot to a file
    plot_path = os.path.join(settings.MEDIA_ROOT, f'reports/{symbol}_performance_report.png')
    plt.savefig(plot_path)
    plt.close()

    # Create PDF report
    pdf_path = os.path.join(settings.MEDIA_ROOT, f'reports/{symbol}_performance_report.pdf')
    pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []

    # Add the plot image
    img = Image(plot_path)
    img.drawHeight = 3 * inch  # Adjust height
    img.drawWidth = 5 * inch  # Adjust width
    elements.append(img)

    # Create a table for predicted prices
    data = [['Date', 'Predicted Price']]  # Header
    for date, row in predicted_data.iterrows():
        data.append([date.strftime('%Y-%m-%d'), row['predicted_price']])
    
    # Create a Table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Conclusions Section
    conclusions = f"""
    Conclusion:
    The predicted prices for {symbol} for the next 30 days are presented in the table above. 
    This report visualizes the actual vs. predicted prices to assess the model's performance.
    """
    
    # Use Paragraph for text
    styles = getSampleStyleSheet()
    conclusion_paragraph = Paragraph(conclusions, styles['Normal'])
    elements.append(conclusion_paragraph)

    # Build PDF
    pdf.build(elements)

    return pdf_path, plot_path
