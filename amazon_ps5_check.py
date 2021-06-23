# This runs a Selenium script to refresh the Amazon PS5 (disk version) page and checks to see if it's available or not. If it's available, it adds it to the cart & sends an notification using AWS SNS.

import boto3
import time
import random
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Sets Selenium to use your profile in Chrome, rather than a brand new instance (so you can stay logged in on Amazon)
options = webdriver.ChromeOptions()
options.add_argument("<INSERT LOCATION HERE BELOW>")

# Usual default locations for Chrome options:
# MacOS: options.add_argument("user-data-dir=/Users/<USER NAME>/Library/Application Support/Google/Chrome/")
# Windows: options.add_argument('user-data-dir=C:/Users/<USERNAME>/AppData/Local/Google/Chrome/User Data')

# Passes the options through to Chrome & opens the Amazon link of your choice. Don't forget to download Chromedriver & install or include the location in webdriver
driver = webdriver.Chrome(chrome_options=options)
url = driver.get(
    'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG/')

def main():
    attempt = 0
    InStock = False
    while not InStock:
        try:
            if (driver.find_element_by_xpath("""/html/body/div[2]/div[2]/div[7]/div[6]/div[4]/div[18]/div[1]/span""").text == "Currently unavailable."):
                # Checks if the page shows it as currently unavailable
                attempt += 1
                print("Not available. Try number: ", attempt)
                # Waits a random amount of time between 5 and 20 seconds to refresh
                wait_time = random.randrange(5, 20)
                time.sleep(wait_time)
                driver.refresh()
            else:
                InStock = True
        except:
            # If available, gets the price, adds the PS5 to the cart, & passes the data through to SNS for notification
            price = driver.find_element_by_xpath("""//*[@id="priceblock_ourprice"]""").text
            driver.find_element_by_xpath("""//*[@id="add-to-cart-button"]""").click()
            cartLink = "https://www.amazon.com/gp/cart/view.html?ref_=nav_cart"
            publish(price, cartLink)

# Publishes a notification using AWS SNS with the pass-through from the previous function
def publish(price, cartLink):
    arn = #ARN reference code here
    sns_client = boto3.client(
        'sns',
        # Optional steps to define AWS info
		    # region_name= 'us-east-1' etc-
    		# If your AWS environment isn't set up in your IDE - you'll need to add the below. HOWEVER - it's insecure to store keys in code - much better to reference from environment variables! 
    		# access_key_id=<AWS Access Key>
    		# aws_secret_access_key=<AWS Secret Access Key>
    )

    response = sns_client.publish(TopicArn=arn,
                                  Message='PS5 is in stock! Added to cart! Price is ' + price + '! Check out now: ' + cartLink)


main()
