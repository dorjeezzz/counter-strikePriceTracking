from asyncio import gather

async def get_stock(product_div):
    elements = await product_div.query_selector_all('.a-size-base')
    filtered_elements = [element for element in elements if 'stock' in await element.inner_text()]
    return filtered_elements

#function should query for all elements at once, then await them all at once
async def get_product(product_div):
    image_element_future = product_div.query_selector('img.s-image')
    name_element_future = product_div.query_selector('h2 a span')
    price_element_future = product_div.query_selector('span.a-offscreen')
    url_element_future = product_div.query_selector('a.a-link-normal.s-no-hover.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')

    image_element, name_element, price_element, url_element = await gather(
        image_element_future,
        name_element_future,
        price_element_future,
        url_element_future
    )

