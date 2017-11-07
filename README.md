# AliBot
Get ready for Flash Deals and buy products instantly. The tool waits until a product's price goes above a given price and navigates to the payment page. It is also able to auto-buy the product, altought it is not recommended to use.

## Getting Started

These instructions will show you how to configure the bot

### Prerequisites

Install the latest Selenium Webdriver for Python by using the following command:

```
pip install selenium
```
You also need a **Chromedriver** placed in the project directory, you can download it from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

### Setting

To use this tool you need to configure the following parameters in **config** file:
* **DEAL_LINK** : link to the Flash Deal
* **USER** : aliexpress user name
* **PWD** : aliexpress password
* **TARGET_PRICE** : price you want to buy the product under
* **REFRESH_INTERVAL** : page refresh interval
* **WAIT_TIMEOUT** : max wait time for an element to load
* **AUTO_BUY** : buy product automatically (YES/NO). Not recommended to keep it as **YES**. It will automatically fill out bank card details and buy the product.
* **CARD_NUMBER** : bank card number
* **EXPIRY_MONTH** : bank card expiry month
* **EXPIRY_YEAR** : bank card expiry year
* **CVC** : bank card cvc number
* **FIRST_NAME** = bank card first name
* **LAST_NAME** = bank card last name

## Start the tool

The script can start by 
```
python autobuy.py
```
