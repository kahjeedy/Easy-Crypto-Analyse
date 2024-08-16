# Cryptocurrency Transaction Analyzer

## Overview

The Cryptocurrency Transaction Analyzer is a Python script that processes crypto transactions from a json file (Generated via Trezor Suite). Calculates the profit and value over time, exporting into an easy to read graph and json file.

## Features

- **Historical and Current Price Comparsion**: Fetches historical prices of the cryptocurrencies at the time of each transaction and compares them to current prices.
- **Profit Calculation**: Calculates profit for each transaction based on historical and current prices. This assumes the cryptocurrency was bought at the time of recieving the crypto
- **Graphical Representation**: Generates a graph that displays profit and wallet value over time
- **Comprehensive JSON Output**: Outputs a JSON file summarising all transactions.

## How It Works

1. **Transaction Processing**:
    - The script reads a JSON file containing transaction data. The json file is in the format that Trezor Suit generates. On Trezor Suit select transactions > export to json

2. **Profit Calculation**:
    - For each transaction, the script fetches the historical price of the cryptocurrency at the time of the transaction.
    - It calculates the profit by comparing the cost of the cryptocurrency at the time it was received to its current value.
    - This assumes that when you recieved crypto in your wallet is when the crypto was bought.

3. **Graph Generation**:
    - The script generates a graph that plots both wallet value and profit over time.

4. **Output**:
    - The script saves a JSON file that includes a summary of all transactions.
    - The graph is saved as a PNG image in a directory named after the cryptocurrency

## Installation

To use the Cryptocurrency Transaction Analyzer install python and the requirements

## Usage
python crypto_analysis.py -f path/file.json -c currency

Example:
python crypto_analysis.py -f Ethereum_1_20241608.json -c aud
python crypto_analysis.py -f Bitcoin_1_20241508.json -c usd



### Install Dependencies

```sh
pip install -r requirements.txt
```

** Exporting JSON Data from Trezor Suite**:
![image](https://github.com/user-attachments/assets/5883b0d0-c9c9-4e12-86e4-b3a463c774a9)

**Example Output**:
**Graph**:
![Figure_1](https://github.com/user-attachments/assets/27fec376-1940-49e0-b512-de19d725c698)

**JSON**:
```json
{
    "Total ETH Received": 1.5,
    "Total ETH Sent": 0.0,
    "Current Balance (ETH)": 1.5,
    "Total Cost (USD)": 2415.0,
    "Current Value (USD)": 5250.0,
    "Total Profit (USD)": 2835.0,
    "Total Fees Paid (ETH)": 0.005,
    "Total Fees Paid (USD)": 17.5,
    "Total Transactions": 5,
    "Transaction Summary by Type": {
        "recv": 5,
        "sent": 0
    },
    "Transactions": [
        {
            "Transaction ID": "0x1",
            "Time": "2021-01-01 00:00:00",
            "Amount": 0.5,
            "Wallet Value": 365.0,
            "Profit": 1385.0,
            "Fee": 0.001
        },
        {
            "Transaction ID": "0x2",
            "Time": "2021-02-01 00:00:00",
            "Amount": 0.3,
            "Wallet Value": 1120.0,
            "Profit": 2015.0,
            "Fee": 0.001
        },
        {
            "Transaction ID": "0x3",
            "Time": "2021-03-01 00:00:00",
            "Amount": 0.2,
            "Wallet Value": 1600.0,
            "Profit": 2395.0,
            "Fee": 0.001
        },
        {
            "Transaction ID": "0x4",
            "Time": "2021-04-01 00:00:00",
            "Amount": 0.1,
            "Wallet Value": 2090.0,
            "Profit": 2555.0000000000005,
            "Fee": 0.001
        },
        {
            "Transaction ID": "0x5",
            "Time": "2021-05-01 00:00:00",
            "Amount": 0.4,
            "Wallet Value": 4200.0,
            "Profit": 2835.0,
            "Fee": 0.001
        }
    ]
}
```




