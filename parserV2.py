import csv
from bs4 import BeautifulSoup
import requests
import time
import psycopg2
"""Запись csv в постгресс"""
def into_to_postgresql():
    connect = psycopg2.connect(database="my_info_parse", user="postgres", password="", host="127.0.0.1", port="")
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE itog_to_parse_ultrasport(
        id integer NOT NULL,
        name text NOT NULL,
        href text NOT NULL,
        price integer
    )""")
    cursor.execute("""COPY itog_to_parse_ultrasport(id, name, href, price)
    FROM 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Postgres Enterprise Manager\parse_V2_CSV'
    DELIMITER ','
    CSV HEADER;
    """)

    connect.commit()
    connect.close()
"""Парсит информацию из магазина спорт товаров"""
def Parse_I_geat():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.664 YaBrowser/23.9.5.664 Yowser/2.5 Safari/537.36"
    }
    url = "https://ultrasport.ru/"
    with open("parse_shop_sport/parse_V2_magasine_sport", "r", encoding="utf=8") as file, open("parse_shop_sport/parse_V2_CSV", "w", newline="", encoding="utf=8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["id", "name", "href", "price"])
        stack_up = [400]

        def soup_f(url):
            responce = requests.get(url, headers=header)
            soup = BeautifulSoup(responce.text, "html.parser")
            return (soup)

        def into_csv(stack, el1, eli2, eli3, stack_up):
            stack += 1
            csv_writer.writerow([stack, el1, eli2, eli3])
            print(stack, el1, eli2, eli3)
            if stack == stack_up[-1]:
                stack_up.append(stack_up[-1]+400)
                time.sleep(180)
            time.sleep(0.06)
            return stack

        def one_page(soup, stack):
            item = soup.select("div.item_info")
            for el in item:
                el1 = el.find("a", attrs={"class": "dark_link"}).text
                eli2 = "https://ultrasport.ru" + el.find("a").get("href")
                eli3 = el.find("span", attrs={"class": "price_value"}).text
                if " " in eli3:
                    eli3 = eli3.replace(" ", "")
                stack = into_csv(stack, el1, eli2, eli3, stack_up)
                return stack

        def end_p(soup):
            end_page = soup.select("div.nums")
            if end_page == []:
                return []
            for el in end_page:
                end = el.text.replace("\n", " ").strip().split(" ")
                end = int(end[-1])
            print(f"page to end: {end}\n")
            return end

        def page_href_code(soup):
            next = soup.select("div.nums")
            for el in next:
                key = el.find("a", attrs={"class": "dark_link"}).get("href")
                key = key[0:key.find("=") + 1]
            return key

        def page(soup, stack):
            end = end_p(soup)
            if end == []:
                stack = one_page(soup, stack)
                return stack
            k = 1
            time.sleep(0.1)
            next = page_href_code(soup)
            while k < end+1:
                item = soup.select("div.item_info")
                for el in item:
                    el1 = el.find("a", attrs={"class": "dark_link"}).text
                    eli2 = "https://ultrasport.ru" + el.find("a").get("href")
                    eli3 = el.find("span", attrs={"class": "price_value"})
                    if eli3 != None:
                        eli3 = eli3.text
                        if " " in eli3:
                            eli3 = eli3.replace(" ", "")
                    stack = into_csv(stack, el1, eli2, eli3, stack_up)
                    time.sleep(0.4)
                k += 1
                new_href = f"https://ultrasport.ru{next}"+ str(k)
                soup = soup_f(new_href)
                time.sleep(1)
                if k < end:
                    print(f"\npage: {k}\n")
                    print(new_href, "\n")
            return stack
        def items():
            stack = 0
            for line in file:
                if "https:" in line:
                    print(f"parse in to page: {line}")
                    stack = page(soup_f(line[:-1]), stack)
                    time.sleep(20)
        items()

def main():
    pass

if __name__ == "__main__":
    main()

