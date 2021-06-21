# InStockBot
This is a quick python script that uses the Best Buy API to check stock of specific SKUs and then uses AWS SNS to send a text with the Add to Cart link.

API calls are limited to once every 5 seconds.

Requires:
AWS Account (optional for SNS & to run on EC2)
Best Buy Developer Account (required for the API)
