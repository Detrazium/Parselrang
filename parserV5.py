import csv
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time

"""
/Спарсить каталог через селениум
/пройтись по всем ссылкам
/спарсить все возможные материалы
/1.название товара/2.наличие/3.код товара(артикул)/4.цена/5.ссылка на твоар/
"""

"""Запись csv в постгресс"""
def parse_info_into_to_postgresql():
    connect = psycopg2.connect(database="my_info_parse", user="postgres", password="", host="127.0.0.1", port="")
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE parse_igroray(
        id integer NOT NULL,
        name text NOT NULL,
        availability text NOT NULL,
        code_product text,
        price integer NOT NULL,
        hrefs text NOT NULL
    )""")
    cursor.execute("""COPY parse_igroray(id, name, availability, code_product, price, hrefs)
    FROM 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Postgres Enterprise Manager\Parse_V5_magasine.csv'
    DELIMITER ','
    CSV HEADER;
    """)
    connect.commit()
    connect.close()
"""Проход по всем ссылкам каталога и запись файла"""
def ParserII():
    with open("parse_shop_sport/Parse_V5_magasine.csv", "w", newline="", encoding="utf=8") as csv_write, open("parse_shop_sport/parserV5_hrefs.text", "r", encoding="utf=8") as file:
        writer = csv.writer(csv_write)
        writer.writerow(["id", "name", "availability", "code_product", "price", "hrefs"])
        def soup_casual(url):
            responce = requests.get(url)
            soup = BeautifulSoup(responce.text, "html.parser")
            return soup

        def soup_driver(driver):
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            return soup
        def into_csv(itog):
            writer.writerow([itog[0], itog[1], itog[2], itog[3], itog[4], itog[5]])
            time.sleep(0.05)
            print(itog)

        def items_itog(soups, stack):
            for el1, el2, el3 , el4 in zip(soups[0], soups[1], soups[2], soups[3]):
                stack += 1
                k1 = el1.text.replace('\n', '')
                k2 = el2.text
                k3 = el3.text.split(" ")[-1].replace("\n", "").replace("\t", "")
                k4 = el4.find("span", attrs={"class": "values_wrapper"}).text.replace(" ", "")[:-4]
                k5 = "https://igroray.ru" + el1.find("a").get("href")
                itog = (stack, k1, k2, k3, k4, k5)
                into_csv(itog)
            time.sleep(3)
            return stack

        def parse_page(soup, stack):
            #prices_stack full = 36
            name = soup.select("div.item-title") #"""el1"""
            availability= soup.select("div.item-stock") #"""el2
            code_product = soup.select("div.article_block") #"""el3
            price = soup.select("div.price_matrix_wrapper") #"""el4
            soups = (name, availability, code_product, price)
            stack = items_itog(soups, stack)
            return stack

        def driver(url, stack):
            option = Options()
            option.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            driver = webdriver.Chrome(options=option)
            driver.get(url)
            key_bottom = soup_casual(url).select("div.nums")
            if key_bottom != []:
                for num in key_bottom:
                    itog = int(num.text.split("\n")[-2])
                st = 1
                print(f"itog page: {itog} ==___")
                while st != itog:
                    if st != itog:
                        print(f"... hovers to page process: {st} :|||: {itog}")
                    time.sleep(2)
                    elm = driver.find_element(By.CLASS_NAME, "ajax_load_btn")
                    time.sleep(1)
                    elm.click()
                    time.sleep(2)
                    st += 1
                print("\n==________(((( PARSE TO ITEMS PAGE ! ))))________==")
                stack = parse_page(soup_driver(driver), stack)
                return stack
            else:
                stack = parse_page(soup_driver(driver), stack)
            return stack

        def pars_hrefs_catalog():
                stack = 0
                for line in file:
                    if "https:"in line:
                        print(f"\n\n\t===------------\n\t Parse in process: {line} \n\t===------------\n\n\t")
                        stack = driver(line, stack)
                    time.sleep(7)
        pars_hrefs_catalog()
"""Парсинг каталога"""
def ParserI():
    url_catalog = "https://igroray.ru/catalog/"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.664 YaBrowser/23.9.5.664 Yowser/2.5"
    }
    def soup_p(url):
        responce = requests.get(url, headers=header)
        soup = BeautifulSoup(responce.text, "html.parser")
        return soup

    def core():
        with open("parse_shop_sport/parserV5_hrefs.text", "w", encoding="utf=8") as file:
            soup = soup_p(url_catalog)
            named = soup.select("li.name")
            k = 0
            for el in named:
                k += 1
                print(el.text.replace("\n", ""))
                print("https://igroray.ru" + el.find("a").get("href"), "\n")
                file.write("\n" + str(k) + "\t" + el.text.replace("\n", "")+'\n' + "https://igroray.ru" + el.find("a").get("href"))
                time.sleep(1)
    core()

def main():
    pass
    # ParserI(), ParserII(), parse_info_into_to_postgresql()
if __name__ == "__main__":
    main()
