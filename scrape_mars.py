#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
import pandas as pd
import re
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver

# Scrape the NASA Mars News Site and collect the latest News Title and Paragragh Text
# Assign the text to variables that you can reference later


# In[2]:


path = {'executable_path': './chromedriver.exe'}


# In[3]:


# Obtain html of Mars website
mars_news_url = 'https://mars.nasa.gov/news/'
mars_news_html = requests.get(mars_news_url)


# In[4]:


# Parse html file with BeautifulSoup# Parse 
mars_soup = BeautifulSoup(mars_news_html.text, 'html.parser')


# In[5]:


# Print body of html
print(mars_soup.body.prettify())


# In[6]:


# Find article titles
article_titles = mars_soup.find_all('div', class_='content_title')
article_titles


# In[7]:


# Loop to get article titles# Loop  
for article in article_titles:
    title = article.find('a')
    title_text = title.text
    print(title_text)


# In[8]:


paragraphs = mars_soup.find_all('div', class_='rollover_description')
paragraphs


# In[9]:


# Loop through paragraph texts
for paragraph in paragraphs:
    p_text = paragraph.find('div')
    news_p = p_text.text
    print(news_p)


# In[10]:


# Open browser of Mars space images

#REVIEW LATER
#mars_images_browser = Browser('chrome', headless=False)

mars_images_browser = Browser('chrome', **path)

nasa_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
mars_images_browser.visit(nasa_url)


# In[11]:


# Parse html file with BeautifulSoup
mars_images_html = mars_images_browser.html
nasa_soup = BeautifulSoup(mars_images_html, 'html.parser')


# In[12]:


# Print body of html
print(nasa_soup.body.prettify())


# In[13]:


# Find image link with BeautifulSoup
images = nasa_soup.find_all('div', class_='carousel_items')
images


# In[14]:


# Loop through images
for nasa_image in images:
    image = nasa_image.find('article')
    background_image = image.get('style')
    # print(background_image)
    
  
    re_background_image = re.search("'(.+?)'", background_image)
    # print(re_background_image)
    
    # Convert match object (url link) to string
    # group(0) includes quotations
    # group(1) gets the url link
    search_background_image = re_background_image.group(1)
    # print(search_background_image)
    
    featured_image_url = f'https://www.jpl.nasa/gov{search_background_image}'
    print(featured_image_url)


# In[15]:


# Get weather tweets with splinter
path = {'executable_path': './chromedriver.exe'}
twitter_browser = Browser('chrome', **path)
twitter_url = 'https://twitter.com/marswxreport?lang=en'
twitter_browser.visit(twitter_url)


# In[16]:


# Parse html file with BeautifulSoup
twitter_html = twitter_browser.html
twitter_soup = BeautifulSoup(twitter_html, 'html.parser')


# In[17]:


# Print body 
print(twitter_soup.body.prettify())


# In[18]:


# Find weather tweets with BeautifulSoup
mars_weather_tweets = twitter_soup.find_all('p', class_='TweetTextSize')
mars_weather_tweets


# In[19]:


# Get tweets that begin with 'Sol' which indicate weather
weather_text = 'Sol '

for tweet in mars_weather_tweets:
    if weather_text in tweet.text:
        mars_weather = tweet.text
        print(tweet.text)


# In[20]:


#Mars Facts

# Url to Mars facts website
mars_facts_url = 'https://space-facts.com/mars/'
mars_fact_table = pd.read_html(mars_facts_url)
mars_fact_table


# In[21]:


mars_fact = mars_fact_table[0]

# Switch columns and rows
mars_fact_df = mars_fact.transpose()
mars_fact_df


# In[22]:


# Rename columns
mars_fact_df.columns = [
    'Equatorial diameter',
    'Polar diameter',
    'Mass',
    'Moons',
    'Orbit distance',
    'Orbit period',
    'Surface temperature',
    'First record',
    'Recorded by'
]

mars_fact_df


# In[23]:


c_mars_facts_df = mars_fact_df.iloc[1:]
c_mars_facts_df


# In[24]:


# Print dataframe in html format
mars_facts_html_table = c_mars_facts_df.to_html()
print(mars_facts_html_table)


# In[25]:


# Mars Hemispheres
# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres

path = {'executable_path': './chromedriver.exe'}
usgs_browser = Browser('chrome', **path)
usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
usgs_browser.visit(usgs_url)


# In[30]:


mars_hemispheres_html = usgs_browser.html
mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html, 'html.parser')


# In[31]:


print(mars_hemispheres_soup.body.prettify())


# In[32]:


# Find hemisphere image link and title
mars_hemispheres = mars_hemispheres_soup.find_all('div', class_='description')
mars_hemispheres


# In[33]:


# Create list of dictionaries to hold all hemisphere titles and image urls
hemisphere_image_urls = []


# In[34]:


# Loop through each link of hemispheres on page
for image in mars_hemispheres:
    hemisphere_url = image.find('a', class_='itemLink')
    hemisphere = hemisphere_url.get('href')
    hemisphere_link = 'https://astrogeology.usgs.gov' + hemisphere
    print(hemisphere_link)
    # Visit each link that you just found (hemisphere_link)
    usgs_browser.visit(hemisphere_link)
    
    # Create dictionary to hold title and image url
    hemisphere_image_dict = {}
    
    # Need to parse html again
    mars_hemispheres_html = usgs_browser.html
    mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html, 'html.parser')
    
    # Get image link
    hemisphere_link = mars_hemispheres_soup.find('a', text='Original').get('href')
    hemisphere_title = mars_hemispheres_soup.find('h2', class_='title').text.replace(' Enhanced', '')
    
    # Append title and image urls of hemisphere to dictionary
    hemisphere_image_dict['title'] = hemisphere_title
    hemisphere_image_dict['img_url'] = hemisphere_link
    
    # Append dictionaries to list
    hemisphere_image_urls.append(hemisphere_image_dict)

    print(hemisphere_image_urls)


# In[35]:


# Convert this jupyter notebook file to a python script called 'scrape_mars.py'
get_ipython().system(' jupyter nbconvert --to script --template basic mission_to_mars.ipynb --output scrape_mars')

