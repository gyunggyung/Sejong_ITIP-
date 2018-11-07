from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib.request import urlretrieve
import time
import csv
import re


options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
options.add_argument("--lang=en-US")
driver = webdriver.Chrome('chromedriver', chrome_options=options)


def extract_url(name_to_search, old_url="https://www.google.co.kr/maps?hl=en"):
    if old_url == "https://www.google.co.kr/maps?hl=en":
        driver.get(old_url)
    else:
        driver.find_element_by_class_name("gsst_a").click()
    driver.implicitly_wait(3)

    driver.find_element_by_id("searchboxinput").send_keys(name_to_search)
    driver.find_element_by_id("searchbox-searchbutton").click()
    driver.implicitly_wait(3)

    while True:
        time.sleep(1)
        new_url = driver.current_url
        print(new_url)
        if "search" in new_url:
            try:
                search_result = driver.find_element_by_class_name("section-result")
            except NoSuchElementException:
                print("redirecting")
            else:
                search_result.click()
        elif "place" in new_url:
            if driver.find_element_by_css_selector(".section-hero-header.white-foreground") is not None:
                time.sleep(1)
                return driver.current_url


def extract_elements():
    obj = driver.page_source
    soup = BeautifulSoup(obj, "html.parser")

    element_list = []
    # name, category, editorial, saturday, sunday, monday, tuesday, wednesday,
    # thursday, friday, score, num of review, in/out, longitude, latitude

    # name
    header_description = soup.find("div", {"class":"section-hero-header white-foreground"})
    name = header_description.find("h1", {"class":"section-hero-header-title"}).get_text()
    element_list.append(name)

    # category
    category = header_description.find("button", {"jsaction":"pane.rating.category"})
    if category is None:
        element_list.append("")
    else:
        element_list.append(category.get_text())

    # editorial
    editorial = soup.find("div", {"class":"section-editorial-quote"})
    if editorial is None:
        element_list.append("")
    else:
        element_list.append(editorial.find("span").get_text())

    # open hours
    open_hours = soup.find("table", {"class":"widget-pane-info-open-hours-row-table-hoverable"})
    if open_hours is None:
        element_list.extend(["", "", "", "", "", "", ""])
    else:
        date = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        today = open_hours.find("th", {"class":"widget-pane-info-open-hours-row-header widget-pane-info-open-hours-row-today"})\
                                .find("div").get_text()
        today_idx = date.index(today)
        for idx in range(0,7):
            date[today_idx] = open_hours.find("tr", {"data-copy-key":str(idx)}).find("li").get_text()
            today_idx = (today_idx + 1) % 7
        element_list.extend(date)

    # star
    star = header_description.find("span", {"class":"section-star-display"})
    if star is None:
        element_list.append("")
    else:
        element_list.append(star.get_text())

    # review
    review = header_description.find("button", {"jsaction":"pane.rating.moreReviews"})
    if review is None:
        element_list.append("")
    else:
        element_list.append(review.get_text().split(' ')[0])

    # in/out - null
    element_list.append("")

    # coordinate
    coordinate = driver.current_url.split('@')[1].split(',')[0:2]
    element_list.append(coordinate[1])  # longitude
    element_list.append(coordinate[0])  # latitude

    # image
    driver.implicitly_wait(5)
    image = header_description.find("img")["src"]
    if image[0:2] == "//":
        image = "https:" + image
    image_name = name + ".jpg"
    urlretrieve(image, image_name)
    element_list.append(image_name)

    return element_list


def push_to_db():
    place_list = open("place_list.txt", "r", encoding="utf-8")
    db_file = open("Seoul_Place.csv", "a+", encoding="utf-8")
    db = csv.writer(db_file)
    extracted_url = None
    place = place_list.readline()
    while place:
        place = place.split(".")[1].strip()
        print(place)
        if extracted_url is None:
            extracted_url = extract_url(place)
        else:
            param_tmp = extracted_url
            extracted_url = extract_url(place, param_tmp)
        extracted_elements = extract_elements()
        db.writerow(extracted_elements)
        place = place_list.readline()
    place_list.close()
    db_file.close()


if __name__ == "__main__":
    push_to_db()
    driver.close()