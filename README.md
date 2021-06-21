# InStockBot
This is a quick python script that uses the Best Buy API to check stock of specific SKUs and then uses AWS SNS to send a text with the Add to Cart link.

API calls are limited to once every 5 seconds per the Developer agreement.

Requires:

- AWS Account (optional for SNS & to run on EC2)

- Best Buy Developer Account (required for the API)
-   Best Buy limits access to their API, so you either have to have a company account to grab a key, or you can sign up using a non-free email and get a temporary key until they approve or deny your request
