import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

def scrape():

    #latest news scrape
    news_url = 'https://mars.nasa.gov/news'
    response = requests.get(news_url)
    soup = bs(response.text, 'lxml')
    all_titles = soup.find_all('div', class_='content_title')
    latest_title = all_titles[0].text.strip()
    paragraphs = soup.find_all('div', class_='rollover_description_inner')
    latest_paragraph = paragraphs[0].text


    #featured image scrape
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    image_html = browser.html
    soup_two = bs(image_html, 'lxml')
    featured_images = soup_two.find('a', class_='button fancybox')
    x = featured_images.get('data-fancybox-href')
    featured_image_url = 'https://www.jpl.nasa.gov' + x

    #twitter scrape
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    response_t = requests.get(twitter_url)
    soup_three = bs(response_t.text, 'html.parser')
    all_tweets = soup_three.find_all('div', class_='js-tweet-text-container')
    mars_weather = all_tweets[0].p.text

    #mars facts table scrape
    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    df = tables[1]
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    #mars hemisphere images scrape
    cerberus_link = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    schiaparelli_link = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    syrtis_major_link = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    valles_marineris_link = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    response_cerberus = requests.get(cerberus_link)
    response_schiaparelli = requests.get(schiaparelli_link)
    response_syrtis_major = requests.get(syrtis_major_link)
    response_valles_marineris = requests.get(valles_marineris_link)

    soup_cerberus = bs(response_cerberus.text, 'html.parser')
    soup_schiaparelli = bs(response_schiaparelli.text, 'html.parser')
    soup_syrtis_major = bs(response_syrtis_major.text, 'html.parser')
    soup_valles_marineris = bs(response_valles_marineris.text, 'html.parser')

    cerberus = soup_cerberus.find('img', class_='wide-image').get('src')
    schiaparelli = soup_schiaparelli.find('img', class_='wide-image').get('src')
    syrtis_major = soup_syrtis_major.find('img', class_='wide-image').get('src')
    valles_marineris = soup_valles_marineris.find('img', class_='wide-image').get('src')

    cerberus_image = 'https://astrogeology.usgs.gov' + cerberus
    schiaparelli_image = 'https://astrogeology.usgs.gov' + schiaparelli
    syrtis_major_image = 'https://astrogeology.usgs.gov' + syrtis_major
    valles_marineris_image = 'https://astrogeology.usgs.gov' + valles_marineris

    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": cerberus_image},
        {"title": "Schiaparelli Hemisphere", "img_url": schiaparelli_image},
        {"title": "Syrtis Major Hemisphere", "img_url": syrtis_major_image},
        {"title": "Valles Marineris Hemisphere", "img_url": valles_marineris_image}
    ]

    #final dictionary
    mars_data = {
        "latest_title": latest_title,
        "latest_paragraph": latest_paragraph,
        "featured_image": featured_image_url,
        "current_weather": mars_weather,
        "mars_facts_table": html_table,
        "cerberus_image": cerberus_image,
        "schiaparelli_image": schiaparelli_image,
        "syrtis_major_image": syrtis_major_image,
        "valles_marineris_image": valles_marineris_image,

    }

    browser.quit()

    return mars_data