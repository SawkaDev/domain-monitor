from flask_apscheduler import APScheduler
from app.services.whois_service import WhoisService
from app.models.whois import Domain
import logging
import concurrent.futures

scheduler = APScheduler()

def update_whois_for_domain(app, domain):
    with app.app_context():
        try:
            WhoisService.update_whois_record(domain.name)
            app.logger.info(f"Updated WHOIS record for {domain.name}")
        except Exception as e:
            app.logger.error(f"Error updating WHOIS record for {domain.name}: {str(e)}")

def init_scheduler(app):
    scheduler.init_app(app)
    logging.getLogger('apscheduler').setLevel(logging.WARNING)
    scheduler.start()

    @scheduler.task('interval', id='update_whois_records', hours=24, misfire_grace_time=3600)
    def scheduled_update_whois_records():
        with app.app_context():
            domains = Domain.query.all()
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(update_whois_for_domain, app, domain) for domain in domains]
            concurrent.futures.wait(futures)

