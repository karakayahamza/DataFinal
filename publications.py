import os

from bs4 import BeautifulSoup
from flask import Flask, render_template
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


class Publications:
    print("Hello")

    def getData(self):
        driver = webdriver.Chrome()
        # Sayfayı açma
        url = "http://boracanbula.com.tr/"
        driver.get(url)
        # CSS seçicisiyle öğeyi bulma

        raw_button1 = driver.find_element(By.XPATH, "/html/body/main/div/div[2]/ul/li[4]")
        raw_button1.click()

        html_element = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[4]")
        html_content = html_element.get_attribute("innerHTML")

        soup = BeautifulSoup(html_content, 'html.parser')
        publications = []

        ul_tags = soup.find_all('ul')

        for ul in ul_tags:
            li_tags = ul.find_all('li')

            for li in li_tags:
                a_tag = li.find('a')
                title = a_tag.text.strip()
                url = a_tag['href']

                spans = li.find_all('span')
                authors = spans[0].text.strip()
                publication_info = spans[1].text.strip()

                article = {
                    'title': title,
                    'url': url,
                    'authors': authors,
                    'publication_info': publication_info
                }

                publications.append(article)
        driver.quit()

        # Get the project directory path
        project_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the file path
        file_path = os.path.join(project_dir, 'data.json')

        # Save data to JSON file
        with open(file_path, 'w') as file:
            json.dump(publications, file)
