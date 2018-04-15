# IndeedWebScraper

Python application for scraping job postings from Indeed.com

## How to use it?

```
  scraper = WebScraper(IndeedScraper,
                       CsvSaver('indeedSF.csv'),
                       {'job_title':'data scientist',
                        'location': 'San Francisco, CA',
                        'max_count': 500,
                        'save_links': False })
  scraper.scrape()

```

* You have to define:
    * a name for the csv file
    * `job_title`
    * `location`
    * `max_count` - desired amount of records
    * `save_links`(True/ False) whether it should save the links of the scarped job postings in a separate csv file.
* Currently, it only has a capability to save results into a CSV file.

## Technical requirements

* Python 3.6.3
* bs4

## License

This project is licensed under the MIT License.
