import boto3
import time
import random
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import discord
from discord import Webhook, RequestsWebhookAdapter

# Sets Selenium to use your profile in Chrome, rather than a brand new instance (so you can stay logged in on Amazon)
options = webdriver.ChromeOptions()
options.add_argument("# USER DATA LOCATION HERE")

# Usual default locations for Chrome options:
# MacOS: options.add_argument("user-data-dir=/Users/<USER NAME>/Library/Application Support/Google/Chrome/")
# Windows: options.add_argument('user-data-dir=C:/Users/<USERNAME>/AppData/Local/Google/Chrome/User Data')

# Passes the options through to Chrome & opens the Amazon link of your choice.
driver = webdriver.Chrome(chrome_options=options)
url = driver.get(
    'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG/')

def main():
    attempt = 0
    InStock = False
    while not InStock:
        if (driver.find_element_by_xpath("""//*[@id="availability"]/span""").text == "Currently unavailable."):
            # Checks if the page shows it as currently unavailable
            attempt += 1
            print("Not available. Try number: ", attempt)
            # Waits a random amount of time between 5 and 20 seconds to refresh
            time.sleep(random.randrange(5, 20))
            driver.refresh()
        elif bool(driver.find_element_by_xpath("""//*[@id="buybox-see-all-buying-choices"]/span/a""")) == True:
            # This section is checking if it's available through the "See All Buying Options" box & displays the price, but it doesn't notify.
            driver.find_element_by_xpath("""//*[@id="buybox-see-all-buying-choices"]/span/a""").click()
            time.sleep(5)
            type = driver.find_element_by_xpath("""//*[@id="aod-offer-heading"]/h5""").text
            seller = driver.find_element_by_xpath("""//*[@id="aod-offer-shipsFrom"]/div/div/div[2]/span""").text
            price = driver.find_element_by_xpath("""//*[@id="aod-price-1"]/span/span[2]/span[2]""").text
            addToCart = str("https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG/")
            driver.refresh()
            print("Found, but not Amazon. Lowest price is: $" + price + ". Trying again.")
            time.sleep(random.randrange(5, 20))
        else:
            InStock = True
            continue
    else:
        # This section alerts through notifications when an "Our Price" appears on the Amazon PS5 page. This is a proxy for a real sale from Amazon at MSRP.
        price = driver.find_element_by_xpath("""//*[@id="priceblock_ourprice"]""").text
        driver.find_element_by_xpath("""//*[@id="add-to-cart-button"]""").click()
        ASIN = driver.find_element_by_xpath(
            """/html/body/div[1]/div[2]/div[7]/div[23]/div/div/div/div[1]/div/div/table/tbody/tr[1]/td""")
        addToCart = ("https://www.amazon.com/gp/cart/view.html?ref_=nav_cart")
        seller = "Amazon"
        type = "New"
        publish(price, addToCart)
        discord_pub(seller, type, price, addToCart)
        print("Waiting 30min to check again.")
        time.sleep(1800)
        driver.refresh()
        main()


# Publishes a notification using AWS SNS with the pass-through from the previous function
def publish(price, addToCart):
    arn = # Your Key Here
    sns_client = boto3.client(
        'sns',
        region_name=# Your Region Here
    )

    response = sns_client.publish(TopicArn=arn,
                                  Message='PS5 is in stock! Added to cart! Price is ' + price + '! Check out now: ' + addToCart)

def discord_pub(seller, type, price, addToCart):
    webhook = Webhook.from_url("<< Discord Webhook URL Here >>", adapter=RequestsWebhookAdapter())
    webhook.send("@here PS5 available! Seller is: " + seller + ", the type is: " + type +" and the price is: " + str(price) + " and URL is: " + addToCart)

main()
