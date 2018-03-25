import selenium, bs4
import time
import os
import copy
import re
import pickle
import json

from collections import defaultdict

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Firefox()
seasons = ["spring", "autumn", "winter", "summer"]

result = defaultdict(list)

for season_name in seasons:
    browser.get("http://www.color-hex.com/color-palettes/popular.php")
    query_field = browser.find_element_by_id("paletteSearchInput")
    query_field.send_keys(season_name)
    query_field.send_keys(Keys.RETURN)
    time.sleep(1)
    content = copy.deepcopy(browser.page_source)
    soup = BeautifulSoup(content, "lxml")
    queries = []
    for link in soup.find_all('a', attrs={'href': re.compile("^/")}):
        if "color-palette" in str(link) and season_name in str(link).lower():
            title = str(link.get("title")).lower()
            array = title.strip().split()[2:]
            if len(array) <= 2 and season_name in array:
                queries.append("http://www.color-hex.com" + str(link.get('href')))
    for link in queries:
        browser.get(link)
        content = copy.deepcopy(browser.page_source)
        soup = BeautifulSoup(content, "lxml")
        for item in soup.find_all('td'):
            item_str = str(item)
            item_str = item_str[4:-5]
            if item_str.startswith("(") and item_str.endswith(")"):
                item_arr = item_str[1:-1].split(",")
                rgb = [int(val) for val in item_arr]
                result[season_name].append(rgb)

with open("colors.json", "w") as fp:
    json.dump(result, fp, indent=4)




