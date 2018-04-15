from web_scraper import WebScraper
from indeed_scraper import IndeedScraper
from csv_saver import CsvSaver

scraper = WebScraper(IndeedScraper, CsvSaver('data_scientist.csv'), {'job_title':'',
                                     'location': '',
                                     'max_count': 50,
                                     'save_links': True,
                                     'advance_request': 'q=\"data+scientist\"&limit=50'})
scraper.scrape()
