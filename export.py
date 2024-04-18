import yfinance as yf
import os

def get_stock_price(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    stock_data = stock.history(start=start_date, end=end_date)
    return stock_data

def export_to_excel(data_frame, file_name, folder_path=".", index=True):
    """
    Export a DataFrame to an Excel file.

    Parameters:
    - data_frame: pandas DataFrame, the data to be exported.
    - file_name: str, the name of the Excel file.
    - folder_path: str, optional, the path of the folder where the file will be saved.
                   Defaults to the current working directory.

    Returns:
    - excel_file_path: str, the full path of the exported Excel file.
    """
    # Create the full file path
    excel_file_path = os.path.join(folder_path, f"{file_name}.xlsx")

    # Export data to Excel
    data_frame.to_excel(excel_file_path, index=index)

    return excel_file_path

def main():
    # Define parameters
    ticker_symbols = ["AAPL", "MSFT", "GOOGL"]  # Add more ticker symbols as needed
    start_date = "2023-01-01"
    end_date = "2024-01-01"

    data_folder = os.path.join(os.getcwd(), "data")

    for ticker_symbol in ticker_symbols:
        # Fetch stock prices
        stock_prices = get_stock_price(ticker_symbol, start_date, end_date)

        # Convert datetime index to timezone-unaware datetime
        stock_prices.index = stock_prices.index.tz_localize(None)

        # Export data to Excel using the export_to_excel function
        excel_file_path = export_to_excel(stock_prices, f"{ticker_symbol}_stock_prices", folder_path=data_folder)
        print(f"Stock prices for {ticker_symbol} exported to '{excel_file_path}'")

if __name__ == "__main__":
    main()