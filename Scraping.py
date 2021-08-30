# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


#Define a function to:
#1. Initialize the browser
#2. Create a data dictionary
#3. End the webdriver and return the scraped data

    
#the word "browser" of the function, tells python that we will be using the browser variable defined outside the function
def mars_news(browser):

    #Scrape mars news
    # Visit the Mars news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

#By adding the "try" we´re telling python to look for these elements. If there´s an error, will continue to run the reminder of the code
    try:

        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image


#make a function definition

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

    # Add try/except for error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel
    except AttributeError:
        return None
    
    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
        
    return img_url



# ## Mars Facts

def mars_facts():

    # Add try/except for error handling
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
# Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


# hemisphere function
def hemisphere(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    img_soup = soup(html, 'html.parser')

    hemisphere_image_urls = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    hemisphere= img_soup.find_all('div', class_="item")
    hemisphere
    
    for image in hemisphere:
        title = image.find('h3').text
        url = image.find('img', class_='thumb').get('src')
        complete_url = f'https://astrogeology.usgs.gov/cache/{url}'
        print(title)
        print(complete_url)
        
        info= dict({'img_url':complete_url,'title': title})
        hemisphere_image_urls.append(info)

    return hemisphere_image_urls

def scrape_all():
    #Set up Splinter
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    #setting news title and news paragraph variables
    news_title, news_paragraph = mars_news(browser)
    
    #create the data dictionary
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemisphere_images": hemisphere (browser),
        "last_modified": dt.datetime.now(),
        
        }
    
    # Stop webdriver and return data
    browser.quit()
    return data 


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
