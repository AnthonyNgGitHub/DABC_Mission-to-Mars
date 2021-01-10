#!/usr/bin/env python
# coding: utf-8

# In[165]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup


# In[166]:


# Import Pandas
import pandas as pd


# Below block of code works for Windows only, not Mac.

# In[167]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# Assign the url and instruct the browser to visit it

# In[40]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# With the following line, 
# 
#     browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
#     
#    we are accomplishing two things.
# 
# 
# 1. One is that we're searching for elements with a specific combination of tag 
# 
#         (ul and li) 
#         
#       and attribute 
#       
#         item_list and slide
#         
#       respectively.
#         
#    For example, 
#    
#        ul.item_list 
#        
#       would be found in HTML as 
#       
#        <ul class=”item_list”>
# 
#     
# 2. Secondly, we're also telling our browser to wait one second before searching for components. 
# 
#     The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.

# Set up HTML parser

# In[41]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# #### Note 1:
# 
# Notice how we've assigned 
# 
#     slide_elem
#     
#    as the variable to look for the 
#     
#     <ul /> 
#     
#    tag and its descendent (the other tags within the 
#    
#     <ul />
#     
#    element), the 
#    
#     <li />
#     
#    tags? 
#    
# ##### This is our parent element. 
# 
# This means that this element holds all of the other elements within it, and we'll reference it when we want to filter search results even further. 
# 
# The . is used for selecting classes, such as 
# 
#     item_list
#    
#    so the code 
#    
#     'ul.item_list li.slide'
#    
#    pinpoints the 
#    
#     <li />
#      
#    tag with the class of 
#    
#     slide
#     
#    and the 
#    
#     <ul />
#     
#    tag with a class of 
#    
#     item_list. 
#     
# #### Note 2:
# 
# CSS works from right to left, such as returning the last item on the list instead of the first. 
# 
# Because of this, when using 
# 
#     select_one
#     
#    the first matching element returned will be a 
#    
#     <li /> 
#     
#    element with a class of 
#    
#     slide
#     
#    and all nested elements within it.

# #### Search for components
# 
# After opening the page in a new browser, right-click to inspect and activate your DevTools. 
# 
# Then search for the HTML components you'll use to identify the title and paragraph you want.
# 
# We'll want to assign the title and summary text to variables we'll reference later.

# #### Scrape for Title

# In[42]:


slide_elem.find("div", class_='content_title')


# In this line of code, we chained 
# 
#     .find
#     
#    onto our previously assigned variable, 
#    
#     slide_elem.
#     
# When we do this, we're saying, 
# 
#     "This variable holds a ton of information, so look inside of that information to find this specific data." 
#     
# The data we're looking for is the content title, which we've specified by saying, 
# 
#     "The specific data is in a <div /> with a class of 'content_title'."
#     
# The output should be the HTML containing the content title and anything else nested inside of that
# 
#     <div />

# We need to get just the text; the extra HTML stuff isn't necessary.

# In[43]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# #### Scrape for Summary Text

# In[44]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ##### Note
# 
# There will be many matches for the class "article_teaser_body" because there are many articles, each with a tag of 
# 
#     <div /> 
#     
#    and a class of 
#    
#     article_teaser_body. 
#     
# We want to pull the first one on the list, not a specific one, so more than 40 results is fine. 
# 
# In this case, if our scraping code is too specific, we'd pull only that article summary instead of the most recent.
# 
# Because new articles are added to the top of the list, and we only need the most recent one, our search leads us to the first article.

# #### There are two methods used to find tags and attributes with BeautifulSoup:
# 
# 1. When we want only the first class and attribute we've specified, use:
# 
#         .find() 
# 
# 2. When we want to retrieve all of the tags and attributes.
# 
# 
#         .find_all() 
#         
# If we were to use  .find_all()  instead of  .find()  when pulling the summary, we would retrieve all of the summaries on the page instead of just the first one.

# ### Image Scraping

# #### Featured Images
# 
# https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars

# In[45]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# ##### A new automated browser should open to the featured images webpage.

# Taking a look at the button's HTML tags and attributes with the DevTools, we will see that there is a lot of code within the 
# 
#     <a /> tag.
#     
#   Near the end of the attributes in the 
#   
#     <a /> tag 
#     
#   is
#   
#     id=“full_image”. 
#     
# This is significant because in HTML, an id is a completely unique identifier. 
# 
# 
# - Often, a class is used as an identifier, but only for other HTML tags with similar styling. 
# 
# 
# - For example, when we were scraping the articles, we saw that all of the articles had the same class. 
# 
# 
# - None of the other components of that webpage had that class, though. 
# 
# 
# - An id, on the other hand, can only be used one time throughout the entire page.

# In[46]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# #####  The automated browser should automatically "click" the button and change the view to a slideshow of images

# Taking a look at the DevTools again to see what elements we can use for our scraping, there aren't any really unique classes here and no ids at all.
# 
# This brings us to another useful Splinter functionality: the ability to search for HTML elements by text.

# In[47]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# ##### The automated browser should automatically "click" the button and change the view to the page with details behind this full image.

# Let's break down this code.
# 
# 1. The code uses the 
# 
#         is_element_present_by_text() method 
#     
#   to search for an element that has the provided text, in this case “more info.” 
#   
#  We've also added an additional argument, 
#  
#         wait_time=1. 
#         
#   This allows the browser to fully load before we search for the element. 
#   
#   Once this line is executed, it will return a Boolean to let us know if the element is present (true) or not (false).
#   
#   
# 2. Next, we create a new variable, 
# 
#         more_info_elem
#         
#    where we employ the 
#    
#         browser.links.find_by_partial_text() method. 
#         
#    This method will take our string ‘more info’ to find the link associated with the "more info" text.
#    
#    
# 3. Finally, we tell Splinter to click that link by chaining the 
# 
#         .click() function
#         
#     onto our 
#     
#         more_info_elem variable.
#          
# All together, these three lines of code check for the "more info" link using only text, store a reference to the link to a variable, then click the link.

# With the new page loaded onto our automated browser, it needs to be parsed so we can continue and scrape the full-size image URL

# In[48]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# It's important to note that the value of the src will be different every time the page is updated, so we can't simply record the current value—we would only pull that image each time the code is executed, instead of the most recent one.
# 
# We'll use all three of these tags 
# 
#     (<figure />, <a />, and <img />) 
#   
#   to build the URL to the full-size image. 

# In[49]:


# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# What we've done here is tell BeautifulSoup to look inside the 
# 
#     <figure class=”lede” /> 
#     
#    tag for an 
#    
#     <a /> tag
#     
#    and then look within that 
#    
#     <a /> tag 
#     
#    for an 
#    
#     <img /> tag. 
#     
# Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."
# 
#     
# We pull the link to the image with
# 
#     .get("src") 

# Add the base URL

# In[50]:


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts Scraping

# Let's look at the webpage again, this time using our DevTools. 
# 
# All of the data we want is in a 
# 
#     <table /> tag. 

# Tables in HTML are basically made up of many smaller containers. 
# 
# The main container is the 
# 
#     <table /> tag. 
#     
#   Inside the table is 
#   
#     <tbody />
#     
#   which is the body of the table—the headers, columns, and rows.
# 
# 
# Next,
# 
#     <tr />
#     
#   is the tag for each table row. 
#   
#   Within that tag, the table data is stored in 
#   
#     <td /> tags. 
#     
#   This is where the columns are established.

# Instead of scraping each row, or the data in each 
# 
#     <td />
#  
#  we're going to scrape the entire table with Pandas' 
#  
#     .read_html() 
#     
#  function.
#  
#  
# At the top of the Jupyter Notebook, add 
# 
#     import pandas as pd 
#     
#   to the dependencies and rerun the cell. 
#   
#   This way, we'll be able to use this new function without generating an error.

# In[51]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# With this line, 
# 
#     df = pd.read_html('http://space-facts.com/mars/')[0]
# 
#   we're creating a new DataFrame from the HTML table. 
#   
#   The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. 
#   
#   By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. 
#   
#   Then, it turns the table into a DataFrame.

# Here, we assign columns to the new DataFrame for additional clarity.
# 
#     df.columns=['description', 'value']

# In the next line,
# 
#     df.set_index('description', inplace=True)
# 
# By using the 
# 
#     .set_index() function 
#     
#    we're turning the Description column into the DataFrame's index. 
#    
#     inplace=True 
#     
#    means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.

# Our data is live—if the table is updated, then we want that change to appear in the app also.
# 
# Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the 
# 
#     .to_html() function

# In[52]:


df.to_html()


# ### Mars Weather 

# In[53]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[54]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[55]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# ### End the automated browsing session

# In[168]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[169]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

title_names =[]
image_urls = []
    


# In[170]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.

html = browser.html
hemi_soup = soup(html, 'html.parser')

full_rel_paths = []
enhanced_img_urls = []

div_items = hemi_soup.find_all("div", class_="item")
for div_item in div_items:
    a_class = div_item.find('a')
    rel_path = a_class['href']
    full_rel_path = f'https://astrogeology.usgs.gov{rel_path}'
    print(full_rel_path)
    full_rel_paths.append(full_rel_path)

for full_rel_path in full_rel_paths:
    browser.visit(full_rel_path)
    html = browser.html
    enhanced_soup = soup(html, 'html.parser')
    div_block = enhanced_soup.select('div.downloads a')
    enhanced_hrefs = [link['href'] for link in div_block]
    enhanced_img_url = enhanced_hrefs[0]
    print()
    print(enhanced_img_url)
    image_urls.append(enhanced_img_url)
    
print()
print(image_urls)


# In[171]:


titles_raw = hemi_soup.find_all('h3')
for title_raw in titles_raw:
    title_name = title_raw.get_text().strip()
    title_names.append(title_name)

print(title_names)


# In[172]:


hemisphere_image_urls = [{'image_url':L1, 'title':L2} for (L1,L2) in zip(image_urls, title_names)]


# In[173]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[174]:


browser.quit()


# In[ ]:




