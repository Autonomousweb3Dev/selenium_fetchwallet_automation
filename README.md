# Automate Fetch wallet using selenium

This project automates various tasks in the Fetch Wallet using Python and Selenium. It can import an existing account, open the wallet, change the network, send tokens, stake tokens, claim tokens, and create a new account.

## Prerequisites

* Python3
* [ChromeDriver](https://chromedriver.chromium.org/downloads)
* Fetch Wallet CRX file

## Setup &  Run project on local

1. Create and activate virtual environment
2. Install required dependencies:

   ```python
   pip install -r requirements.txt
   ```

3. Create a `.env` file and Copy the keys from the `example.env` file and update their values according to your configuration:
4. Run the project:

   ```python
   python wallet.py
   ```

The script will now perform the automation tasks on the Fetch Wallet.
