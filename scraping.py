
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup

# Import Pandas
import pandas as pd

# Import Datetime
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    # Set news title and paragraph variables as the mars_news() function returns 2 values
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres" : hemisphere_scrape(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Define function for scraping news title and summary from NASA with the variable "browser" as the argument

def mars_news(browser):

    # Assign the url and instruct the browser to visit it

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Set up HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        # #### Scrape for Title
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')

        # We need to get just the text; the extra HTML stuff isn't necessary.

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        
        # #### Scrape for Summary Text

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p

# Define function for scraping featured image from NASA with the variable "browser" as the argument

def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # With the new page loaded onto our automated browser, it needs to be parsed so we can continue and scrape the full-size image URL

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None
        
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url


# Define function for scraping from space-facts

#### Mars Facts Scraping

def mars_facts():

    try:    
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe    
    df.columns=['description', 'Mars']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-hover")

def hemisphere_scrape(browser):

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls = []

    title_names =[]
    image_urls = []

    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    full_rel_paths = []
    enhanced_img_urls = []

    div_items = hemi_soup.find_all("div", class_="item")
    for div_item in div_items:
        a_class = div_item.find('a')
        rel_path = a_class['href']
        full_rel_path = f'https://astrogeology.usgs.gov{rel_path}'
        full_rel_paths.append(full_rel_path)

    for full_rel_path in full_rel_paths:
        browser.visit(full_rel_path)
        html = browser.html
        enhanced_soup = soup(html, 'html.parser')
        div_block = enhanced_soup.select('div.downloads a')
        enhanced_hrefs = [link['href'] for link in div_block]
        enhanced_img_url = enhanced_hrefs[0]
        image_urls.append(enhanced_img_url)

    titles_raw = hemi_soup.find_all('h3')
    for title_raw in titles_raw:
        title_name = title_raw.get_text().strip()
        title_names.append(title_name)

    hemisphere_image_urls = [{'image_url':L1, 'title':L2} for (L1,L2) in zip(image_urls, title_names)]

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())