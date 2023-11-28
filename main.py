import csv
import psycopg2
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

"""please"""
'''Parse_catalog'''
"""please"""
# def parse_catalog():
#     headers = {
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.838 YaBrowser/23.9.4.838 Yowser/2.5 Safari/537.36"
#     }
#     url = "https://my-shop.ru/"
#     with open("Pape.txt", "w", encoding="utf=8") as file:
#         def so(driver):
#             html = driver.page_source
#             soup = BeautifulSoup(html, "html.parser")
#             return soup
#
#         def Catalog_hrefs_get(driver):
#             k = 0
#             hrefs = so(driver).select("a.menu__list__link")
#             for el in hrefs:
#                 print("\n\t===\n\t"+el.text+"\n"+"\thttps://my-shop.ru"+el.get("href")+"\t")
#                 file.write("\n\t===\n\t"+el.text+"\n"+"\thttps://my-shop.ru"+el.get("href")+"\t")
#                 k += 1
#         def driver_move():
#             options = Options()
#             options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
#             # options.add_experimental_option("detach", True)
#             driver = webdriver.Chrome(options=options)
#             driver.get(url)
#             button = driver.find_element(By.CLASS_NAME, "header__menu")
#             time.sleep(2)
#             button.click()
#             time.sleep(2)
#             category = so(driver).select("a.menu__category")
#             for el, i in zip(category, driver.find_elements(By.CLASS_NAME, "menu__category")):
#                 print("\n__---___--===--___---__\n"+el.text+"\n__---___--===--___---__\n")
#                 file.write("\n__---___--===--___---__\n"+el.text+"\n__---___--===--___---__\n")
#                 time.sleep(2)
#                 Catalog_hrefs_get(driver)
#                 time.sleep(2)
#                 hover = ActionChains(driver).move_to_element(i).perform()
#                 time.sleep(2)
#
#         def main():
#             driver_move()
#         main()
"""Parse II"""
# def parse_book():
#     with open("Pape_2.txt", "r", encoding="utf=8") as file_parse_catalog, open("Parse_itog_my_shop_book.csv", "w", encoding='utf=8', newline='') as csv_file:
#         writer = csv.writer(csv_file)
#         writer.writerow(["id_book", "autor_name", "name_book", "href_book", "price_book"])
#         trice = [2000]
#
#         def print_cvs(i):
#             for el in i:
#                 if "\xa0" in el:
#                     i[i.index(el)] = el.replace("\xa0", "")
#             i = tuple(i)
#             # print(i)
#             writer.writerow([(i[0]), i[1], i[2], i[3], i[4]])
#
#         def items(item, stack, cvs_itoger):
#             stack += 1
#             print_cvs(cvs_itoger)
#             print(stack, item)
#             time.sleep(0.05)
#             if stack == trice[-1]:
#                 time.sleep(120)
#                 trice.append(trice[-1] + 2000)
#             return stack
#
#         def soup_k(url):
#             print("\t_____________")
#             print("\tParse in process next url:",url[1:-1])
#             print("\t_____________\n\n")
#             responce = requests.get(url[:-2])
#             soup = BeautifulSoup(responce.text, "html.parser")
#             return soup
#
#         def one_page(soup, stack):
#             price = soup.select("span.rubl")
#             href = soup.select("div.item__title__container")
#             if href == [] or price == []:
#                 return stack
#             for el1, el2 in zip(href, price):
#                 name = el1.find("a", attrs={"class": "item__producer"})
#                 if name == None:
#                     itog = el1.find("span").text + "\nhttps://my-shop.ru" + el1.find("a").get(
#                         "href") + "\nСтоимость: " + el2.text + " Руб." + "\n"
#                     cvs_itoger = [stack, "None", el1.find("span").text, "https://my-shop.ru" + el1.find("a").get(
#                         "href"), el2.text]
#                     cvs_itoger = [str(i) for i in cvs_itoger]
#                 else:
#                     itog = name.text + "\n" + el1.find("span").text + "\nhttps://my-shop.ru" + el1.find("a").get(
#                         "href") + "\nСтоимость: " + el2.text + " Руб." + "\n"
#                     cvs_itoger = [stack, name.text, el1.find("span").text, "https://my-shop.ru" + el1.find("a").get(
#                         "href"), el2.text]
#                     cvs_itoger = [str(i) for i in cvs_itoger]
#                 stack = items(itog, stack, cvs_itoger)
#                 return stack
#
#         def hrefs_parse(soup, core_href, stack):
#             k = 1
#             k2 = 2
#             end = soup.select("span.border")
#             if end == []:
#                 stack = one_page(soup, stack)
#                 return stack
#             for el3 in end:
#                 end_page = int(el3.text)
#             while k != end_page+1:
#                 price = soup.select("span.rubl")
#                 href = soup.select("div.item__title__container")
#                 for el1, el2 in zip(href, price):
#                     name = el1.find("a", attrs={"class": "item__producer"})
#                     if name == None:
#                         itog = el1.find("span").text + "\nhttps://my-shop.ru" + el1.find("a").get(
#                             "href") + "\nСтоимость: " + el2.text + " Руб." + "\n"
#                         cvs_itoger = [stack, "None", el1.find("span").text, "https://my-shop.ru" + el1.find("a").get(
#                             "href"), el2.text]
#                         cvs_itoger = [str(i) for i in cvs_itoger]
#                     else:
#                         itog = name.text + "\n" + el1.find("span").text + "\nhttps://my-shop.ru" + el1.find("a").get(
#                             "href") + "\nСтоимость: " + el2.text + " Руб." + "\n"
#                         cvs_itoger = [stack, name.text, el1.find("span").text, "https://my-shop.ru" + el1.find("a").get(
#                             "href"), el2.text]
#                         cvs_itoger = [str(i) for i in cvs_itoger]
#                     stack = items(itog, stack, cvs_itoger)
#                 core_href = core_href.replace(f"/a/page/{k}.html", f"/a/page/{k2}.html")
#                 print("page:", k, "\n")
#                 if k != 97:
#                     soup = soup_k(core_href)
#                 k = k + 1
#                 k2 = k2 + 1
#                 time.sleep(1)
#             return stack
#         def core_hrefs():
#             stack = 0
#             for el in file_parse_catalog:
#                 if "https:" in el:
#                     stack = hrefs_parse(soup_k(el), el, stack)
#                     time.sleep(20)
#         core_hrefs()
"""Input in postgresql"""
# def input_sql():
#     connection = psycopg2.connect(database="my_info_parse", user="postgres", password="", host="127.0.0.1",
#                                   port="")
#     cursor = connection.cursor()
#
#     cursor.execute("""CREATE TABLE itog_parse_my_shop(
#         	id_book integer NOT NULL,
#         	autor_name text,
#         	name_book text NOT NULL,
#         	hrefs_book text NOT NULL,
#         	price_book integer NOT NULL
#         )""")
#
#     cursor.execute("""
#             COPY itog_parse_my_shop(id_book, autor_name, name_book, hrefs_book, price_book)
#             FROM 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Postgres Enterprise Manager\itog_parse.csv'
#             DELIMITER ','
#             CSV HEADER;
#         """)
#     connection.commit()
#     connection.close()


def main():
    pass

if __name__ == "__main__":
    main()
