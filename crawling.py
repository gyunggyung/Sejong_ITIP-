from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib.request import urlretrieve
import time
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs',{'profile.default_content_setting_values.geolocation':1})
driver = webdriver.Chrome('chromedriver', chrome_options=options)


def get_location():
    driver.get("https://www.google.co.kr/maps")
    new_url = driver.current_url
    while '/@' not in new_url:
        time.sleep(0.5)
        new_url = driver.current_url

    driver.find_element_by_xpath("//button[@aria-label='내 위치 보기']").click()
    while new_url == driver.current_url:
        time.sleep(0.3)
    new_url = driver.current_url

    while int(new_url.split("/@")[1].split("z")[0].split(",")[2]) < 20:
        old_url = new_url
        driver.find_element_by_xpath("//button[@aria-label='확대']").click()
        driver.implicitly_wait(3)
        while old_url == driver.current_url:
            time.sleep(0.3)
        new_url = driver.current_url
        print(new_url)
    coordinate = new_url.split('/@')[1].split(',')[0:2]

    driver.find_element_by_id("searchboxinput").send_keys(",".join(coordinate))
    driver.find_element_by_id("searchbox-searchbutton").click()
    driver.implicitly_wait(3)
    while True:
        time.sleep(0.5)
        new_url = driver.current_url
        print(new_url)
        if "search" in new_url:
            try:
                driver.find_element_by_class_name("section-result")
            except NoSuchElementException:
                print("redirecting")
        elif "place" in new_url:
            try:
                place = driver.find_element_by_xpath("//span[@class='widget-pane-link']")
            except NoSuchElementException:
                print("loading")
                time.sleep(0.2)
            else:
                break
    coordinate.reverse()
    address = place.text.split(' ')
    for s in address:
        if s[-1] == '구':
            coordinate.append(s)
            break

    print(coordinate)
    return coordinate


def url_search(name_to_search, places, current_location):
    if "place" in places[name_to_search]:
        print("searching over - "+name_to_search)
    else:
        driver.get(current_location)
        driver.implicitly_wait(3)

        driver.find_element_by_id("searchboxinput").send_keys(name_to_search)
        driver.find_element_by_id("searchbox-searchbutton").click()
        driver.implicitly_wait(3)

        while True:
            time.sleep(0.5)
            new_url = driver.current_url
            print(new_url)
            if "search" in new_url:
                time.sleep(0.5)
                new_url = driver.current_url
                try:
                    driver.find_element_by_class_name("section-result")
                except NoSuchElementException:
                    print("redirecting")
                else:
                    if "data" in new_url:
                        return
            elif "place" in new_url:
                if "data" in new_url:
                    return


def iter_result(url, dup_chk):
    driver.get(url)
    while True:
        try:
            driver.find_element_by_class_name("section-result")
        except NoSuchElementException:
            print("redirecting")
        else:
            break
    soup = BeautifulSoup(driver.page_source, "html.parser")

    result_list = []
    result_num = int(soup.find("div", {"class":"section-pagination-right"}).find("span").find("span").find_next_sibling().get_text())
    for i in range(1, result_num+1):
        while driver.find_element_by_xpath("//div[@data-result-index='"+str(i)+"']") is None:
            print("loading")
            time.sleep(0.5)
        result = driver.find_element_by_xpath("//div[@data-result-index='"+str(i)+"']")
        while result.find_element_by_class_name("section-result-title") is None:
            time.sleep(0.5)
        name = result.find_element_by_class_name("section-result-title").find_element_by_tag_name("span").text

        if name in dup_chk:
            print(name)

        else:
            data = url.split("z/")[1]
            new_url = url
            for j in range(3):
                old_url = new_url
                driver.find_element_by_xpath("//button[@aria-label='확대']").click()
                driver.implicitly_wait(3)
                while old_url == driver.current_url:
                    time.sleep(0.3)
                new_url = driver.current_url
                print(new_url + "/" + data)
            result.click()
            driver.implicitly_wait(3)
            while soup.find("div", {"class": "section-hero-header white-foreground"}) is None \
                    or "place" not in driver.current_url\
                    or soup is None:
                soup = BeautifulSoup(driver.page_source, "html.parser")
                time.sleep(0.5)
            result_list.append(extract_elements())
            dup_chk.append(name)
            driver.get(url)
    return result_list


def extract_elements():
    obj = driver.page_source
    soup = BeautifulSoup(obj, "html.parser")

    element_list = []
    # name, category, editorial, saturday, sunday, monday, tuesday, wednesday,
    # thursday, friday, score, num of review, in/out, longitude, latitude

    while soup.find("div", {"class":"section-hero-header white-foreground"}) is None:
        print("loading")
        time.sleep(0.5)

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
        date = ["토요일", "일요일", "월요일", "화요일", "수요일", "목요일", "금요일"]
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
        element_list.append(review.get_text()[3:-1])

    # in/out - null
    element_list.append("")

    # coordinate
    coordinate = driver.current_url.split('/@')[1].split(',')[0:2]
    element_list.append(coordinate[1])  # longitude
    element_list.append(coordinate[0])  # latitude

    # image
    driver.implicitly_wait(5)
    while header_description.find("img") is None:
        print("reloading")
        driver.get(driver.current_url)
        driver.implicitly_wait(3)
        time.sleep(7)
    image = header_description.find("img")["src"]
    if image[0:2] == "//":
        image = "https:" + image
    image_name = name + ".jpg"
    urlretrieve(image, "image/"+image_name)
    element_list.append(image_name)

    print(element_list)
    return element_list


def push_to_db():
    db_file = open("Seoul_Place.csv", "r", encoding="utf-8")
    place_list = []
    for row in csv.reader(db_file):
        place_list.append(row[0])
    print(place_list)
    db_file.close()
    db_file = open("Seoul_Place.csv", "a+", encoding="utf-8")
    db = csv.writer(db_file, lineterminator='\n')
    current_location = get_location()

    keywords = {}
    try:
        place_file = open("place_list.txt", "r", encoding="utf-8")
    except FileNotFoundError:
        print("No search keywords. Terminate program.")
        quit()
    else:
        for keyword in place_file.readlines():
            if keyword != "":
                keywords[keyword] = ""
        place_file.close()

    main_url = "https://www.google.com/maps/@"+current_location[1]+","+current_location[0]+",20z"
    for place in list(keywords.keys()):
        print(place)
        url_search(place, keywords, main_url)

    for url in list(keywords.values()):
        result_list = iter_result(url, place_list)
        for result in result_list:
            if result is not None:
                db.writerow(result)
    db_file.close()



if __name__ == "__main__":
    push_to_db()
    driver.close()