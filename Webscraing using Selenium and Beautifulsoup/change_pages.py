# sample program to naviagte through pages using click buttons

from selenium import webdriver
import time

PATH = 'C:\Program Files (x86)\chromedriver.exe'
URL = 'https://nitrkl.ac.in/FacultyStaff/EmployeeDirectory/Faculty/'

driver = webdriver.Chrome(PATH)
driver.get(URL)

search = driver.find_element_by_id('ContentPlaceHolder1_PageContent_btnnext')
move_ahead = search.get_attribute('disabled')
while True and not move_ahead:
    time.sleep(5)
    search.click()
    search = driver.find_element_by_id('ContentPlaceHolder1_PageContent_btnnext')
    move_ahead = search.get_attribute('disabled')

time.sleep(10)  
driver.quit()