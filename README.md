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

### Install Dependencies

```sh
pip install -r requirements.txt
