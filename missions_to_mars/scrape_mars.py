# app
import flask
from flask_pymongo import PyMongo

# data wrangling
import pandas as pd

# html gather/parse
from bs4 import BeautifulSoup
import requests
import urllib.parse

# browser
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

# ----------------------------------------

def scrape():

    # browser instance
    browser = Browser('firefox', headless=True)

    # ----------------------------------------

    # latest news: title and paragraph text
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    latest_news_title = browser.find_by_css('div[class="content_title"]').first.text
    latest_news_article = browser.find_by_css('div[class="article_teaser_body"]').first.text

    news_dict = {
        'title' : latest_news_title,
        'article' : latest_news_article
    }

    # ----------------------------------------

    # jpl image
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)
    html = browser.html
    soup = BeautifulSoup(html)

    #tag
    img_html = soup.find(id="full_image")

    #strip partial path
    img_str = str(img_html).split('"')[7]

    #combine
    img_path = urllib.parse.urljoin(url_jpl, img_str)
    
    # featured image dict
    feat_img_dict = {
        'img' : img_path
    }

    # ----------------------------------------

    #mars weather
    url_weather = 'https://twitter.com/marswxreport?lang=en'

    #visit
    browser.visit(url_weather)

    #find str
    weather_data = browser.find_by_css('div[class="js-tweet-text-container"]').first.text

    #build dict
    weather_dict = {
        'weather_data' : weather_data
    }

    # ----------------------------------------

    #mars facts/table
    url_facts = 'https://space-facts.com/mars/'

    #visit
    browser.visit(url_facts)

    #html
    table_html_full = browser.html

    #soup
    soup_table = BeautifulSoup(table_html_full)

    # raw table html
    table_html = soup_table.find(id="tablepress-p-mars")

    table_html = soup_table.find(id="tablepress-p-mars")

    table_df = pd.read_html(table_html.prettify(), flavor='bs4')
    df = table_df[0]

    df = df.rename(columns={0:'attribute', 1:'observation'})

    df_html = df.to_html(index=False).replace('\n', '')

    table_dict = {
        'table' : str(table_html),
        'df': df_html
    }

    # ----------------------------------------
    # slower method, no loop, hardcoded element indexes

    hemisphere_urls = {}

    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url_hemi)
    hemi_element_list = browser.find_by_css('h3')
    hemi_element_list[0].click()

    hemi_url_1 = browser.find_by_text('Sample').first['href']
    hemi_title_1 = browser.find_by_css('h2[class="title"]').first.text

    browser.visit(url_hemi)
    hemi_element_list = browser.find_by_css('h3')
    hemi_element_list[1].click()

    hemi_url_2 = browser.find_by_text('Sample').first['href']
    hemi_title_2 = browser.find_by_css('h2[class="title"]').first.text

    browser.visit(url_hemi)
    hemi_element_list = browser.find_by_css('h3')
    hemi_element_list[2].click()

    hemi_url_3 = browser.find_by_text('Sample').first['href']
    hemi_title_3 = browser.find_by_css('h2[class="title"]').first.text

    browser.visit(url_hemi)
    hemi_element_list = browser.find_by_css('h3')
    hemi_element_list[3].click()

    hemi_url_4 = browser.find_by_text('Sample').first['href']
    hemi_title_4 = browser.find_by_css('h2[class="title"]').first.text

    hemisphere_image_urls = [
        {"title": hemi_title_1, "img_url": hemi_url_1},
        {"title": hemi_title_2, "img_url": hemi_url_2},
        {"title": hemi_title_3, "img_url": hemi_url_3},
        {"title": hemi_title_4, "img_url": hemi_url_4},
    ]   

    # ----------------------------------------

    # full dictionary
    mars = {
        "news": news_dict,
        "feat_img_dict": feat_img_dict,
        "weather_dict": weather_dict,
        "table_dict": table_dict,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # ----------------------------------------

    # return all results
    return mars
