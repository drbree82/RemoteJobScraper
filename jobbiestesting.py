import logging
import requests
import json
import os
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from flask import Flask, make_response

app = Flask(__name__)

urls = [    'https://www.flexjobs.com/jobs',    'https://remote.co/remote-jobs',    'https://workingnomads.co/jobs',    'https://weworkremotely.com',    'https://jobspresso.co/browsejobs',    'https://www.virtualvocations.com/jobs',    'https://www.freelancer.com/jobs',    'https://www.skipthedrive.com/jobs',    'https://www.peopleperhour.com/freelance-jobs',    'https://www.guru.com/d/jobs']

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

        for job in job_listings:
            job_title = job.find("h2", class_="card-title").text.strip()
            job_url = job.find("a", class_="card-link")["href"]
            company = job.find("h3", class_="card-subtitle").text.strip()
            date = job.find("div", class_="job-date").text.strip()

            job_listings.append({
                'title': job_title,
                'company': company,
                'date': date,
                'url': job_url
            })
    else:
        logging.error(f"Failed to fetch the remote.co webpage. Status code: {response.status_code}")
        return []

    return job_listings


def scrape_working_nomads(url):
    logging.info("Scraping workingnomads.co")
    job_listings = []

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings_section = soup.find("section", class_="jobs")
        if job_listings_section is None:
            logging.error("Job listings section not found on workingnomads.co")
            return []
        job_listings = job_listings_section.find_all("li")

        for job in job_listings:
            title = job.find("h2", class_="title").text.strip()
            company = job.find("span", class_="company").text.strip()
            job_link = job.find("a", class_="job-link")
            if job_link:
                job_url = "https://workingnomads.co" + job_link["href"]
            else:
                job_url = ""
            job_date = job.find("span", class_="date").text.strip()

            job_listings.append({
                'title': title,
                'company': company,
                'date': job_date,
                'url': job_url
            })
    else:
        logging.error(f"Failed to fetch the workingnomads.co webpage. Status code: {response.status_code}")
        return []

    return job_listings



# You can continue adding scraping functions for the other URLs in the list.
# Remember to call them in the main function and aggregate the results.

def main():
    job_listings = []
    for url in urls:
        if 'flexjobs' in url:
            job_listings += scrape_flexjobs(url)
        elif 'remote.co' in url:
            job_listings += scrape_remote_co(url)
        elif 'workingnomads.co' in url:
            job_listings += scrape_working_nomads(url)
        # Add more elif blocks for the other websites

    job_listings = [j for j in job_listings if j is not None]
    if len(job_listings) == 0:
        logging.warning("No job listings found.")
        return ""

    fg = FeedGenerator()
    fg.title("Remote Job Listings")
    fg.description("Aggregated remote job listings from various websites.")
    fg.link(href="http://localhost:5000/rss")

    for job in job_listings:
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
