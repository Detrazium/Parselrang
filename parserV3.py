import requests
from bs4 import BeautifulSoup
import psycopg2
import csv
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.664 YaBrowser/23.9.5.664 Yowser/2.5 Safari/537.36"
}
"""Запись csv в постгресс"""
def into_postgresql():
    connect = psycopg2.connect(database= "my_info_parse", user="postgres", password="", host="127.0.0.1", port="")
    cursor =connect.cursor()

    cursor.execute("""CREATE TABLE itog_shop_footers(
        id integer NOT NULL,
        name text NOT NULL,
        price integer,
        footer text,
        href text NOT NULL
    )""")
    cursor.execute("""COPY itog_shop_footers(id, name, price, footer, href)
        FROM 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Postgres Enterprise Manager\parse_footers.csv'
        DELIMITER ','
        CSV HEADER;
    """)
    connect.commit()
    connect.close()
"""Парсит мужскую обувь"""
def parser():
    def into_cvs(k1, k2, k3):
        with open("parse_shop_sport/parse_footers.csv", "w", newline="", encoding="utf=8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["id", "name", "price", "footer", "href"])
            stack = 0
            for el1, el2, el3 in zip(k1, k2, k3):
                stack += 1
                el2 = el2.find("span", attrs={"class": "product-price__current"}).text[0:-2]
                el3 = el3.text.replace("\n", "|")
                el4 = "https://zenden.ru" + el1.find("a").get("href")
                el1 = el1.text.replace("\n", " ")
                if " " in el2:
                    el2 = el2.replace(" ", "")
                writer.writerow([stack, el1, el2, el3, el4])
                print(stack, el1, el2, el3, el4)

        pass

    def so(driver):
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def parse():
        url = "https://zenden.ru/catalog/men/"
        option = Options()
        option.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        driver = webdriver.Chrome(options=option)
        driver.get(url)
        timer = 0
        while True:
            timer += 1
            print("page: ", timer)
            button = driver.find_element(By.CLASS_NAME, "js-list-load")
            if timer == 71:
                soup = so(driver)
                k1 = soup.select("div.product-card__title")
                k2 = soup.select("div.product-card__price")
                k3 = soup.select("div.product-card__sizes")
                into_cvs(k1, k2, k3)
                return
            time.sleep(1)
            button.click()
            time.sleep(3)
    parser()
def main():
    pass

if __name__ == "__main__":
    main()