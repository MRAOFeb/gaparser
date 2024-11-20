import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from collections import Counter


json = []

c = 0

class GA_Parser:
    def __init__(self, url):
        self.url = url
        self.driver = self.init_webdriver()

    def init_webdriver(self):
        driver = webdriver.Chrome()
        stealth(driver, platform='Win10')
        return driver

    def scroll_down(self, deep, driver):
        driver.set_window_size(21, 78)
        driver.set_window_size(1524, 1024)

        button = driver.find_element(By.XPATH, 
            "/html/body/div/div/div/main/div[2]/div/div/div/div[2]/button").click()

        
        for i in range(deep):
            driver.execute_script('window.scrollBy(0, 500)')
            time.sleep(random.random()/2)


        

    def parse(self):
        self.driver.get(self.url)
        time.sleep(3)

        self.scroll_down(50, self.driver)

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        return soup

    def extract_classes(self, soup):
        classes = []
        for element in soup.find_all('div'):
            if 'class' in element.attrs:
                classes.extend(element['class'])
        return Counter(classes)

    def display_top_classes(self, class_counts, soup, top_n=15):
        for i in range(0,1):
            
            class_name, count = class_counts[i]
            print(f"Class: {class_name}, Count: {count}")

            items = soup.find_all(class_=class_name)
            
            s = []
            for i in range(len(items)):
                j = items[i].get_text().strip()
                if len(j) < 5 and  j.count('+'):
                    continue

                if j.count('₽') and j.count('от') and (not j.count('платежа')):
                    s.append(j.split('\n')[1])
                elif not ( j.count('₽') or j.count('\n')) :
                    s.append(j.replace('  ', '?-').split('?-')[0])
                    s.append(j.replace('  ', '?-').split('?-')[-1])
            
                elif j.count('₽') and  not j.count('от'):
                    s.append(j.split('\n')[0])
                
                
            
            global c
            
            for i in range(0,len(s)-4,3):
                c+=1
                json.append({'id' : c, 'brand' : s[i], 'name' : s[i+1], 'price' : s[i+2]})
            
                
    def close(self):
        self.driver.quit()

def main():

 

    urls = ["https://goldapple.ru/lajm",
        "https://goldapple.ru/makijazh",
        "https://goldapple.ru/uhod"
        ]
    
    for url in urls:     
        parser = GA_Parser(url)

        try:
            soup = parser.parse()
            
            class_counts = parser.extract_classes(soup).most_common()

            parser.display_top_classes(class_counts, soup)
        finally:
            parser.close()

if __name__ == "__main__":
    main()

    with open('data.jsonl', 'w', encoding='utf-8') as file:
        for j in json:
            file.write(str(j) + ',\n')