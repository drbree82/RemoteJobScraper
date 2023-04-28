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

if __name__ == '__main__':
    app.run(debug=True)
