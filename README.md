# InStockBot Alerts
This is a collection of different Python scripts to check for stock of certain items (namely PlayStation 5, Nvidia GPUs, etc-) on Amazon, Best Buy, and other websites. These were written as a side-project as I was tired of trying to compete with scalpers/bots to get cards - why not fight fire with a bit of fire.

Use them at your own risk! They may also break - I'm not a developer, so this won't be the prettiest or most efficient code - but it's my shot at trying.

## [Best Buy API InStockBot](https://github.com/justinvee/InStockBot/blob/main/BestBuy_API_InStockBot.py)

This is a quick python script that uses the Best Buy API to check stock of specific SKUs and then uses AWS SNS to send a text with the Add to Cart link. Best Buy requires a developer account to access their API - they will not allow free email (gmail etc-) to sign up & they will usually revoke your temporary access after 24-72 hours - you can re-request a temporary key after this - but be warned it won't always work & requires some management. Plus - it's not right to take advantage of that!

Note: API calls are limited to once every 5 seconds per the Developer agreement.

Requires:
- Best Buy Developer Account (required for the API)
  -   Best Buy limits access to their API, so you either have to have a company account to grab a key, or you can sign up using a non-free email and get a temporary key until they approve or deny your request

- AWS Account (optional for SNS & to run on EC2)

## [Amazon PS5 Check](https://github.com/justinvee/InStockBot/blob/main/amazon_ps5_check.py) 

This is a Selenium script that checks the Amazon page for a PS5 (disk version, but you can update to diskless if you'd like) every 5-20 seconds. When it sees that the page shows it as no longer unavailable - it gets the price, adds it to cart, and sends a notification through SNS to check out with a checkout link.

Requires:
- Google Chrome (or Firefox - need to alter the code) and an ability to run Chrome refreshes on your machine (which can use a lot of RAM! so ideally use a separate computer)
  -   I haven't worked on getting this into EC2 yet - there is a way, but it's more complicated that it's probably worth - given you want cookies/user profiles to remain logged in

- AWS Account (optional for SNS)


## [Skroutz PS5 Price Monitoring](https://github.com/justinvee/InStockBot/blob/main/skroutz_ps5.py)

Similar to the Amazon PS5 check above, this checks the price for a PS5 on Skroutz (Greek retail/marketplace) and alerts if the price goes below a set price through AWS SNS. Need more work on this one & to add Discord notifications.
Requires:
- AWS Account (optional for SNS)


## Other

More to come... planning on having a similar check for Best Buy using Selenium (due to API key difficulties) and maybe some other sites. Plus maybe seeing if there is a way to set up notifications that doesn't require SMS & uses push instead.

Ps. I'm not a developer, so this may not be (ok, *is definitely not*) the most efficient way of doing this

Pps. I had a lot of help from posts and YouTube videos to make all these, so shout out to those great folks:

[Be A Better Dev - Scraping Bestbuy's Website with Python and AWS](https://www.youtube.com/watch?v=6ixBJZ2vnYk)

[Praneeth Kandula - Running Python scripts on an AWS EC2 Instance](https://praneeth-kandula.medium.com/running-python-scripts-on-an-aws-ec2-instance-8c01f9ee7b2f)

[Andreas Nagy - How to run a Python script in the cloud?](https://medium.com/@andras1000_18467/how-to-run-a-python-script-in-the-cloud-e486eef96ac3)

[Minho Ryang - Connect AWS EC2 Instance with PyCharm Professional](https://minhoryang.github.io/en/posts/connect-aws-ec2-instance-with-pycharm-professional/)

