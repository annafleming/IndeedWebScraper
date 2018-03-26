import requests, re
from bs4 import BeautifulSoup
import urllib

class IndeedScraper:
    URL = 'https://www.indeed.com'
    JOB_PATH = 'jobs'
    COLUMN_NAMES = ['job_title', 'company_name', 'job_contents', 'location', 'link']
    MAX_BATCH_SIZE = 100

    def __init__(self, params, saver):
        self._job_title = params['job_title']
        self._location = params['location']
        self._max_count = params['max_count']
        self._saver = saver
        self._results = []

    def scrape_all(self):
        links = self._get_position_links()
        jobs = []
        if len(links) > 0:
            self._saver.create_file(self.COLUMN_NAMES)
            for link in links:
                jobs.append(self._parse_job_listing_page(link))
                if len(jobs) >= self.MAX_BATCH_SIZE:
                    self._saver.save_batch(jobs)
                    jobs = []
            if len(jobs):
                self._saver.save_batch(jobs)

        return 'SUCCESS'

    def _get_position_links(self):
        links = []
        page_url = self._form_initial_url()
        page_object = self._get_page_object(page_url)

        while len(links) < self._max_count:
            links = links + self._parse_position_links(page_object)
            page_url = self._parse_next_page_link(page_object)
            if page_url is None:
                break
            page_object = self._get_page_object(page_url)

        if len(links) > self._max_count:
            links = links[:self._max_count]
        return links

    def _get_page_object(self, url):
        return BeautifulSoup(requests.get(url).text,'html.parser')

    def _parse_position_links(self, page):
        links = []
        for header in page.find_all("h2",class_="jobtitle"):
            links.append(header.a.get('href'))
        return links

    def _parse_next_page_link(self, page):
        last_page_element = page.find("div",class_="pagination").contents[-1]
        if last_page_element.name == 'a':
            return self.URL + last_page_element.get('href')
        return None

    def _form_initial_url(self):
        request_params = {'q': self._job_title, 'l': self._location}
        return self.URL + '/' + self.JOB_PATH + '?'+ urllib.parse.urlencode(request_params)

    def _parse_job_listing_page(self, link):
        page_container = self._get_page_object(self.URL + link)
        job_container = page_container.find(id="job-content")

        job_title = job_container.find(class_='jobtitle').get_text()
        company_name = job_container.find(class_='company').get_text()
        job_contents = str(job_container.find(id='job_summary'))
        location = page_container.find(id='where').attrs['value']

        return dict(zip(self.COLUMN_NAMES, [job_title, company_name, job_contents, location, link]))
