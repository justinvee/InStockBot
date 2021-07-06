from lxml import html
import requests
import json
import boto3
import time
import discord
from discord import Webhook, RequestsWebhookAdapter

URL = 'https://www.skroutz.gr/s/23615477/Sony-PlayStation-5-Digital-Edition.html'
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

# Choose the price you want to be alerted when the item goes lower. MSRP in Greece is 499,99 or 399,99.
# ΜSRP στην Ελλαδα ειναι "499,99 €" για "disk" ή "399,99 €" για "diskless"
# Γράψεις το τιμή ο΄τι θελεις. Το φορματ ειναι: "ΧΧΧ,ΧΧ €"
want_price = "500,00 €"

# Comment out the version you don't want. Both won't work. Coming soon perhaps.
# Γράψεις '#' πριν απο το έκδοση δεν θελεις.
version = "disk"
#version = "diskless"

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
    else:
        print("Διαλέξεις disk η diskless παρακαλώ.")
        exit()

    while get_price > want_price:
        attempt += 1
        print("Τιμή: " + str(get_price) + " Προσπάθεια: " + str(attempt))
        # Choose how long you want to wait until it checks again. (In seconds.)
        # Επιλέξτε πόσο καιρό θα περιμένετε πριν ελέγξετε ξανά. (Σε δευτερόλεπτα.)
        time.sleep(1200)
    else:
        print("Επιτυχία!")
        aws_publish(get_price, URL)
        discord_pub(get_price, URL)
        # If you want it to keep running after success, keep the code below. If not, delete.
        # Αν θες να κλειστει όταν είναι επιτυχής, γράψεις '#' πριν "time.sleep" και "main()"
        time.sleep(1800)
        main()

def publish(get_price, URL):
    arn = #ARN Number Here
    sns_client = boto3.client(
        'sns',
        region_name=#AWS Region Name Here
    )

    response = sns_client.publish(TopicArn=arn, Message='PS5! Ωραια τημη! Τημη: ' + get_price + ' Εδω: ' + URL)

def discord_pub(get_price, URL):
    webhook = Webhook.from_url(
        "<DISCORD WEBHOOK URL HERE>",
        adapter=RequestsWebhookAdapter())
    webhook.send("@here PS5! Ωραια τημη! Τημη: " + str(get_price) + " Εδω: " + URL)
    
main()
