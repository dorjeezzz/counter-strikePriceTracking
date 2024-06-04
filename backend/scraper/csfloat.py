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
    
    if image_url: 
        image_url = await image_element.get_attribute('src')
    else:
        None
    if name_element:
        name_url = await name_element.inner_text()
    else:
        None
    try:
        print((await price_element.inner_text()).replace('$',"").replace(',',"").strip())
        product_price = float((await price_element.inner_text()).replace('$',"").replace(',',"").strip()) if price_element else None
    except:
        product_price = None
    product_url = "/".join((await url_element.get_attribute('href')).split('/')[:4]) if url_element else None

    return {"img": image_url, "name": product_name, "pric": product_price, "url": product_url}