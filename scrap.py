import csv
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By

html_text = requests.get('https://www.tid.gov.hk/service/dir/searchByNature.do').text
links = []
soup = BeautifulSoup(html_text, 'lxml')
a_elements = soup.select("table.listing_table1 a")
# print(a_elements)
for a in a_elements:
    links.append(a.text)
print(links)


for each_link in links:
    driver = webdriver.Chrome()
    driver.get('https://www.tid.gov.hk/service/dir/searchByNature.do')

    link_element = driver.find_element(By.PARTIAL_LINK_TEXT, each_link)
    link_element.click()

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    name_email_list = []


    internal_links=[]
    internal_elements = soup.select("table.listing_table1 a")
    for link in internal_elements:
        link_text = link.text
        if link_text[-1]==" ":
            link_text = link_text[:-1]
        internal_links.append(link_text)
        
    print('length of internal links is',len(internal_links))    
    for every_link in internal_links:
        
        print(every_link+"is clicked")
        new_link_element = driver.find_element(By.PARTIAL_LINK_TEXT,every_link)  # Replace with the actual ID of the element
        new_link_element.click()
        
        try:
            td_element = driver.find_element(By.CSS_SELECTOR, 'td.column2')
            link_text = td_element.find_element(By.TAG_NAME,("a")).text
        except:
            link_text = "N/A"
        print("Link Text:", link_text)
        name_email_list.append([every_link, link_text])
        driver.back()
        driver.refresh()
        print("back to general")
        print(name_email_list)



    with open('name_email_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([' ', ' '])
        
        writer.writerows(name_email_list)
            
        
    driver.close() 
    

