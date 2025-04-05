import pandas as pd
import matplotlib.pyplot as plt
def load_stock_data():
    data = {
        'Date': ['2024-01-01', '2024-01-01', '2024-01-01', '2024-01-02'],
        'Company': ['Apple', 'Microsoft', 'Amazon', 'Apple'],
        'Stock_Price': [150, 280, 3200, 155]
    }
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date']) 
    return df
def compute_daily_changes(df):
    df['Prev_Price'] = df.groupby('Company')['Stock_Price'].shift(1)
    df['Price_Change'] = df['Stock_Price'] - df['Prev_Price']
    return df
def plot_stock_trends(df):
    plt.figure(figsize=(10, 5))
    for company in df['Company'].unique():
        company_data = df[df['Company'] == company]
        plt.plot(company_data['Date'], company_data['Stock_Price'], marker='o', label=company)
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.title("Stock Market Trends")
    plt.legend()
    plt.grid(True)
    plt.show()
df = load_stock_data()
df = compute_daily_changes(df)
print("\nStock Data with Daily Changes:\n", df)
plot_stock_trends(df)
