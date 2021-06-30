from lxml import html
import requests
import json
import boto3
import time


URL = 'https://www.skroutz.gr/s/23600384/Sony-PlayStation-5.html'
headers = {
    'authority': 'www.skroutz.gr',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4159.2 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-GB,en;q=0.9'
}

# ΜSRP στην Ελλαδα ειναι "499,99 €" η "399,99 €"
want_price = "500,00 €"

# Comment out the version you don't want. Please don't use both!

version = "disk"
#version = "diskless"

# Lowest price or Skroutz price? TBD on this, need to finish
# price_type = lowest
# price_type = skroutz - /html/body/div[2]/main/section/div/div[2]/div[5]/div/form/div[2]/div[1]/button/span/strong

def main():
    attempt = 0

    req = requests.get(URL, headers=headers)
    htmlreq = req.content

    tree = html.fromstring(htmlreq)

    price = tree.xpath('//span[@class="price-details"]/em/node()')
    if (version == "disk"):
        get_price = price[0]
    elif (version == "diskless"):
        get_price = price[1]
    else: print("Διαλέξεις disk η diskless παρακαλώ.")

    while get_price > want_price:
        attempt += 1
        print("Τιμή: " + str(get_price) + " Προσπάθεια: " + str(attempt))
        time.sleep(1200)
    else:
        print("PS5! Ωραια τιμή! Τιμή: ", get_price, " Εδω: ", URL)
        publish(get_price, URL)


def publish(get_price, URL):
    arn = #ARN Number Here
    sns_client = boto3.client(
        'sns',
        region_name=#AWS Region Name Here
    )

    response = sns_client.publish(TopicArn=arn, Message='PS5! Ωραια τημη! Τημη: ' + get_price + ' Εδω: ' + URL)

main()
