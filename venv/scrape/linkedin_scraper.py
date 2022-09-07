import csv
#import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import database as db

#auto update chromedriver


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
    get_profile_info(profile_url_list)

def login():
    global driver
    options = Options()
    options.add_argument("--enable-javascript")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    user = "fac"
    password = "Sportlife123"
    driver.get('https://www.linkedin.com/login/')
    if "signup" not in driver.current_url:
        driver.find_element('xpath','//*[@id="username"]').send_keys(user)#send in username to username field
        driver.find_element('xpath','//*[@id="password"]').send_keys(password)#send in password to password field
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'))).click()#click log in
        try:
            driver.find_element('xpath','//*[@id="ember455"]/button').click()#click skip phonenumber
        except:
            pass
        print("logged on")
    else:
        print("Waiting 10 seconds and trying again")
        time.sleep(10)
        login()

def shutdown():
    driver.close()

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



    print("profule_url_list before return "+(str(len(profile_url_list))))
    return profile_url_list


def get_profile_info(list):
    profile_list = []
    print("getprofileinfo length")
    print(len(list))
    for profile_url in list:
        print("Working on "+str(list.index(profile_url))+" of "+str(len(list)))
        driver.get(profile_url)
        full_name = driver.find_element('xpath','//h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]').get_attribute('innerText')
        split_name = full_name.split(" ",1)
        first_name = split_name[0]
        last_name = split_name[1:]
        img_url = driver.find_element('xpath','//img[contains(@title, "'+first_name+'")]').get_attribute('src')
        if "data:image" in img_url:
            img_url = "https://microbiology.ucr.edu/sites/default/files/styles/form_preview/public/blank-profile-pic.png?itok=4teBBoet"
        title = driver.find_element('xpath', '//div[@class="text-body-medium break-words"]').get_attribute('innerText').split(" at")
        title = title[0].replace("adesso sweden","").replace("purple scout","").replace(" på ","").replace("Adesso","").replace("Sweden","").replace("'","")
        location = driver.find_element('xpath', '//span[@class="text-body-small inline t-black--light break-words"]').get_attribute('innerText')
        try:
            description = driver.find_element('xpath', '//div[contains(@class, "inline-show-more-text")]/span[@class="visually-hidden"]').get_attribute('innerText')
        except:
            description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam id tellus a justo congue accumsan. Nulla et iaculis magna, at facilisis dolor. Nullam vel mauris sollicitudin, commodo dolor luctus, vehicula lorem. Maecenas justo tellus, lacinia non ante quis, bibendum bibendum ante. Mauris at commodo lectus. Maecenas pellentesque turpis mi, vel feugiat libero scelerisque at. Pellentesque sodales ligula quis ante condimentum, eu suscipit turpis hendrerit. Donec porttitor cursus lectus id vestibulum. Vivamus sed aliquet sem. Nulla metus ligula, condimentum eget tortor quis, auctor sagittis enim. Cras libero urna, tincidunt ut vehicula ac, semper nec enim. Mauris lectus tellus, posuere sit amet tellus a, suscipit hendrerit lectus."
        #go to competence page
        description = description.replace("'","")
        competence_page = driver.current_url+"/details/skills/"
        driver.get(competence_page)
        time.sleep(2)
        try:
            driver.find_element('xpath','//*[@id="ember89"]').click()#expand results if possible
        except:
            pass
        scroll_to_bottom()
        ulElements = driver.find_elements('xpath', '//ul[@class="pvs-list "][@tabindex="-1"]/li[@class="pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated "]')
        competence_list = []
        for ul in ulElements:
            competence_name_unsplit = ul.get_attribute('innerText')
            competence_name = competence_name_unsplit.split('\n')
            competence_list.append(competence_name[0])

        competence_list[:] = [x for x in competence_list if x]


        profile_list.append((first_name, last_name, title, img_url, location, description, competence_list))

    return profile_list


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


def scrapeAndSave():
    login()
    anstalldaSearch = ["https://www.linkedin.com/search/results/people/?currentCompany=%5B%2218358%22%2C%2286140890%22%5D&origin=FACETED_SEARCH&sid=mkZ"]
    profile_url_list = []
    for url in anstalldaSearch:
        temp_profile_list = get_people_from_company_search(url, profile_url_list)
        profile_url_list.extend(temp_profile_list)  # add lists together
    print("profile url length "+str(len(profile_url_list)))
    profiles = get_profile_info(profile_url_list)

    #save profiles to CSV instead so i dont have to run this script over each time during debugging
    try:
        with open('profiles.csv', 'w+', newline='') as profile_csv:
            fieldnames = ['firstname', 'lastname', 'role', 'image_url', 'location', 'description']
            profile_writer = csv.DictWriter(profile_csv, fieldnames=fieldnames)
            writer.writeheader()
            with open('tags.csv', 'w+', newline='') as tags_csv:
                tag_fieldnames ['tag','consult_id']
                tag_writer = csv.DictWriter(tags_csv, fieldnames=tag_fieldnames)
                for row in profiles:
                    writer.writerow({'firstname': row[1], 'lastname':row[2],'role':row[3],'image_url':row[4],'location':row[5],'description':row[6]})
                    for tagrow in profiles[-1]:
                        tag_writer.writerow({'tag':tagrow, 'consult_id':row[0]})
    except e:
        print(e)
        print("some error in writer")

    print("Number of profiles saved:"+str(len(profiles)))
    db.add_consultants_to_db(profiles)
    driver.close()
    return True

