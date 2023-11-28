import requests
from bs4 import BeautifulSoup
import csv
import psycopg2
import time
"""
Спарсить все мобилки0
"""

"""Запись csv в постгресс"""
def into_postgresql():
    connect = psycopg2.connect(database="my_info_parse", user="postgres", password="", host="127.0.0.1",
                               port="")
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE to_parse_phone(
        id integer NOT NULL,
        name text NOT NULL,
        operation text NOT NULL,
        price integer NOT NULL,
        product_code text NOT NULL,
        href text NOT NULL
    )""")
    cursor.execute("""COPY to_parse_phone(id, name, operation, price, product_code, href)
    FROM 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Postgres Enterprise Manager\\to_parse_phone.csv'
    DELIMITER ','
    CSV HEADER;
    """)
    connect.commit()
    connect.close()
"""Код вытаскивает всю инфу о мобилках с сайта"""
def parser():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.664 YaBrowser/23.9.5.664 Yowser/2.5 Safari/537.36"
    }
    with open("parse_shop_sport/to_parse_phone.csv", "w", encoding="utf=8", newline="") as csv_file:
        write = csv.writer(csv_file)
        write.writerow(['id', 'name', 'operation', 'price', 'product_code', 'href'])
        def into_csv(key):
            print(key)
            time.sleep(0.1)
            write.writerow([key[0], key[1], key[2], key[3], key[4], key[5]])

        def so(url):
            responce = requests.get(url, headers=headers)
            soup = BeautifulSoup(responce.text, "html.parser")
            return soup
        def price_form(price):
            k = []
            p = None
            for el in price:
                p = el.find("div", attrs={"class": "new-price"})
                if p == None:
                    p = el.find("div", attrs={"class": "list-price"})
                k.append(p)
            return k

        def operation_slip(operation):
            k = []
            for el2 in operation:
                k.append(el2.text.replace("\n", "|"))
            return k
        def item_p(soup):
            name = soup.select("div.list_name")
            operation = operation_slip(soup.select("div.list_attrs"))
            price = price_form(soup.select("div.list-td-price"))
            product_code = soup.select("div.list-code")

            soups = (name, operation, price, product_code)
            return soups

        def parse():
            url = "https://www.niceprice62.ru/telefony/mobilnye-telefony/"
            stack = 0
            end = 1
            while end < 59:
                time.sleep(3)
                print(f"===-----------\npage to parse process: {end}\n===-----------")
                time.sleep(3)
                key = so(url)
                item = item_p(key)
                url = f"https://www.niceprice62.ru/telefony/mobilnye-telefony/page-{end}/"
                end += 1
                for el1, el2, el3, el4 in zip(item[0], item[1], item[2], item[3]):
                    stack += 1
                    k1 = el1.text.replace("\n","")
                    k2 = el2
                    k3 = el3.text.replace(" ","")[:-1].replace("\r\n","")
                    k4 = el4.text
                    k5 = "https://www.niceprice62.ru" + el1.find("a").get("href")
                    itog = (stack, k1, k2, k3, k4, k5)
                    into_csv(itog)



        parse()
def main():
    pass

if __name__ == "__main__":
    main()