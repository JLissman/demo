import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

#auto update chromedriver
chromedriver_autoinstaller.install()
driver=webdriver.Chrome()

def debug():
    login()
    #anstalldaSearch = ["https://www.linkedin.com/search/results/people/?currentCompany=%5B%2218358%22%5D","https://www.linkedin.com/search/results/people/?currentCompany=%5B%2286140890%22%5D" ]
    anstalldaSearch = ["https://www.linkedin.com/search/results/people/?currentCompany=%5B%2218358%22%2C%2286140890%22%5D&origin=FACETED_SEARCH&sid=mkZ"]
    profile_url_list = []
    for url in anstalldaSearch:
        temp_profile_list = get_people_from_company_search(url, profile_url_list)
        profile_url_list.extend(temp_profile_list) #add lists together

    for link in profile_url_list:
        if profile_url_list.count(link) > 1:
            print(link+" already in list")
    print(len(profile_url_list))

def login():
    user = "facehump90@gmail.com"
    password = "Sportlife123"
    driver.get('https://www.linkedin.com/login/')
    driver.find_element('xpath','//*[@id="username"]').send_keys(user)#send in username to username field
    driver.find_element('xpath','//*[@id="password"]').send_keys(password)#send in password to password field
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'))).click()#click log in
    try:
        driver.find_element('xpath','//*[@id="ember455"]/button').click()#click skip phonenumber
    except:
        pass


def get_people_from_company_search(url, current_list):
    driver.get(url)
    results = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div/h2'))).get_attribute('innerText') #get text of number of results
    results = results.replace(" resultat","") #remove text element
    results = int(results) #convert to int so we can round the number
    pages_max = int (round(results + 5.1,-1) / 10) #round up to nearest 10 and then divide by 10 to get total number of pages
    print("max pages "+str(pages_max))
    current_page = 1
    profile_url_list = []
    while current_page <= pages_max:
        page_suffix = "&page=" + str(current_page)
        driver.get(url + page_suffix)
        current_page += 1
        print("current page is "+str(driver.current_url))
        searchResults = driver.find_element('xpath','//*[@id="main"]/div/div').get_attribute('innerHTML') #get search results container
        soup = BeautifulSoup(searchResults, "html.parser")#load bs4 with all search results
        profileElement = soup.find_all("a", {"class": "app-aware-link scale-down"}) #get all profile link elements
        for a in profileElement:
            link = a['href']
            if link not in profile_url_list and "/in/" in link and link not in current_list:
                profile_url_list.append(link)




    return profile_url_list


def get_profile_info(list):
    for profile_url in list:
        driver.get(list)
        full_name = driver.get_element('xpath','//*[@id="ember130"]/div[2]/div[2]/div[1]/div[1]/h1').get_attribute('innerText')
        split_name = full_name.split(" ",1)
        first_name = split_name[0]
        last_name = split_name[1]
        title = driver.get_element('xpath', '//*[@id="ember130"]/div[2]/div[2]/div[1]/div[2]').get_attribute('innerText').split(" at")
        title = title[0]
        location = driver.get_element('xpath', '//*[@id="ember130"]/div[2]/div[2]/div[2]/span[1]').get_attribute('innerText')
        description = driver.get_element('xpath', '//*[@id="ember144"]/div[3]/div/div/div/span[1]').get_attribute('innerText')
        #go to competence page
        competence_page = driver.current_url+"/details/skills/"
        driver.get(competence_page)





def scroll_to_bottom():#scrolls to bottom of page for auto-updating results
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


if __name__ == '__main__':
    debug()
