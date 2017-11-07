from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def read_config(filepath='config'):
    with open(filepath) as f:
        values = list(map(lambda x: x.split(' = '), f.readlines()))
    return dict(values)


def close_cupon(driver):
    try:
        element = WebDriverWait(driver, int(config['WAIT_TIMEOUT'])).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'close-layer')))
        element.click()
    except TimeoutException:
        print('Coupon did not show up...')


def signin(driver, user, pwd):
    element = WebDriverWait(driver, int(config['WAIT_TIMEOUT'])).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'nav-user-account')))
    element.click()

    WebDriverWait(driver, int(config['WAIT_TIMEOUT'])).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'iframe')))
    iframe = driver.find_element_by_css_selector('iframe')
    driver.switch_to_frame(iframe)
    user_textbox = driver.find_element_by_id('fm-login-id')
    password_textbox = driver.find_element_by_id('fm-login-password')
    user_textbox.send_keys(user)
    password_textbox.send_keys(pwd)

    driver.find_element_by_id('login-submit').click()


def buy_stuff(driver, target_price, config):
    print('buying stuff...')
    driver.find_element_by_class_name('buy-now-btn').click()
    if config['AUTO_BUY'] == 'YES':
        card_number_textbox = WebDriverWait(driver, int(config['WAIT_TIMEOUT'])).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'card-no')))
        expiry_month_textbox = WebDriverWait(driver, int(config['WAIT_TIMEOUT'])).until(
            EC.presence_of_element_located((By.ID, 'expiry-month')))
        expiry_year_textbox = WebDriverWait(driver, int(config['WAIT_TIMEOUT'])).until(
            EC.presence_of_element_located((By.ID, 'expiry-year')))
        cvc_textbox = WebDriverWait(driver, int(config['WAIT_TIMEOUT'])).until(
            EC.presence_of_element_located((By.NAME, 'cvc')))
        first_name_textbox = WebDriverWait(driver, int(config['WAIT_TIMEOUT'])).until(
            EC.presence_of_element_located((By.NAME, 'billingFirstName')))
        last_name_textbox = WebDriverWait(driver, int(config['WAIT_TIMEOUT'])).until(
            EC.presence_of_element_located((By.NAME, 'billingLastName')))
        price = driver.find_element_by_class_name('p-val')
        if float(price.text.split('$')[1]) == target_price:
            card_number_textbox.send_keys(config['CARD_NUMBER'])
            expiry_month_textbox.send_keys(config['EXPIRY_MONTH'])
            expiry_year_textbox.send_keys(config['EXPIRY_YEAR'])
            cvc_textbox.send_keys(config['cvc'])
            first_name_textbox.send_keys(config['FIRST_NAME'])
            last_name_textbox.send_keys(config['LAST_NAME'])
            #uncheck new card
            driver.find_element_by_id('saveToAe').click()
            driver.find_element_by_id('place-order-btn').click()
        else:
            print('Price changed')
    else:
        print('Buy it yourself')

config = read_config()

driver = webdriver.Chrome('./chromedriver')

driver.get(config['DEAL_LINK'])

close_cupon(driver)
time.sleep(int(config['REFRESH_INTERVAL']))
signin(driver, config['USER'], config['PWD'])

time.sleep(int(config['REFRESH_INTERVAL']))

price_not_changed = True
while price_not_changed:
    price = float(driver.find_element_by_xpath(".//*[@id='j-sku-discount-price']").text)
    if price < float(config['TARGET_PRICE']):
        price_not_changed = False
        buy_stuff(driver, price, config)
    else:
        print('Price: %f' % price)
        time.sleep(int(config['REFRESH_INTERVAL']))
        driver.refresh()