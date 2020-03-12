
def search_links(job_urls):
    job_output = []
    for job_url in job_urls:
        #print(job_url) #You can uncomment this if you want to make sure it is progressing through the web pages
        
        time.sleep(random.randint(10,100)/100) #I generally put in a random time-delay to not overload servers and not get banned
        try: 
            req = Request(job_url, headers= {'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, "html.parser")
            
            #Get raw results
            title_result = soup.find_all("h1")
            company_result = soup.find_all("a", class_="topcard__org-name-link")
            description_result = soup.find_all("section", class_="description")
            
            #Clean results
            title = return_string(title_result)
            company = return_string(company_result)
            description = clean_description(description_result)
            
            #Compile results into dictionary
            job_info = {
                'title': title,
                'company': company,
                'url' : job_url,
                'description' : description,
                'description_raw': str(description_result)
            }
            del description_result
            del title_result
            del company_result
            #Append dictionary to list
            job_output.append(job_info)
        except:
            pass
    return(job_output)