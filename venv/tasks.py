from celery import Celery
import scrape.linkedin_scraper as scrape
import database as db
from cvReader.pdfReader import cvReader
import os
import sys
app = Celery('tasks',backend='rpc://', broker='amqp://admin:pass@localhost:5672/myvhost')


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

@app.task()
def getLinkedinProfile(profile_url):
    print("Scraping profile:"+profile_url)
    scrape.login()
    profile = scrape.get_profile_info(profile_url)
    scrape.shutdown()
    db.add_consult(profile)
    return{'status':'Profile imported'}

def checkWorker():
    i = app.control.inspect()
    return i.active()



def getWorkerStatus():
    i = app.control.inspect()
    status = {}
    status["active"] = i.active()
    status["scheduled"] = i.scheduled()
    status["qued"] = i.reserved()

    return status


def get_celery_worker_status():
    i = app.control.inspect()
    availability = i.ping()
    stats = i.stats()
    registered_tasks = i.registered()
    active_tasks = i.active()
    scheduled_tasks = i.scheduled()
    result = {
        'availability': availability,
        'stats': stats,
        'registered_tasks': registered_tasks,
        'active_tasks': active_tasks,
        'scheduled_tasks': scheduled_tasks
    }
    return result


def startWorker():
    print("starting worker")
    #app.worker_main(argv=['worker', '--loglevel=info', "-n", "linkedin",'--without-gossip'])
    startCommand = "celery -A tasks worker -l info -P gevent -n linkedin"
    os.system('start cmd /c '+startCommand)

def killAllWorkers():
    #app.worker_main(argv=['-A', 'taks', 'control', 'shutdown'])
    os.system('cmd /c "celery -A tasks control shutdown"')