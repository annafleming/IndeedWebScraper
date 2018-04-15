import requests, re
from bs4 import BeautifulSoup
import urllib
import time
from selenium import webdriver

class IndeedScraper:
    URL = 'https://www.indeed.com'
    JOB_PATH = 'jobs'
    COLUMN_NAMES = ['job_title', 'company_name', 'job_contents', 'location', 'link']
    MAX_BATCH_SIZE = 100

    def __init__(self, params, saver):
        self._job_title = params['job_title']
        self._location = params['location']
        self._max_count = params['max_count']
        self._save_links = params['save_links']
        self._advance_request = params['advance_request']
        self._saver = saver
        self._results = []
        self._driver = webdriver.PhantomJS()

    def scrape_all(self):
        links = self._get_position_links()
        if self._save_links:
            self._saver.save_links(links)
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
        self._driver.close()

        return 'SUCCESS'

    def _get_position_links(self):
        links = []
        page_url = self._get_initial_url()
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
        self._driver.get(url)
        return BeautifulSoup(self._driver.page_source,'html.parser')

    def _parse_position_links(self, page):
        links = []
        for header in page.find_all("h2",class_="jobtitle"):
            if header.a:
                links.append(header.a.get('href'))
        return links

    def _parse_next_page_link(self, page):
        last_page_element = page.find("div",class_="pagination").contents[-1]
        if last_page_element and last_page_element.name == 'a':
            return self.URL + last_page_element.get('href')
        return None

    def _get_initial_url(self):
        if self._advance_request != '':
            return self.URL + '/' + self.JOB_PATH + '?' + self._advance_request
        else:
            return self._form_initial_url()


    def _form_initial_url(self):
        request_params = {'q': self._job_title, 'l': self._location}
        return self.URL + '/' + self.JOB_PATH + '?'+ urllib.parse.urlencode(request_params)

    def _parse_job_listing_page(self, link):
        page_container = self._get_page_object(self.URL + link)
        job_container = page_container.find(id="job-content")

        job_title = company_name = job_contents = location = ''
        if job_container:
            job_title = self._get_element_text_by_class(job_container, 'jobtitle')
            company_name = self._get_element_text_by_class(job_container, 'company')
            job_contents = ''.join(map(str, job_container.find(id='job_summary').contents))
            location = self._get_input_value_by_id(page_container, 'where')
        return dict(zip(self.COLUMN_NAMES, [job_title, company_name, job_contents, location, link]))

    def _get_element_text_by_class(self, bs_object, classname):
        page_element = bs_object.find(class_=classname)
        if page_element:
            return page_element.get_text()
        return ''

    def _get_element_text_by_id(self, bs_object, element_id):
        page_element = bs_object.find(id=element_id)
        if page_element:
            return page_element.get_text()
        return ''

    def _get_input_value_by_id(self, bs_object, element_id):
        page_element = bs_object.find(id=element_id)
        if page_element:
            return page_element.attrs['value']
        return ''
