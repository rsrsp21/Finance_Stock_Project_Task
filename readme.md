# Stock Price Prediction and Performance Report

This project is a stock price prediction system that allows users to view predicted stock prices for a given symbol and generate performance reports, including a downloadable PDF and a plot of the actual vs. predicted prices.

## Features

- **Stock Price Prediction**: Predict future stock prices for a given symbol.
- **Performance Report**: Generate a PDF report with a comparison between actual and predicted stock prices along with a plot image.
- **Interactive UI**: Users can view predicted stock prices and generate reports directly from the web interface.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Generating Reports](#generating-reports)
- [Contributing](#contributing)

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Plotting**: Matplotlib
- **PDF Generation**: ReportLab
- **Prediction Algorithm**: Linear Regression (integrated in Backend)

## Project Structure

```plaintext
stock_project/
│
├── stockapp/
│   ├── migrations/
│   ├── static/
│   │   └── stockapp/
│   │       └── css/
│   │           └── styles.css         # Custom styles for the frontend
│   ├── templates/
│   │   └── stockapp/
│   │       ├── base.html              # Base template
│   │       ├── predict.html           # Page for predictions and report generation
│   ├── models.py                      # Django models for stock data
│   ├── views.py                       # Main view functions
│   ├── urls.py                        # URL routing
│   ├── utils.py                       # Utility functions (data parsing, report generation, etc.)
│   └── ...
│
├── media/
│   └── reports/                       # Generated reports (PDF and images)
│
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```
## Installation

Follow these steps to get the project up and running on your local machine:

### Prerequisites

- **Python 3.10 or later**: Ensure Python is installed on your system.
- **Virtual Environment**: It's recommended to use a virtual environment for isolating dependencies.

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/rsrsp21/Finance_Stock_Project_Task_Blockhouse.git
    cd stock_project
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv env
    ```

3. **Activate the virtual environment**:
    - On Windows:
      ```bash
      .\env\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source env/bin/activate
      ```

4. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run database migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Start the development server**:
    ```bash
    python manage.py runserver
    ```

7. **Access the application**: Open your browser and go to `http://127.0.0.1:8000/stockapp` to view the stock prediction page.

## Usage

### Predict Stock Prices:
- Enter a valid stock symbol (e.g., "AAPL") in the input field.
- The page will display the predicted prices in a table.

### Generate Performance Report:
- Click the "Generate Report" button to generate a PDF report that includes a plot comparing actual and predicted stock prices.

### Download Report:
- Once the report is generated, links to download the PDF and image plot will appear.

## Generating Reports

The project generates reports using Matplotlib for plots and ReportLab for PDF generation. Reports include a visual representation of the stock's predicted vs. actual performance.

### Steps to generate a report:
1. Enter the stock symbol (e.g., AAPL).
2. Click "Generate Report".
3. The system generates a downloadable PDF and plot file, displaying the links on the page.

## Contributing

Contributions are welcome! Here's how you can help:
1. Fork the project.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m 'Added a new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a Pull Request.

