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
     # Send a request to the URL and get the content
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the job listings container
        jobs_container = soup.find("section", class_="jobs")
        
        # Find all job listings
        job_listings = jobs_container.find_all("div", class_="card")
        
        # Iterate through the job listings and extract information
        for job in job_listings:
            # Find the job title
            title = job.find("h2", class_="font-weight-bold").text.strip()
            
            # Find the company name
            company = job.find("span", class_="text-secondary").text.strip()
            
            # Find the job link
            job_link = job.find("a", class_="card")["href"]
            
            # Print the extracted information
            print(f"Job Title: {title}")
            print(f"Company: {company}")
            print(f"Job Link: https://remote.co{job_link}\n")
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)

    pass

def scrape_working_nomads(url):
    # Send a request to the URL and get the content
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the job listings container
        jobs_container = soup.find("div", class_="jobs-container")
        
        # Find all job listings
        job_listings = jobs_container.find_all("div", class_="job")
        
        # Iterate through the job listings and extract information
        for job in job_listings:
            # Find the job title
            title = job.find("h2", class_="title").text.strip()
            
            # Find the job category
            category = job.find("div", class_="meta").find("span", class_="category").text.strip()
            
            # Find the job link
            job_link = job.find("a", class_="job-link")["href"]
            
            # Print the extracted information
            print(f"Job Title: {title}")
            print(f"Category: {category}")
            print(f"Job Link: {job_link}\n")
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)

    pass

def scrape_weworkremotely(url):
      # Send a request to the URL and get the content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the job listings container
        jobs_container = soup.find("div", class_="jobs-container")

        # Find all job listings
        job_listings = jobs_container.find_all("div", class_="feature")

        # Iterate through the job listings and extract information
        for job in job_listings:
            # Find the job title
            title = job.find("span", class_="title").text.strip()

            # Find the company name
            company = job.find("span", class_="company").text.strip()

            # Find the job link
            job_link = job.find("a", class_="feature")["href"]

            # Print the extracted information
            print(f"Job Title: {title}")
            print(f"Company: {company}")
            print(f"Job Link: https://weworkremotely.com{job_link}\n")
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)
    pass

def scrape_jobspresso(url):
    def scrape_jobspresso(url):
        # Send a request to the URL and get the content
    response = requests.get(url)

        # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the job listings container
        jobs_container = soup.find("div", class_="job_listings")

        # Find all job listings
        job_listings = jobs_container.find_all("li", class_="job_listing")

        # Iterate through the job listings and extract information
        for job in job_listings:
            # Find the job title
            title = job.find("h3", class_="job_listing-title").text.strip()

            # Find the company name
            company = job.find("div", class_="job_listing-company").text.strip()

            # Find the job link
            job_link = job.find("a", class_="job_listing-clickbox")["href"]

            # Print the extracted information
            print(f"Job Title: {title}")
            print(f"Company: {company}")
            print(f"Job Link: {job_link}\n")
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)

    pass

def scrape_virtualvocations(url):
def scrape_virtualvocations(url):
    # Send a request to the URL and get the content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the job listings container
        jobs_container = soup.find("div", class_="lrv-a-grid")

        # Find all job listings
        job_listings = jobs_container.find_all("div", class_="lrv-a-grid-item")

        # Iterate through the job listings and extract information
        for job in job_listings:
            # Find the job title
            title = job.find("h2", class_="entry-title").text.strip()

            # Find the company name
            company = job.find("span", class_="entry-company").text.strip()

            # Find the job link
            job_link = job.find("a", class_="entry-title__link")["href"]

            # Print the extracted information
            print(f"Job Title: {title}")
            print(f"Company: {company}")
            print(f"Job Link: {job_link}\n")
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)
    pass

def scrape_freelancer(url):
    def scrape_freelancer(url):
    # Send a request to the URL and get the content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the job listings container
        jobs_container = soup.find("div", class_="JobSearchCard-list")

        # Find all job listings
        job_listings = jobs_container.find_all("div", class_="JobSearchCard-item")

        # Iterate through the job listings and extract information
        for job in job_listings:
            # Find the job title
            title = job.find("h2", class_="JobSearchCard-primary-heading").text.strip()

            # Find the job link
            job_link = job.find("a", class_="JobSearchCard-primary-heading-link")["href"]

            # Find the job budget
            budget = job.find("div", class_="JobSearchCard-secondary-price").text.strip()

            # Print the extracted information
            print(f"Job Title: {title}")
            print(f"Job Link: https://www.freelancer.com{job_link}")
            print(f"Budget: {budget}\n")
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)

    pass

def scrape_skipthedrive(url):
    # Send a request to the URL and get the content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the job listings container
        jobs_container = soup.find("div", class_="listify_widget")

        # Find all job listings
        job_listings = jobs_container.find_all("article", class_="job_listing")

        # Iterate through the job listings and extract information
        for job in job_listings:
            # Find the job title
            title = job.find("h3", class_="job_listing-title").text.strip()

            # Find the company name
            company = job.find("div", class_="job_listing-company").text.strip()

            # Find the job link
            job_link = job.find("a", class_="job_listing-clickbox")["href"]

            # Print the extracted information
            print(f"Job Title: {title}")
            print(f"Company: {company}")
            print(f"Job Link: {job_link}\n")
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)
    pass

def scrape_peopleperhour(url):
      # Send a request to the URL and get the content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the job listings container
        jobs_container = soup.find("ul", class_="clearfix")

        # Find all job listings
        job_listings = jobs_container.find_all("li", class_="clearfix")

        # Iterate through the job listings and extract information
        for job in job_listings:
            # Find the job title
            title = job.find("h2", class_="clearfix").text.strip()

            # Find the job link
            job_link = job.find("a", class_="clearfix")["href"]

            # Find the job budget
            budget = job.find("span", class_="pull-right").text.strip()

            # Print the extracted information
            print(f"Job Title: {title}")
            print(f"Job Link: https://www.peopleperhour.com{job_link}")
            print(f"Budget: {budget}\n")
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)
    pass

def scrape_guru(url):
    def scrape_guru(url):
    # Send a request to the URL and get the content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the job listings container
        jobs_container = soup.find("section", class_="job-list")

        # Find all job listings
        job_listings = jobs_container.find_all("div", class_="job-list-item")

        # Iterate through the job listings and extract information
        for job in job_listings:
            # Find the job title
            title = job.find("h3", class_="job-title").text.strip()

            # Find the job link
            job_link = job.find("a", class_="job-title")["href"]

            # Find the job budget
            budget = job.find("span", class_="job-budget").text.strip()

            # Print the extracted information
            print(f"Job Title: {title}")
            print(f"Job Link: https://www.guru.com{job_link}")
            print(f"Budget: {budget}\n")
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)
    pass

def scrape_jobs():
    all_job_listings = []

    # Uncomment and replace each function with the correct scraping code for each website
    # Make sure to also import the necessary libraries for each function

    # Example: Scrape FlexJobs
    job_listings = scrape_flexjobs(urls[0])
    all_job_listings.extend(job_listings)

    return all_job_listings

def read_previous_jobs(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return []

def write_new_jobs(file_path, new_jobs):
    with open(file_path, 'w') as file:
        json.dump(new_jobs, file)

def generate_rss

def generate_rss_feed(job_listings):
    fg = FeedGenerator()
    fg.title('Latest Remote Jobs')
    fg.description('A feed of the latest remote job listings from various websites')
    fg.link(href='https://example.com', rel='alternate')

    for job in job_listings:
        fe = fg.add_entry()
        fe.title(job['title'])
        fe.description(f"Company: {job['company']}<br>Date: {job['date']}")
        fe.link(href=job['url'])

    return fg.rss_str(pretty=True)

@app.route('/rss')
def rss():
    all_job_listings = scrape_jobs()
    previous_jobs = read_previous_jobs('previous_jobs.json')

    new_jobs = [job for job in all_job_listings if job not in previous_jobs]
    write_new_jobs('previous_jobs.json', all_job_listings)

    rss_feed = generate_rss_feed(new_jobs)
    response = make_response(rss_feed)
    response.headers.set('Content-Type', 'application/rss+xml')

    return response

if __name__ == "__main__":
    app.run(port=5000)
