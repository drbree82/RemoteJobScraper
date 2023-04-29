import logging
import requests
import json
import os
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from flask import Flask, make_response

app = Flask(__name__)

urls = [
    'https://www.flexjobs.com/jobs',
    'https://remote.co/remote-jobs',
    'https://workingnomads.co/jobs',
    'https://weworkremotely.com',
    'https://jobspresso.co/browsejobs',
    'https://www.virtualvocations.com/jobs',
    'https://www.freelancer.com/jobs',
    'https://www.skipthedrive.com/jobs',
    'https://www.peopleperhour.com/freelance-jobs',
    'https://www.guru.com/d/jobs'
]

logging.basicConfig(filename='app.log', level=logging.DEBUG)


def scrape_flexjobs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_listings = []
    job_elems = soup.select('div.job.row.result')
    for job_elem in job_elems:
        job_title_elem = job_elem.select_one('div.col-md-5 > h5 > a')
        job_title = job_title_elem.get_text(strip=True)
        job_url = f"https://www.flexjobs.com{job_title_elem['href']}"

        company_elem = job_elem.select_one('div.col-md-3 > span > a')
        company = company_elem.get_text(strip=True)

        date_elem = job_elem.select_one('div.col-md-2 > span')
        date = date_elem.get_text(strip=True)

        job_listings.append({
            'title': job_title,
            'company': company,
            'date': date,
            'url': job_url
        })

    return job_listings


def scrape_remote_co(url):
    logging.info("Scraping remote.co")
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        jobs_container = soup.find("section", class_="jobs")

        if jobs_container is None:
            logging.error("Jobs container not found on remote.co")
            return []

        job_listings = jobs_container.find_all("div", class_="card")

        # rest of the code

    else:
        logging.error(f"Failed to fetch the remote.co webpage. Status code: {response.status_code}")
        return []


def scrape_working_nomads(url):
    logging.info("Scraping workingnomads.co")
    job_listings = []

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings_section = soup.find("section", class_="jobs")
        job_listings = job_listings_section.find_all("li")

        for job in job_listings:
            title = job.find("h2", class_="title").text.strip()
            company = job.find("span", class_="company").text.strip()
            job_link = job.find("a", class_="job-link")["href"]

            print(f"Job Title: {title}")
            print(f"Company: {company}")
            print(f"Job Link: https://workingnomads.co{job_link}\n")
    else:
           print("Failed to fetch the webpage. Status code:", response.status_code)

# You can continue adding scraping functions for the other URLs in the list.
# Remember to call them in the main function and aggregate the results.

def main():
    flexjobs_listings = scrape_flexjobs(urls[0])
    remote_co_listings = scrape_remote_co(urls[1])
    working_nomads_listings = scrape_working_nomads(urls[2])

    all_job_listings = flexjobs_listings + remote_co_listings + working_nomads_listings

    fg = FeedGenerator()
    fg.title("Remote Job Listings")
    fg.description("Aggregated remote job listings from various websites.")
    fg.link(href="http://localhost:5000/rss")

    for job in all_job_listings:
        fe = fg.add_entry()
        fe.title(job['title'])
        fe.link(href=job['url'])
        fe.description(f"Company: {job['company']} | Date: {job['date']}")

    rssfeed = fg.rss_str(pretty=True)

    with open("remote_job_listings.xml", "wb") as f:
        f.write(rssfeed)

    return rssfeed

@app.route('/rss')
def rss():
    try:
        rssfeed = main()
    except Exception as e:
        logging.exception("Error occurred while generating RSS feed:")
        return f"An error occurred: {str(e)}", 500

    response = make_response(rssfeed)
    response.headers.set("Content-Type", "application/rss+xml")
    return response

if __name__ == '__main__':
    app.run()
