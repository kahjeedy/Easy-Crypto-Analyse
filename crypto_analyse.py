import json
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import time
import os
import argparse


price_cache = {}

# Function to get the current price
def get_price(coin_id, currency):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": currency
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if coin_id in data:
            return data[coin_id][currency]
        else:
            print("API Response:", data)
            raise ValueError(f"Unexpected response format: '{coin_id}' key not found")
    else:
        raise ConnectionError(f"Failed to fetch data: {response.status_code}")

# Function to get the historical price
def get_historical_price(coin_id, timestamp, currency, retries=5):
    date = datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y')
    

    if date in price_cache:
        return price_cache[date]
    
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/history"
    params = {
        "date": date
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if "market_data" in data and "current_price" in data["market_data"]:
                    price = data["market_data"]["current_price"][currency]
                    price_cache[date] = price  # Cache the price for this date
                    return price
                else:
                    print("API Response:", data)
                    raise ValueError(f"Unexpected response format: 'market_data' key not found")
            elif response.status_code == 429:
                print(f"Rate limit hit. Waiting 60 seconds... (Attempt {attempt + 1} of {retries})")
                time.sleep(60)  # Wait for 60 seconds before retrying
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            time.sleep(60) 
    
    raise ConnectionError("Exceeded maximum retry attempts due to rate limiting.")

# Create folders for saving data and images
def create_output_folders(coin_type):
    data_folder = f"{coin_type}_data"
    
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    return data_folder


def process_file(file_path, currency):
    global price_cache 
    
    # Load the JSON file
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' does not contain valid JSON.")
        return

    # Determine the coin type (eth or btc)
    coin_type = data.get('coin', 'eth').lower()
    coin_id = 'ethereum' if coin_type == 'eth' else 'bitcoin'

    # Create output folders for the specific coin type
    data_folder = create_output_folders(coin_type)

    #process variables
    total_received = 0.0
    total_sent = 0.0
    total_cost_currency = 0.0
    total_fees = 0.0
    transaction_count = 0
    transaction_summary = {}
    transaction_details = []

    #graph variables
    timestamps = []
    wallet_values = []
    profits = []

    #Request count to avoid api limiting
    request_count = 0


    price_in_currency = get_price(coin_id, currency)  # Ensure this is defined at the start of processing

    # Iterate through the transactions
    for tx in data['transactions']:
        timestamp = tx['blockTime']
        datetime_of_transaction = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        #Rate limit
        request_count += 1
        if request_count > 5:
            print("Reached 5 requests, waiting for 60 seconds to avoid rate limiting...")
            time.sleep(60)  # Wait for 60 seconds before continuing
            request_count = 1  # Reset request count after waiting
        
        historical_price_currency = get_historical_price(coin_id, timestamp, currency)

        print(f"\nTransaction ID: {tx['txid']}")
        print(f"Time of Transaction: {datetime_of_transaction}")
        print(f"{coin_type.upper()} Price at the time: ${historical_price_currency} {currency.upper()}")

        amount = float(tx['amount']) if coin_type == 'btc' else sum(float(transfer['amount']) for transfer in tx.get('internalTransfers', []))
        
        if tx['type'] == 'recv':  # Received
            total_received += amount
            cost_currency = amount * historical_price_currency
            total_cost_currency += cost_currency
            print(f"Received: {amount} {coin_type.upper()} at a cost of ${cost_currency} {currency.upper()}")
        elif tx['type'] == 'sent':  # Sent
            total_sent += amount
            print(f"Sent: {amount} {coin_type.upper()}")

        fee = float(tx['fee'])
        total_fees += fee
        print(f"Transaction Fee: {fee} {coin_type.upper()}")

        # Track wallet value and profit over time
        current_balance = total_received - total_sent
        wallet_value = current_balance * historical_price_currency
        profit = (current_balance * price_in_currency) - total_cost_currency
        
        # Append to lists for plotting
        timestamps.append(datetime_of_transaction)
        wallet_values.append(wallet_value)
        profits.append(profit)

        # Log each transaction
        transaction_details.append({
            "Transaction ID": tx['txid'],
            "Time": datetime_of_transaction,
            "Amount": amount,
            "Wallet Value": wallet_value,
            "Profit": profit,
            "Fee": fee
        })

        # Count transactions by type
        tx_type = tx['type']
        if tx_type in transaction_summary:
            transaction_summary[tx_type] += 1
        else:
            transaction_summary[tx_type] = 1
        
        transaction_count += 1

    # Calculate current balance and fees
    current_balance = total_received - total_sent
    current_value_currency = current_balance * price_in_currency
    total_fees_currency = total_fees * price_in_currency

    #summary data
    summary_data = {
        f"Total {coin_type.upper()} Received": total_received,
        f"Total {coin_type.upper()} Sent": total_sent,
        f"Current Balance ({coin_type.upper()})": current_balance,
        f"Total Cost ({currency.upper()})": total_cost_currency,
        f"Current Value ({currency.upper()})": current_value_currency,
        f"Total Profit ({currency.upper()})": profits[-1],  # Final profit
        f"Total Fees Paid ({coin_type.upper()})": total_fees,
        f"Total Fees Paid ({currency.upper()})": total_fees_currency,
        "Total Transactions": transaction_count,
        "Transaction Summary by Type": transaction_summary,
        "Transactions": transaction_details  # Include all transactions
    }

    print("\n--- SUMMARY ---")
    print(json.dumps(summary_data, indent=4))

    # Save the summary to a JSON file
    output_file_path = os.path.join(data_folder, f'{coin_type}_summary_output.json')
    with open(output_file_path, 'w') as outfile:
        json.dump(summary_data, outfile, indent=4)

    print(f"\nSummary has been saved to {output_file_path}")

    # Convert timestamps to numeric for smooth plotting
    x_numeric = np.arange(len(timestamps))

    # Smooth curve plotting using interpolation
    x_smooth = np.linspace(x_numeric.min(), x_numeric.max(), 500)

    # wallet, profit graph
    plt.figure(figsize=(12, 8))

    # Plot Wallet Value (curved and straight lines)
    wallet_values_smooth = make_interp_spline(x_numeric, wallet_values)(x_smooth)
    plt.plot(x_smooth, wallet_values_smooth, color='red', label=f'Wallet Value ({currency.upper()})', linestyle='-')
    plt.plot(x_numeric, wallet_values, color='red', linestyle='-', marker='o')  # Exact line

    # Plot Profit (curved and straight lines)
    profit_smooth = make_interp_spline(x_numeric, profits)(x_smooth)
    plt.plot(x_smooth, profit_smooth, color='green', label=f'Profit ({currency.upper()})', linestyle='-')
    plt.plot(x_numeric, profits, color='green', linestyle='-', marker='o')  # Exact line

    # Annotate all points
    for i, txt in enumerate(wallet_values):
        plt.annotate(f'{txt:.2f}', (x_numeric[i], wallet_values[i]), textcoords="offset points", xytext=(0,5), ha='center')
    for i, txt in enumerate(profits):
        plt.annotate(f'{txt:.2f}', (x_numeric[i], profits[i]), textcoords="offset points", xytext=(0,5), ha='center')

    plt.xlabel('Time')
    plt.ylabel(f'{currency.upper()}')
    plt.title(f'All-in-One: Wallet Value and Profit Over Time ({currency.upper()})')
    plt.legend()
    plt.grid(True)
    plt.xticks(ticks=x_numeric, labels=timestamps, rotation=45)
    plt.tight_layout()

    # Save plot
    all_in_one_plot_path = os.path.join(data_folder, f'{coin_type}_all_in_one_plot.png')
    plt.savefig(all_in_one_plot_path)
    print(f"All-in-One plot has been saved to {all_in_one_plot_path}")

    # Show All-in-One plot
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Process cryptocurrency transaction data and generate plots.")
    parser.add_argument("-f", "--file", required=True, help="Path to the JSON file containing transaction data.")
    parser.add_argument("-c", "--currency", choices=["aud", "usd"], required=True, help="Currency to calculate values in (AUD or USD).")
    
    args = parser.parse_args()
    
    process_file(args.file, args.currency)

if __name__ == "__main__":
    main()
