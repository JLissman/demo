from flask import Blueprint
from login_app import login_is_required
import scrape.linkedin_scraper as scrape

import app

linkedin_scrape = Blueprint('linkedin_scrape', __name__, template_folder='templates')


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)



@celery
@login_is_required
def scrapeLinkedin():
    scrape.scrapeAndSave()