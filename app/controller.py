from scraper import PoliceScraper
from models import PoliceReport, Session

class PoliceReportController:
    def __init__(self, session: Session):
        self.session = session
        self.scraper = PoliceScraper(self.session)

    def run_scraper(self):
        self.scraper.scrape_reports()

    def get_all_reports(self):
        return self.session.query(PoliceReport).all()

    def get_report_by_id(self, report_id: int):
        return self.session.get(PoliceReport, report_id)