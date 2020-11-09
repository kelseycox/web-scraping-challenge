# Import Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time
import requests

from webdriver_manager.chrome import ChromeDriverManager
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Mars news


def scrape():
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Scrape the news title and paragraph
    news_date = soup.find("div", class_="list_date").text
    news_title = soup.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text

    # Display news
    print(news_date)
    print(news_title)
    print(news_paragraph)

    # Mars Images
    url_images = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_images)
    time.sleep(10)
    img_html = browser.html
    img_soup = BeautifulSoup(img_html, "html.parser")

    # Find image
    image = img_soup.find("article")["style"].replace(
        'background-image: url(', '').replace(');', '')[1:-1]

    # Display url of image
    featured_image_url = f"https://www.jpl.nasa.gov{image}"
    print(featured_image_url)

    # Mars Facts
    url_facts = "https://space-facts.com/mars/"
    browser.visit(url_facts)
    mars_facts = pd.read_html(url_facts)
    mars_facts

    # Create Data Frame
    mars_df = mars_facts[0]
    mars_df.columns = ["Description", "Value"]
    mars_df.set_index("Description", inplace=True)
    mars_df

    # Save to html
    html_table = mars_df.to_html()
    mars_df.to_html("mars_facts.html")
    html_table = mars_df.to_html(classes='table table-striped')
    print(html_table)

    # Mars Hemispheres

    spheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    spheres_response = requests.get(spheres_url)
    spheres_soup = BeautifulSoup(spheres_response.text, 'html.parser')

    findings = spheres_soup.find_all('div', class_='item')
    print(findings)

    spheres_image_url = []

    for finding in findings:

        title = finding.find('h3').text

        h3_url = 'https://astrogeology.usgs.gov' + \
            finding.find('a', class_='itemLink product-item')['href']
        response = requests.get(h3_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        img_url = soup.find('img', class_='wide-image')['src']

    # Example:
    # Example: hemisphere_image_urls = [
    # {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #    {"title": "Cerberus Hemisphere", "img_url": "..."},
    #    {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #    {"title": "Syrtis Major Hemisphere", "img_url": "..."},]

        spheres_image_url.append(
            {"title": title, "img_url": f'https://astrogeology.usgs.gov{img_url}'})

    # Dictionary
    mars_data = {
        "news_date": news_date,
        "title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image_url,
        "mars_facts": html_table,
        "spheres_image_url": spheres_image_url}

    # Quit browser
    browser.quit()

    return mars_data
