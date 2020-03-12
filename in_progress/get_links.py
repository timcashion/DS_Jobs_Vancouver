def get_links(search_page):
    job_urls = []
    driver = Chrome()
    driver.get(jobs_page)
    time.sleep(3)
    more_jobs_path = '/html/body/main/section[1]/button'
    for i in range(1,20):
        time.sleep(3)
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
    return(job_urls)