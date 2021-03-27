from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Create an empty dictionary to store all data gathered with the scrape function
mars_data = {}

def scrape():
    # Splinter setup
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # --------------------------------------------------------
    # 1. Navigate browser to NASA's Mars News site
    news_url = 'https://mars.nasa.gov/news'
    browser.visit(news_url)
    # Build soup
    news_html = browser.html
    soup_news = bs(news_html, "html.parser")

    # Scrape the latest news title and its short preview paragraph
    results = soup_news.find_all('li', class_='slide')
    latest_news_title = results[0].find('div', class_='content_title')
    latest_news_body = results[0].find('div', class_='article_teaser_body')

    # Update dict
    mars_data['news_title'] = latest_news_title.text
    mars_data['news_p'] = latest_news_body.text
    latest_news_link = latest_news_title.a['href']
    news_link = 'https://mars.nasa.gov' + latest_news_link
    mars_data['news_link'] = news_link

    print('-------------')
    print('Mars news scrape completed...')

    # --------------------------------------------------------
    # 2. Navigate browser to JPL Mars Space Images site to grab the featured image
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)
    # Build soup
    jpl_html = browser.html
    soup_jpl = bs(jpl_html, 'html.parser')

    # Scrape the URL of the current featured image
    featured_img = soup_jpl.find_all('a', class_='showimg')[0]['href']
    featured_image_url = jpl_url.replace('index.html', featured_img)

    # Update dict
    mars_data['featured_image_url'] = featured_image_url

    print('-------------')
    print('Mars image scrape completed...')

    # --------------------------------------------------------
    # 3. Use pandas to scrape the facts table on space-facts.com "Mars Facts" 
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df = tables[0]
    # Change column headers
    df = df.rename(columns={0: 'Attributes', 1: 'Facts'})

    # Convert the dataframe to html
    # df.to_html('table.html', index=False, justify='left')

    # Store df row information into a list of dictionaries
    mars_facts = []

    for index, row in df.iterrows():
        mars_facts.append(
            {'attribute': row['Attributes'],
            'fact': row['Facts']
            }
        )

    # Update dict
    mars_data['mars_facts'] = mars_facts

    # Note: we will not be using the "table.html" file. That is only for reference purpose.

    print('-------------')
    print('Mars facts table scrape completed...')

    # --------------------------------------------------------
    # 4. Navigate browser to USGS Astrogeology site to obtain images for each of Mar's hemispheres
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)
    # Build soup
    hem_html = browser.html
    soup_hem = bs(hem_html, 'html.parser')

    # Create an empty list to append hemisphere dictionaries
    hemisphere_image_urls = []

    # Scrape specific divs
    hems = soup_hem.find_all('div', class_='description')

    counter = 1

    for hem in hems:    
        # Scrape hemisphere names
        title = hem.a.text.replace(' Enhanced', '')

        # Use Splinter to click into each listed hemisphere to get high resolution image URL
        url_enhanced = 'https://astrogeology.usgs.gov' + hem.a['href']
        
        browser.visit(url_enhanced)
        enhanced_html = browser.html
        soup_enhanced = bs(enhanced_html, 'html.parser')

        # Get URL
        src_url = soup_enhanced.find('img', class_='wide-image')['src']
        image_url = 'https://astrogeology.usgs.gov' + src_url
        
        print('-------------')
        print(f'Hemisphere {counter}\'s title and URL retrived...')
        
        counter += 1
        
        # Update list to create a list of dictionaries so later it can be appended to mars_data dict...
        hemisphere_image_urls.append(
            {'title': title,
            'image_url': image_url
            }
        )

    # Update dict
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    print('-------------')
    print('Mars hemispheres scrape completed...')

    # Scrape completed.
    # --------------------------------------------------------
    print('-------------')
    print('All scraping activities completed...')

    # Close the browser after scraping
    browser.quit()


    # Return results
    return mars_data


# For testing purposes:
# scrape()
# print(mars_data)
