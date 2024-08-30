from scraper import PoliceScraper
from models import PoliceReport, Session
import logging

logging.basicConfig(level=logging.INFO)

class PoliceReportController:
    def __init__(self, session: Session):
        self.session = session
        self.scraper = PoliceScraper(self.session)

    def run_scraper(self):
        logging.info("Starting scraper")
        self.scraper.scrape_reports()
        logging.info("Scraping completed")

    def get_all_reports(self):
        logging.info("Fetching all reports")
        return self.session.query(PoliceReport).all()

    def get_report_by_id(self, report_id: int):
        logging.info(f"Fetching report with id: {report_id}")
        return self.session.get(PoliceReport, report_id)