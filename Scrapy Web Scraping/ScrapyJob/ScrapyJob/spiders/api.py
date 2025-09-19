# This spider has scraped the job advertisement website from the command line.
# Result are written into jobitems.json for further analysis.

import scrapy
import os
from dotenv import load_dotenv  # Load environment variables from a .env file
from scraperapi_sdk import ScraperAPIClient  # SDK for ScraperAPI proxy service
from ..items import JobItem  # Custom item class to structure scraped job data

# Load API key from environment
load_dotenv()
api_key = os.getenv("API_KEY")
client = ScraperAPIClient(api_key)  # Initialize ScraperAPI client with the key

class ApiSpider(scrapy.Spider):
    name = "api"  # Unique spider name
    start_urls = ['https://www.profession.hu/en/advertisements']  # Initial target URL

    def start_requests(self):
        # Wrap the target URL with ScraperAPI proxy to bypass bot detection
        proxied_url = f"http://api.scraperapi.com/?api_key={api_key}&url={self.start_urls[0]}"
        yield scrapy.Request(
            url=proxied_url,
            callback=self.parse,  # Send response to parse method
            dont_filter=True  # Prevent Scrapy from filtering duplicate requests
        )

    def parse(self, response):
        # Select all job cards on the page
        job_cards = response.css(".job-card")
        for card in job_cards:
            item = JobItem()  # Create a new item instance for each job

            # Extract visible job details
            item['title'] = card.css(".ga-enhanced-event-click a::text").get(default='').strip()
            item['employer'] = card.css(".link-icon::text").get(default='').strip()
            item['town'] = card.css(".map .fw-inherit::text").get(default='').strip()
            item['tags'] = [tag.strip() for tag in card.css(".job-card__tag::text").getall()]
            item['stress_tags'] = [tag.strip() for tag in card.css(".job-card__tag--stress-call::text").getall()]
            item['timestamp'] = card.css(".w-100::text").get(default='').strip()

            # Extract metadata embedded in HTML attributes
            item['affiliation'] = card.attrib.get("data-affiliation")
            item['item_name'] = card.attrib.get("data-item-name")
            item['application_type'] = card.attrib.get("data-application_type")
            item['category1'] = card.attrib.get("data-category1")
            item['category2'] = card.attrib.get("data-category2")
            item['category3'] = card.attrib.get("data-category3")
            item['category4'] = card.attrib.get("data-category4")
            item['category5'] = card.attrib.get("data-category5")
            item['category6'] = card.attrib.get("data-category6")
            item['currency'] = card.attrib.get("data-currency")
            item['item_brand'] = card.attrib.get("data-item-brand")
            item['item_id'] = card.attrib.get("data-item-id")
            item['link'] = card.attrib.get("data-link")
            item['linktarget'] = card.attrib.get("data-linktarget")
            item['list_id'] = card.attrib.get("data-list-id")
            item['list_index'] = card.attrib.get("data-list-index")
            item['list_name'] = card.attrib.get("data-list-name")
            item['location_id'] = card.attrib.get("data-location-id")
            item['price'] = card.attrib.get("data-price")
            item['prof_category'] = card.attrib.get("data-prof-category")
            item['prof_id'] = card.attrib.get("data-prof-id")
            item['prof_name'] = card.attrib.get("data-prof-name")
            item['prof_position'] = card.attrib.get("data-prof-position")
            item['prof_product_name'] = card.attrib.get("data-prof_product_name")
            item['quantity'] = card.attrib.get("data-quantity")
            item['row_number'] = card.attrib.get("data-row-number")
            item['value'] = card.attrib.get("data-value")
            item['variant'] = card.attrib.get("data-variant")
            item['id'] = card.attrib.get("id")

            yield item  # Send the populated item to the pipeline

        # Handle pagination: get the next page URL
        next_page = response.css("#cvdb-list_block_pager-next::attr(href)").get()
        proxied_next_page = f"http://api.scraperapi.com/?api_key={api_key}&url={next_page}"

        if next_page is not None:
            # Recursively follow the next page link through the proxy
            yield response.follow(proxied_next_page, callback=self.parse)