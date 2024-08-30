import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models import PoliceReport, Session
import logging

logging.basicConfig(level=logging.INFO)

class PoliceScraper:
    def __init__(self, session: Session):
        self.base_url = "https://www.berlin.de/polizei/polizeimeldungen/"
        self.session = session

    def scrape_reports(self):
        for page in range(1, 3):  # Scrape pages 1 and 2
            url = f"{self.base_url}?page_at_1_6={page}"
            logging.info(f"Scraping page: {url}")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Print the entire HTML content for debugging
            logging.info(f"HTML content:\n{soup.prettify()}")
            
            reports = soup.find_all('li', class_='list--tablelist')
            logging.info(f"Found {len(reports)} reports on page {page}")
            
            if len(reports) == 0:
                # If no reports found, let's check for other possible structures
                logging.info("Checking alternative structures...")
                reports = soup.find_all('ul', class_='list--tablelist')
                if len(reports) > 0:
                    reports = reports[0].find_all('li')
                logging.info(f"Found {len(reports)} reports using alternative structure")
            
            for report in reports:
                logging.info(f"Report HTML:\n{report.prettify()}")
                try:
                    date_div = report.find('div', class_='cell nowrap date')
                    title_div = report.find('div', class_='cell text')
                    
                    if date_div and title_div:
                        date_str = date_div.text.strip()
                        title = title_div.a.text.strip()
                        url = "https://www.berlin.de" + title_div.a['href']
                        location = title_div.find('span', class_='category').text.replace('Ereignisort:', '').strip()
                        
                        logging.info(f"Extracted data: Date: {date_str}, Title: {title}, URL: {url}, Location: {location}")
                        
                        # Parse date
                        date = datetime.strptime(date_str, "%d.%m.%Y %H:%M Uhr")
                        
                        # Check if report already exists
                        existing_report = self.session.query(PoliceReport).filter(PoliceReport.url == url).first()
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
                            logging.info(f"Added new report: {title}")
                        else:
                            logging.info(f"Report already exists: {title}")
                    else:
                        logging.warning(f"Skipping report due to missing data: date_div={bool(date_div)}, title_div={bool(title_div)}")
                except Exception as e:
                    logging.error(f"Error processing report: {e}")
            
            self.session.commit()

    def fetch_full_content(self, url):
        logging.info(f"Fetching full content from: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('div', class_='textile')
        if content_div:
            content = content_div.text.strip()
        else:
            logging.warning("Content div not found. Setting content to 'Content not available'.")
            content = "Content not available"
        return content