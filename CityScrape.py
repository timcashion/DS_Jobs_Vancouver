
### Setup
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import random
import re
from math import floor, ceil
from li_scrape_fx import get_links


#1. get list of urls you want to search from

search_pages_cities = ["https://www.linkedin.com/jobs/search/?keywords=data%20scientist&location=Vancouver%2C%20British%20Columbia%2C%20Canada&trk=guest_job_search_jobs-search-bar_search-submit&sortBy=DD",
"https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=San%20Francisco%20Bay%20Area&trk=guest_job_search_jobs-search-bar_search-submit&sortBy=DD",
"https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=San%20Jose%2C%20California%2C%20United%20States&trk=guest_job_search_jobs-search-bar_search-submit&sortBy=DD",
"https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=New%20York%2C%20New%20York%2C%20United%20States&trk=guest_job_search_jobs-search-bar_search-submit&sortBy=DD", 
"https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Toronto%2C%20Ontario%2C%20Canada&trk=guest_job_search_jobs-search-bar_search-submit&sortBy=DD",
"https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Montreal%2C%20Quebec%2C%20Canada&trk=guest_job_search_jobs-search-bar_search-submit&sortBy=DD",
"https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Seattle%2C%20Washington%2C%20United%20States&trk=guest_job_search_jobs-search-bar_search-submit&sortBy=DD",
"https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Washington%20DC-Baltimore%20Area&trk=guest_job_search_jobs-search-bar_search-submit&sortBy=DD",
"https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Boston%2C%20Massachusetts%2C%20United%20States&trk=guest_job_search_jobs-search-bar_search-submit&sortBy=DD",
"https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Raleigh-Durham-Chapel%20Hill%20Area&trk=guest_job_search_jobs-search-bar_search-submit&sortBy=DD"]


#search_pages_countries = ["https://ca.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Canada&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&sortBy=DD",
#"https://ca.linkedin.com/jobs/search?keywords=Data%20Scientist&location=United%20States&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&sortBy=DD"]

#2. get each job posting within these searches
#Choose between either country-based or city-based search
#search_pages = search_pages_countries[0]
search_pages = search_pages_cities

all_job_urls = []
for search_page in search_pages:
    job_urls = get_links(search_page, driver="/Users/timcashion/chromedriver")
    all_job_urls.append(job_urls)

flat_all_jobs = [item for sublist in all_job_urls for item in sublist]
flat_all_jobs = {"urls":flat_all_jobs}
flat_jobs_output = pd.DataFrame(flat_all_jobs)
flat_jobs_output.to_csv("get_links_output.csv", index=False)
#len(flat_all_jobs) #Check length of links obtained. 
