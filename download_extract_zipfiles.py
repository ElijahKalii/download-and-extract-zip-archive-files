import requests
import time
import os
import zipfile
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

#define the url with the zip file links
URL = 'https://forms.iebc.or.ke/#/downloads?contest=34'

options = Options()
options.headless = True  #we are not interested with the GUI for now
options.add_argument("--window-size=1920,1080")  # set window size to normal size
options.add_argument("start-maximized")  # set window to full-screen

# configure chrome browser to not load images and javascript
chrome_options = webdriver.ChromeOptions()

# disable image loading
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

#define your driver object to send a get request to the url
browser = webdriver.Chrome(executable_path='chromedriver.exe', options=options, chrome_options=chrome_options)
browser.get(URL)

#we want the browser to wait until the website has fully loaded
WebDriverWait(browser, timeout=20).until(EC.presence_of_element_located((By.XPATH, '//td[@class="q-td text-left"]')))

#links_list = []      #create a list to store the data, if you intent to save the scraped data in a file

'''I am using beautiful soup to get the required html elements. 
(You may aas well use the selenium selectors as well). I also use the requests library to send the 
get request to each link I extract using beautifulsoup'''

soup = BeautifulSoup(browser.page_source, 'html.parser')
for line in soup.find_all('td', class_='q-td text-left'):
    county_name = line.text.lower()             
    link = line.find('a', href=True)['href']               
    #filename = f"{link.split('/')[-1].split('.')[0]}"       
    full_link = 'https://forms.iebc.or.ke'+link         #add the url prefix to the link to make a full url
    
    #Some websites will not give you data without headers
    headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    'referer': "https://forms.iebc.or.ke/",
    'accept-language': "en-US,en-GB;q=0.9,en;q=0.8",
    'authority': "forms.iebc.or.ke"}

    '''extract the zip files using the requests library, download the zip files and extract 
    them into a directory/path of your choice'''
    root_dir = 'form34A_zipfiles'
    extract_path = os.path.join(root_dir, county_name)
    with requests.get(full_link, headers=headers) as online_file:
        with zipfile.ZipFile(BytesIO(online_file.content)) as extract_file:
            extract_file.extractall(extract_path)
        time.sleep(10)      #give the website a breather especially when you are downloading many zip files

    #uncomment this section if you want to write the data into a text file
    # link_tuple = (county_name, full_link)  
    # links_list.append(link_tuple)   #add the tuple to the list
    # req = requests.get(full_link, headers=headers)      
    # folder = os.path.join('form34A_zipfiles', county_name)     
    # with open(folder, 'wb', encoding='utf-8') as saved_file:  
    #    saved_file.write(req.content)

#remember to close the driver object once you are done
browser.close()
