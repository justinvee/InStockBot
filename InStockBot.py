import requests
import json
import boto3
import time

# Requires the Best Buy API key from the developer portal
URL = 'https://api.bestbuy.com/v1/products(sku in (<INSERT SKUS HERE>))?apiKey=<INSERT API KEY HERE>&sort=manufacturer.asc&show=manufacturer,name,onlineAvailability,regularPrice,addToCartUrl&format=json'
# Update the API key slot per your Developer account
# SKUs for Nvidia FEs: sku in (6429440, 6439402, 6429442, 6465789)


def main():
	attempt = 0

	# Gets the data from the API call and outputs it formatted as JSON
	req = requests.get(URL)
	req.json()

	req.encoding = 'json'
	output = req.text
	reloaded = json.loads(output)

	# This next section is to narrow down the output from Best Buy to be able to parse out specifically the URL and make it clickable.
	products = reloaded.get('products')
	new_prod = products[0]
	item_name = new_prod.get('name')
	item_price = new_prod.get('regularPrice')
	available = new_prod.get('onlineAvailability')
	addURL = new_prod.get('addToCartUrl')

	# Checks if the item is available, if it isn't - increments the attempts and then waits 5 seconds to try again. BB API is rate-limited.

	while (available != True):
		attempt += 1
    # Optional but helps to show it's working
		print(attempt)
    # Changes the time before checking again
		time.sleep(5)

	else:
		items = str(item_name + addURL)
		publish(item_name, addURL)

# This function publishes a successful find from the API to AWS SNS to text out
def publish(item_name, addURL):
	arn = #ARN Code from AWS here
	sns_client = boto3.client(
		'sns',
    # Optional steps to define AWS info
		#region_name= 'eu-central-1' etc-
    # If your AWS environment isn't set up in your IDE - you'll need to add:
    #access_key_id=<AWS Access Key>
    #aws_secret_access_key=<AWS Secret Access Key>
	)

	response = sns_client.publish(TopicArn=arn, Message=item_name + ' is in stock! Buy here ' + addURL)

main()
