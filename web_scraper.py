class WebScraper:
    def __init__(self, scraper, saver, params):
        self._scraper = scraper(params, saver)

    def scrape(self):
        self._results = self._scraper.scrape_all()
        return self._results
