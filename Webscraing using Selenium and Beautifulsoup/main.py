from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time


def crawler(req, df):

    soup = BeautifulSoup(req, 'html.parser')
    # print("__________________________________________________________")
    source = soup.find_all('div', attrs={'class': "rs-courses-details pt-50 pb-70"})

    for info in source:

        mini_source = info.find_all('div', attrs={'class': 'container'})
        # print(mini_source[0].find_all('div'))
        profiles = mini_source[1]
        tags = profiles.find_all('div', attrs={'class': 'team-body'})

        for anchor in tags:
            url = anchor.find_all('a', attrs={'class': 'btn btn-danger'})[0].get('href')
            url_req = requests.get(url)
            soup_obj = BeautifulSoup(url_req.text, 'html.parser')

            try:
                name = soup_obj.find_all('h3', attrs={'class': 'team-name'})[0]
            except IndexError:
                print('\nName not found..', url)
                continue
        
            print('\nName of the Prof.: ', name.get_text())
            desg = soup_obj.find_all('p', attrs={'class': 'team-title'})
            for i, ele in enumerate(desg):
                if i == 0:
                    pname = ele.get_text().strip()
                    print('Designation: ', pname)
                elif i == 1:
                    dept = ele.get_text().strip()
                    print('Department: ', dept)
                else:

                    if ele.find_all('i'):
                        # print(ele.find_all('i')[0]['class'])
                        if ele.find_all('i')[0]['class'][-1] == 'fa-phone':
                            contact = ele.get_text().strip().split(',')
                            contact = "/".join([x.rstrip() for x in contact])
                            print('Contact: ', contact)
                        else:
                            contact = None
                        if ele.find_all('i')[0]['class'][-1] == 'fa-envelope-o':
                            email = ele.get_text().strip()
                            email = email.replace('[at]', '@')
                            print('Email: ', email)
                        else:
                            email = None
            df = df.append({'Name': name.get_text(),
                            'Designation': pname,
                            'Department': dept,
                            'Contact': contact,
                            'Email': email}, ignore_index=True)
            
            print(df.head())

            print(len(df), '\n')
    pass

if __name__ == '__main__':

    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    URL = 'https://nitrkl.ac.in/FacultyStaff/EmployeeDirectory/Faculty/'
    driver = webdriver.Chrome(PATH)

    driver.get(URL)

    search = driver.find_element_by_id('ContentPlaceHolder1_PageContent_btnnext')
    move_ahead = search.get_attribute('disabled')
    counter = 1

    result = pd.DataFrame(columns=['Name', 'Designation', 'Department', 'Contact', 'Email'])
    
    while True and not move_ahead:
        print(result.head())
        crawler(driver.page_source, result)

        time.sleep(5)
        print('Moving into the {}th page...'.format(counter + 1))
        search.click()
        counter += 1
        search = driver.find_element_by_id('ContentPlaceHolder1_PageContent_btnnext')
        move_ahead = search.get_attribute('disabled')
    
        '''
        for i in mini_source[:1]:
            print('--------------------------------------------')
            print(i.find_all('div', attrs={'class': 'team-body'}))'''
    
    crawler(driver.page_source, result)
    
    time.sleep(15)
    print('\nQuitting the Driver...')
    driver.quit()

    pass
