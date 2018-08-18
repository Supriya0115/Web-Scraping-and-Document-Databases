# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import time

# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/ChromeSafe/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Function to scrape and consolidate mars data
def scrape():

    # Initialize browser
    browser = init_browser()
    mars_data = {}

    # Web Scraping :  NASA Mars News 
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_url)

    # Retrieve page with the browser module, Create BeautifulSoup object; parse with 'html.parser'

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the latest News Title and Paragraph Text

    news_title = soup.find('li',class_="slide").find('div',class_="content_title").text
    news_summary = soup.find('li',class_="slide").find('div',class_="article_teaser_body").text

    # Add to the dictionary  mars_data
    mars_data['News_Title'] = news_title
    mars_data['News_Summary'] = news_summary

    # Web Scraping : Mars Space Images - Featured Image

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # Retrieve page with the browser module, Create BeautifulSoup object; parse with 'html.parser'

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the featured_image_url

    image = soup.find(class_="button fancybox")["data-fancybox-href"]

    featured_image_url = "https://www.jpl.nasa.gov/" + image

    mars_data['Featured_Image_url'] = featured_image_url

    # Web Scraping : Mars Weather from Twitter 

    mars_twitter_url = 'https://twitter.com/MarsWxReport?lang=en'
    browser.visit(mars_twitter_url)
    time.sleep(10)

    # Retrieve page with the browser module, Create BeautifulSoup object; parse with 'html.parser'

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the featured_image_url

    mars_weather_tweet  = soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    mars_data['Weather_Tweet'] = mars_weather_tweet

    # Web Scraping : Mars Facts 

    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)

    mars_facts_table = pd.read_html(mars_facts_url)
    mars_facts_df = pd.DataFrame(mars_facts_table[0])
    mars_facts_df.columns = ['Attribute','Value']
    mars_facts_df = mars_facts_df.set_index('Attribute')

    # Dataframe to HTML Table
    mars_html_table = mars_facts_df.to_html(classes="mars-facts")
    # mars_html_table = mars_html.replace('\n', ' ')

    mars_data['Facts_Table'] = mars_html_table
    
    # Web Scraping : Mars Hemispheres 

    mars_hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hem_url)

    hemisphere_image_urls = []

    # Retrieve page with the browser module, Create BeautifulSoup object; parse with 'html.parser'

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # results are returned as an iterable list

    results = soup.find('div', class_='result-list').find_all('div',class_='item')

    # Image URL to be appended for each iteration

    root_image_url = 'https://astrogeology.usgs.gov/'

    for result in results:
        title = result.find('div',class_='description').h3.text
        
        # split the h3 text to remove "enhanced" from each hemisphere name e.g. Cerberus Hemisphere Enhanced
        title_split_join = ' '.join(title.split()[0:2]) 
        
        # create url for each hemisphere image
        image_url = root_image_url + result.find('a',class_='itemLink product-item')['href']
        browser.visit(image_url)
        time.sleep(10)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        final_image_url = soup.find('div',class_='downloads').a['href']
        
        hemisphere_image = {
            "title" : title_split_join,
            "image_url" : final_image_url
        }
        hemisphere_image_urls.append(hemisphere_image)
        browser.back()

    mars_data['Hemisphere_Image_urls'] = hemisphere_image_urls
    
    # return mars_data

    return {
        "News_Title": mars_data['News_Title'],
        "News_Summary" :mars_data['News_Summary'],
        "Featured_Image" : mars_data['Featured_Image_url'],
        "Weather_Tweet" : mars_weather_tweet,
        "Facts" : mars_html_table,
        "Hemisphere_Image_urls": hemisphere_image_urls,
        "Date" : datetime.datetime.utcnow(),
    }



