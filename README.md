## Remote Job Scraper

This Python script scrapes remote job listings from various websites and generates an RSS feed containing the aggregated results. The script uses the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library for web scraping and the [feedgen](https://github.com/lkiesow/python-feedgen) library for generating the RSS feed.

### Prerequisites

* Python 3.x
* pip package manager

### Installation

1. Clone the repository.
2. Install the required dependencies by running 

pip install beautifulsoup4

pip install flask

pip install feedgen

### Usage

1. Run the script using `python main.py`.
2. The script will scrape job listings from various websites and generate an RSS feed in the `remote_job_listings.xml` file.
3. The RSS feed can be accessed by navigating to `http://localhost:5000/rss` in a web browser.

### Supported Websites

* https://www.flexjobs.com/jobs
* https://remote.co/remote-jobs
* https://workingnomads.co/jobs
* https://weworkremotely.com
* https://jobspresso.co/browsejobs
* https://www.virtualvocations.com/jobs
* https://www.freelancer.com/jobs
* https://www.skipthedrive.com/jobs
* https://www.peopleperhour.com/freelance-jobs
* https://www.guru.com/d/jobs

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
