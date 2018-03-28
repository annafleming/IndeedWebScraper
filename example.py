from web_scraper import WebScraper
from indeed_scraper import IndeedScraper
from csv_saver import CsvSaver

scraper = WebScraper(IndeedScraper, CsvSaver('indeedLA.csv'), {'job_title':'data scientist',
                                     'location': 'Los Angeles, CA',
                                     'max_count': 2000,
                                     'save_links': True })
scraper.scrape()
