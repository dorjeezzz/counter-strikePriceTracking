import asyncio
from playwright.async_api import async_playwright
import json
import os
from amazon import get_product as get_amazon_product
from requests import post

FLOAT = "https://csfloat.com"

URLS = {
    CSFLOAT:{
        "search_field_query": 'input[name="field-keywords"]',
        "search_button_query": 'input[value="Go"]',
        #get back to this step later
    }
}

available_urls = URLS.keys()

def load_auth():
    FILE = os.path.join("Scraper","auth.json")
    with open(FILE, 'r') as f: 
        return json.load(f)

cred = load_auth()
auth = f'{cred["username"]}:{cred["password"]}'
browser_url = f'wss://{auth}@{cred["host"]}'
#should successfully take in credentials 
async def search(metadata, page, search_text):
    print(f"Looking for {search_text} on {page.url}")
    search_field_query = metadata.get("search_field_query")
    search_button_query = metadata.get("search_button_query")
    if search_field_query and search_button_query:
        print("Completing input field")
        search_box = await page.wait_for_selector(search_field_query)
        await search_box.type(search_text)
        print("Pressing search button")
        button = await page.wait_for_selector(search_button_query)
        await button.click()
    else: raise Exception("Error: Could not search. Please try again")

    await page.wait_for_load_state()
    return page



def save_results(results):
    data = {"results": results}
    FILE = os.path.join("Scraper", "results.json")
    with open(FILE, "w") as f:
        json.dump(data, f)


#test script
if __name__ == "__main__":
    asyncio.run(main(CSFLOAT, "M4A4 howl"))
