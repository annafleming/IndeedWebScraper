# IndeedWebScraper

Python application for scraping job postings from Indeed.com

## How to use it?

### Specifying search parameter independently

```
  scraper = WebScraper(IndeedScraper,
                       CsvSaver('indeedSF.csv'),
                       {'job_title':'data scientist',
                        'location': 'San Francisco, CA',
                        'max_count': 500,
                        'save_links': False })
  scraper.scrape()

```

* Required parameters:
    * `job_title`
    * `location`

* Optional parameters:
    * a name for the csv file
    * `max_count` - desired amount of records
    * `save_links`(True/ False) whether it should save the links of the scarped job postings in a separate csv file.

### Utilizing advance search
```
  scraper = WebScraper(IndeedScraper,
                       CsvSaver('indeedSF.csv'),
                       {'max_count': 500,
                        'save_links': False,
                        'advance_request': 'q=\"data+scientist\"&limit=50' })
  scraper.scrape()

```

* Required parameters:
    * `advance_request`

* Optional parameters:
    * a name for the csv file
    * `max_count` - desired amount of records
    * `save_links`(True/ False) whether it should save the links of the scarped job postings in a separate csv file.

## Technical requirements

* Python 3.6.3
* bs4
* selenium.webdriver
* PhantomJS

## License

This project is licensed under the MIT License.
