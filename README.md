# Cryptocurrency Transaction Analyzer

## Overview

The Cryptocurrency Transaction Analyzer is a Python script that processes transaction data from JSON files, calculates wallet value and profit over time, and generates detailed graphs. The script is designed to work with Ethereum (ETH) and Bitcoin (BTC) transactions and outputs clear, annotated visualizations of your portfolio's performance.

## Features

- **Historical and Current Price Analysis**: Fetches historical prices of cryptocurrencies at the time of each transaction and compares them to current prices.
- **Profit Calculation**: Accurately calculates profit for each transaction based on historical and current prices.
- **Graphical Representation**: Generates an "all-in-one" graph that includes both wallet value and profit, with exact lines and smooth curves.
- **Comprehensive JSON Output**: Outputs a detailed JSON file summarizing all transactions, including profit, fees, and wallet value for each timestamp.

## How It Works

1. **Transaction Processing**:
    - The script reads a JSON file containing transaction data.
    - It identifies the cryptocurrency (ETH or BTC) and processes each transaction, calculating the total received and sent amounts.

2. **Profit Calculation**:
    - For each transaction, the script fetches the historical price of the cryptocurrency at the time of the transaction.
    - It calculates the profit by comparing the cost of the cryptocurrency at the time it was received to its current value.

3. **Graph Generation**:
    - The script generates a single "all-in-one" graph that plots both wallet value and profit over time.
    - The graph includes both a smooth curve and exact connecting lines for precise analysis.

4. **Output**:
    - The script saves a detailed JSON file that includes a summary of all transactions and their impact on your portfolio.
    - The graph is saved as a PNG image in a directory named after the cryptocurrency (e.g., `eth_data` for Ethereum).

## Installation

To use the Cryptocurrency Transaction Analyzer, you'll need to have Python installed along with the required dependencies.

### Install Dependencies

```sh
pip install -r requirements.txt
