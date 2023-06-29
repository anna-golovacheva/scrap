import csv
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from perfume import Perfume
from settings import BASE_URL, TAG, USAGE_FIRST_REGEXP, USAGE_SECOND_REGEXP, DESCRIPTION_FIRST_REGEXP, \
    DESCRIPTION_SECOND_REGEXP, COUNTRY_FIRST_REGEXP, COUNTRY_SECOND_REGEXP, PAGES, BASE_PRODUCT_URL


def start_selenium(url: str):
    """ Request to a website """
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    options.add_argument("--headless")
    service = Service(executable_path=r'/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    return page_source


def get_soup(selenium_data):
    """Transform data to BS object"""
    soup = BeautifulSoup(selenium_data, 'lxml')
    return soup


def extract_element(whole_string: str, first_regexp: str, second_regexp: str, is_country=False):
    """ Extract an element from a script """
    element_string = ' '
    dirty_element = re.search(first_regexp, whole_string)
    if dirty_element:
        if not is_country:
            element_string = re.search(second_regexp, dirty_element.group(0)).group(0).replace('\\n', '')
        else:
            element_string = re.search(second_regexp, dirty_element.group(0)).group(1).replace('\\n', '')
    return element_string


def get_inner_data(href: str):
    """ Get data from a product page """
    selenium_items = start_selenium(href)
    item_soup = get_soup(selenium_items)
    soup = item_soup.find_all('script')
    if len(soup) >= 4:
        soup = str(soup[4])
        usage = extract_element(soup, USAGE_FIRST_REGEXP, USAGE_SECOND_REGEXP)
        description = extract_element(soup, DESCRIPTION_FIRST_REGEXP, DESCRIPTION_SECOND_REGEXP)
        country = extract_element(soup, COUNTRY_FIRST_REGEXP, COUNTRY_SECOND_REGEXP, is_country=True)
        return description, usage, country
    return []


def parse():
    """Collecting all data to list"""
    items_list = []

    for i in range(1, PAGES):
        page = i
        url = BASE_URL + str(page)
        selenium_items = start_selenium(url)
        all_soup = get_soup(selenium_items)
        soup_items = all_soup.find_all(TAG)
        item_list = []
        for item in soup_items:
            href = BASE_PRODUCT_URL + item.contents[0].attrs['href']
            base = item.contents[0].contents[2]
            item = base.contents[2].text.replace('\n', '')
            name = base.contents[4].text.replace('\n', '')
            price = base.contents[6].text.replace('\n', '').replace(' ' * 7, ' ')
            perfume = Perfume(href, item, name, price)
            inner_data = get_inner_data(perfume.href)
            if inner_data:
                perfume.set_inner_data(*inner_data)
            item_list.append(perfume.get_params())

        items_list += item_list

    return items_list


def save_data_to_file(data: list):
    """Saving product data to csv file"""
    header = ['link', 'item', 'name', 'price', 'description', 'usage', 'country']
    with open('result.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(header)
        writer.writerows(data)
