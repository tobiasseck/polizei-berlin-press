import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models import PoliceReport, Session

class PoliceScraper:
    def __init__(self, session: Session):
        self.base_url = "https://www.berlin.de/polizei/polizeimeldungen/"
        self.session = session

    def scrape_reports(self):
        for page in range(1, 3):  # Scrape pages 1 and 2
            url = f"{self.base_url}?page_at_1_6={page}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            reports = soup.find_all('li', class_='list--tablelist')
            
            for report in reports:
                date_str = report.find('div', class_='cell nowrap date').text.strip()
                title = report.find('div', class_='cell text').a.text.strip()
                url = "https://www.berlin.de" + report.find('div', class_='cell text').a['href']
                location = report.find('span', class_='category').text.replace('Ereignisort:', '').strip()
                
                # Parse date
                date = datetime.strptime(date_str, "%d.%m.%Y %H:%M Uhr")
                
                # Check if report already exists
                existing_report = self.session.get(PoliceReport, url=url)
                if not existing_report:
                    # Fetch full content
                    full_content = self.fetch_full_content(url)
                    
                    # Create new report
                    new_report = PoliceReport(
                        date=date,
                        title=title,
                        content=full_content,
                        location=location,
                        url=url
                    )
                    self.session.add(new_report)
            
            self.session.commit()

    def fetch_full_content(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find('div', class_='textile').text.strip()
        return content