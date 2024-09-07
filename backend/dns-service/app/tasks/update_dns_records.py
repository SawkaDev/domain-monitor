from flask_apscheduler import APScheduler
from app.services.dns_service import DNSService
import logging

scheduler = APScheduler()

# Assuming you have a list of domains to monitor
domains_to_monitor = ['google.com']

def init_scheduler(app):
    scheduler.init_app(app)
    logging.getLogger('apscheduler').setLevel(logging.WARNING)
    scheduler.start()

    @scheduler.task('interval', id='update_dns_records', minutes=10, misfire_grace_time=900)
    def scheduled_update_dns_records():
        with app.app_context():
            for domain in domains_to_monitor:
                try:
                    DNSService.update_dns_records(domain)
                    app.logger.info(f"Updated DNS records for {domain}")
                except Exception as e:
                    app.logger.error(f"Error updating DNS records for {domain}: {str(e)}")
