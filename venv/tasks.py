from celery import Celery
import scrape.linkedin_scraper as scrape
import database as db
from cvReader.pdfReader import cvReader
import os
import sys
app = Celery('tasks',
             broker='amqp://admin:pass@localhost:5672/myvhost')


@app.task()
def runLinkedinScraper():
    print("Logging in")
    scrape.login()
    anstalldaSearch = [
        "https://www.linkedin.com/search/results/people/?currentCompany=%5B%2218358%22%2C%2286140890%22%5D&origin=FACETED_SEARCH&sid=mkZ"]
    profile_url_list = []
    print("fetching profile urls")
    for url in anstalldaSearch:
        temp_profile_list = scrape.get_people_from_company_search(url, profile_url_list)
        profile_url_list.extend(temp_profile_list)
    print("fetching profile info")
    profiles = scrape.get_profile_info(profile_url_list)
    scrape.shutdown()
    print("posting to database")

    db.add_consultants_to_db(profiles)
    return  {'status': 'Task completed!'}


#need to configure cvreader for use with celery
@app.task()
def runcvReader():
    print(os.getcwd)
    cvReader()
    return {'status':'Task completed!'}


def checkWorker():
    i = app.control.inspect()
    return i.active()