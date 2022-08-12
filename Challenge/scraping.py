
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)
    img_urls_titles = mars_hemis(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres":img_urls_titles,
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# Article Scarping

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #set up html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    #Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        #begin scrapping title
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_p
    except AttributeError:
        return None, None

    return news_title,news_p

# Image Scraping
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #Add try/except error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


# Table Scarping

def mars_facts():
   
    #Add try/except error handling
    try:
       df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    #Assign column and index in df 
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    df


    #if table changes this will keep df updated
    return df.to_html()

#Hemisphere Scarping

def mars_hemis(browser):
    
    # Visit url
    url='https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    for hemis in range(4):
    
        #click the links for each result
        browser.links.find_by_partial_text('Hemisphere')[hemis].click()
        
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        hemis_soup = soup(html, 'html.parser')
        
        #Scrapping
        image_url=hemis_soup.find('li').a.get('href')
        title=hemis_soup.find("h2",class_="title").text
        
        #empty dict to store results
        hemisphere={}
        hemisphere["image_url"]=f'{url}{image_url}'
        hemisphere["title"]=title
        hemisphere_image_urls.append(hemisphere)
        
        #browser back click to repeat in loop
        browser.back()
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

   

