from flask_apscheduler import APScheduler
from app.services.dns_service import DNSService
from app.models.dns_entry import Domain
import logging
import concurrent.futures

scheduler = APScheduler()

def update_dns_for_domain(app, domain):
    with app.app_context():
        try:
            DNSService.update_dns_records(domain.name)
            app.logger.info(f"Updated DNS records for {domain.name}")
        except Exception as e:
            app.logger.error(f"Error updating DNS records for {domain.name}: {str(e)}")

def init_scheduler(app):
    scheduler.init_app(app)
    logging.getLogger('apscheduler').setLevel(logging.WARNING)
    scheduler.start()

    @scheduler.task('interval', id='update_dns_records', minutes=30, misfire_grace_time=900)
    def scheduled_update_dns_records():
        with app.app_context():
            domains = Domain.query.all()
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(update_dns_for_domain, app, domain) for domain in domains]
            concurrent.futures.wait(futures)

