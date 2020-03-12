
### Dependencies
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

def get_links(search_page: str, driver: str) -> list:
    """
    #Get all links for a certain job title search in a certain location

    Parameters
    ----------
    search_page: LinkedIn search page to search on
    driver: Path to ChromeDriver 

    Returns
    ----------
    list of all job links found to be search over. 

    """
    job_urls = []
    driver = Chrome(driver) #Replace with local path to chromedriver if not in PATH location
    driver.get(search_page)
    time.sleep(3+random.randint(10,100)/100)
    more_jobs_path = '/html/body/main/div/section/button'
    num_job_pages = driver.find_element_by_xpath("/html/body/main/div/section/div[1]/h1/span[1]").text
    num_job_pages = re.sub(",|\+", "", num_job_pages)
    num_job_pages = min(ceil(int(num_job_pages)/25), 40) #LinkedIn caps out the 'see more jobs' button at 1000 jobs (40 pages). 
    for i in range(1, num_job_pages): 
        time.sleep(3+random.randint(10,100)/100)
        print(i)
        try:
            element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, more_jobs_path)))
            jobs_button = driver.find_elements_by_xpath(more_jobs_path)[0]
            jobs_button.click()
        except:
            pass
    print("No more buttons to push")
    mydivs = driver.find_elements_by_class_name("result-card__full-card-link")
    for div in mydivs:
        job_url = div.get_attribute("href")
        job_urls.append(job_url)
    driver.close()
    return(job_urls)


def search_links(job_urls: list) -> list:
    """
    #Returns cleaned string of description result

    Parameters
    ----------
    description_result: String with HTML formatting contained. 
        Output of return_string function
    Returns
    ----------
    String of description result

    """
    job_output = []
    i = 0
    for job_url in job_urls:
        i += 1
        print(str(i) + " of " + str(len(job_urls))) #You can uncomment this if you want to make sure it is progressing through the web pages
        description_result = None
        title_result = None
        company_result = None
        time.sleep(random.randint(10,100)/100) #I generally put in a random time-delay to not overload servers and not get banned
        try: 
            req = Request(job_url, headers= {'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, "html.parser")
            #Get raw results
            title_result = soup.find_all("h1")
            location_result = soup.find_all("a", class_="jobs-top-card__bullet")
            company_result = soup.find_all("a", class_="topcard__org-name-link")
            description_result = soup.find_all("section", class_="description")
            #Clean results
            title = return_string(title_result)
            company = return_string(company_result)
            location = return_string(location_result)
            description = clean_description(description_result)
            description_result = str(description_result)
            #Compile results into dictionary
            job_info = {
                "title":title,
                "company":company,
                "location":location,
                "url":job_url,
                "description":description,
                "description_raw":description_result,
            }#Append dictionary to list
            job_output.append(job_info)
        except: 
            pass
    return(job_output)

def search_link(job_url: str) -> dict:
    """
    #Returns dictionary of information of interest from LinkedIn job url

    Parameters
    ----------
    job_url: Individual job url to search on 

    Returns
    ----------
    Dictionary with elements of interest to job_url. 

    """
    time.sleep(random.randint(10,50)/100) #I generally put in a random time-delay to not overload servers and not get banned
    title = None
    company = None
    location = None
    location_result = None
    company_result = None 
    description = None
    description_result = None
    try: 
        req = Request(job_url, headers= {'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, "html.parser")
        #Get raw results
        title_result = soup.find_all("h1")
        location_result = soup.find_all("span", class_="topcard__flavor topcard__flavor--bullet")
        company_result = soup.find_all("a", class_="topcard__org-name-link")
        description_result = soup.find_all("section", class_="description")
        #Clean results
        title = return_string(title_result)
        company = return_string(company_result)
        location = return_string(location_result)
        description = clean_description(description_result)
        description_result = str(description_result)
        #Compile results into dictionary
        job_info = {
            "title":title,
            "company":company,
            "location":location,
            "url":job_url,
            "description":description,
            "description_raw":description_result,}
        return(job_info)
    except:
        pass



def return_string(soup_result: BeautifulSoup) -> list:
    """
    #Returns cleaned string of BeautifulSoup result

    Parameters
    ----------
    soup_result: LinkedIn search page to search on

    Returns
    ----------
    list of text from soup_result split on HTML tags. 

    """
    if len(soup_result)==0:
        return(None)
    else: 
        text = str(soup_result)
        text = text.split(">")[1]
        text = text.split("<")[0]
        return(text)

def clean_description(description_result: str) -> str:
    """
    #Returns cleaned string of description result

    Parameters
    ----------
    description_result: String with HTML formatting contained. 
        Output of return_string function
    Returns
    ----------
    String of description result

    """
    if len(description_result)==0:
        return(None)
    else: 
        description_text = str(description_result)
        description_text = re.sub('<[^<]+?>'," ", description_text)
        description_text = re.sub('  '," ", description_text)
        return(description_text)
assert clean_description("") == None


def remove_escape_chars(text: str) -> str:
    """
    #Returns cleaned string of description result

    Parameters
    ----------
    text: String containing escape characters
    
    Returns
    ----------
    Cleaned string (without escape characters)

    """
    text = text.replace("-", "")
    text = text.replace("[", "")
    text = text.replace("{", "")
    text = text.replace("(", "")
    return(text)
assert remove_escape_chars("-[{(text")=="text"
assert remove_escape_chars("-[[[[[[{(text")=="text"

#return_list function returns the list that follows a certain word. 
#Job description often have list sections (e.g., Requirements: list)
def return_list(text: str, list_starters: list) -> list:
    """
    #Returns list from section that was 'bulleted' in job description based on list_starters

    Parameters
    ----------
    text: String with HTML formatting contained. 
    list_starters: Words to use that often preceed bulleted list in job postings (e.g., "Requirements")
    
    Returns
    ----------
    List of items that followed 'list_starters'. 

    """
    jobs_quals = []
    text = text.lower()
    list_starters = [x.lower() for x in list_starters]
    split_list = text.split("<li>") #Split each list element into its own text.
    text = remove_escape_chars(text)
    text = remove_escape_chars(text)#Need to run twice because of "--"
    false_list = [False] * len(list_starters)
    for i in range(0,len(split_list)):
        text = split_list[i]
        if [x in text for x in list_starters] != false_list:
            y = [x in text for x in list_starters]
            print(y)
            list_starter = np.array(list_starters)[np.array(y)]
            list_starter = str(list_starter[0])
            
            #Create a list and store each 'qualification' in it
            job_quals = []
            for n in range(i+1, len(split_list)):           
                if "</li>" in split_list[n]:
                    qual = split_list[n]
                    qual = qual.split("</li>")[0]
                    job_quals.append(qual)
                    print("List item")
            #Define output as a dictionary with the qualification type and the qualifications
            job_dict = {list_starter : job_quals}
            jobs_quals.append(job_dict)
    return(jobs_quals)

def job_attribute(df: pd.DataFrame, colname: str, search_column: str, search_string: str=None) -> pd.DataFrame:
    """
    #Converts prescence of job_attributes in described sections into dummy columns

    Parameters
    ----------
    df: DataFrame with columns to search on and add to. 
    colname: New column name to create
    search_column: Column to search for search_string in
    search_string: String corresponding to attribute to search for (e.g., Python). 
    
    Returns
    ----------
    Amended DataFrame with new column indicating prescence of search_string in new colname. 


    """
    z = pd.Series(0, index=df.index)
    if search_string==None:
        search_string = colname
    if type(search_string)==str:
        z = df[search_column].str.find(search_string)
    if type(search_string)==list:
        for x in search_string:    
            y = df[search_column].str.find(x)
            z = z + y
    df[colname] = z  
    del z 
    df[colname] = df[colname].apply(lambda x: 1 if x >0 else 0)
    return(df)

def show_progress(it: iter, milestones: int=1) -> None:
    """
    #Enumerates progress when searching many listing. 

    Parameters
    ----------
    it: Iterable 
    milestones: Frequency with which to report progress. Defaults to 1. 
    Returns
    ----------
    None

    """
    for i, x in enumerate(it):
        yield x
        processed = i + 1
        if processed % milestones == 0:
            print('Processed %s elements' % processed)

