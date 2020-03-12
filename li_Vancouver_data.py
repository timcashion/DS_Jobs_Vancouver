
### Packages
import pandas as pd
import numpy as np
import time
import random
import re
from math import floor, ceil
from li_scrape_fx import search_link, job_attribute, remove_escape_chars, return_string, clean_description, return_list, show_progress

search_output_clean = pd.read_csv("./data/linkedin_vancouver_data.csv")


jobs_df = pd.DataFrame(search_output_clean)
jobs_df = jobs_df.sort_values("company")
jobs_df["description"] = jobs_df["description"].astype(str) 
jobs_df["description_raw"] = jobs_df["description_raw"].astype(str)
jobs_df = jobs_df.drop_duplicates()

requirements = ["Qualifications", "Requirements", "Required Skills And Experience", "Background", "background includes",  "Skills", "Needs", "Basic Qualifications", "Must Have"]
responsibilities = ["Responsibilities", "Your Role Is To", "What’s the job?"]
assets = ["Assets", "Additional skills", "Charm Us With", "Preferred Qualifications", "Additional", "Bonus", "we'd love to see you have"]


false_list = [False] * len(requirements)


jobs_df["Requirements"] = jobs_df["description_raw"].apply(return_list, list_starters=requirements)
jobs_df["Responsibilities"] = jobs_df["description_raw"].apply(return_list, list_starters=responsibilities)
jobs_df["Assets"] = jobs_df["description_raw"].apply(return_list, list_starters=assets)

jobs_df["Requirements"].astype(str).str.find("qualifications")

#jobs_df
for n in range(1, len(jobs_df)):
    if len(jobs_df.loc[n, "Requirements"]) > 0:        
        if len(jobs_df.loc[n, "Assets"]) > 0:
            for i in range(0, len(jobs_df.loc[n, "Requirements"])):
                req_dict = jobs_df.loc[n, "Requirements"][i].values()
                for x in range(0, len(jobs_df.loc[n, "Assets"])):
                    asset_dict = jobs_df.loc[n, "Assets"][x].values()
                    if asset_dict==req_dict:
                        print("1")

jobs_df["Requirements"] = jobs_df["Requirements"].astype(str) 
jobs_df["Requirements"] = jobs_df["Requirements"].str.lower()
jobs_df["Assets"] = jobs_df["Assets"].astype(str) 
jobs_df["Assets"] = jobs_df["Assets"].str.lower()
jobs_df["Responsibilities"] = jobs_df["Responsibilities"].astype(str) 
jobs_df["Responsibilities"] = jobs_df["Responsibilities"].str.lower()


jobs_df["All"] = jobs_df["Requirements"].astype(str)  + jobs_df["Assets"].astype(str) 
jobs_df["All"] = jobs_df["All"].str.lower()

#simple searches just use the lower case text to search. Must be fairly unique
simple_searches = ["bigquery", "python", "sql", "jira", "tableau", "docker", "scala", "java", "spark", "hadoop",
                  "statistics", "nlp", "cnn", "rnn", "programming"]
cols = ["Requirements", "Assets"]

for col in cols:
    for search in simple_searches:
        job_attribute(df=jobs_df, colname=search+"_"+col, search_string=search, search_column=col)

#Complex searches wouldn't necessarily work, and would return a lot of false positives 
#E.g., 'r' would return every posting that has an 'r' in it. 
complex_searches = {
    "R": [" r,", " R or"],
    "bachelor" : ["bachelor", "bs/ms"],
    "master" : ["master", "bs/ms", " ms ", "graduate degree"],
    "phd" : ["phd","ph\.d" "graduate degree"],
    "C":  ["c\+", "c\+\+", "c#"],
    "ML": [" ml", "machine learning"],
    "CS":  ["computer science", " cs"],
    "SAS": [" sas ", " sas,", " sas\."],
    "AI": [" ai ", " ai,", "ai "]
}

#This for loop goes through each of the complex searches dictionary items 
#It creates a column based on the dictionary key, and uses the values as the search string
for col in cols:
    for search in complex_searches:
        job_attribute(df=jobs_df, colname=search+"_"+col, search_string=complex_searches[search], search_column=col)

#I have to clean the data for where a masters or phd degree appears in both the requirements and assets
jobs_df.loc[jobs_df["master_Requirements"]==1, "master_Assets"] = 0
jobs_df.loc[jobs_df["phd_Requirements"]==1, "phd_Assets"] = 0


#jobs_df["graduate_edu_all"] = 0 
#jobs_df["graduate_edu_all"].loc[jobs_df["master_all"]==1] = 1
#jobs_df["graduate_edu_all"].loc[jobs_df["phd_all"]==1] = 1

#Then I want to look at posting that require and graduate education or any university education
jobs_df["graduateEducation_Requirements"] = 0 
jobs_df.loc[jobs_df["master_Requirements"]==1, "graduateEducation_Requirements"] = 1
jobs_df.loc[jobs_df["phd_Requirements"]==1, "graduateEducation_Requirements"] = 1

jobs_df["university_Requirements"] = 0 
jobs_df.loc[jobs_df["master_Requirements"]==1, "university_Requirements"] = 1
jobs_df.loc[jobs_df["phd_Requirements"]==1, "university_Requirements"] = 1
jobs_df.loc[jobs_df["bachelor_Requirements"]==1, "university_Requirements"] = 1

#jobs_df
jobs_df.to_csv("./data/vancouver_jobs_df_clean.csv", index=False)


skills_summary = jobs_df.iloc[:, 10:len(jobs_df.columns)]
skills_summary = skills_summary.melt()
skills_summary = skills_summary.groupby('variable', as_index=False).sum()

skills_summary_df = pd.DataFrame(skills_summary)

skills_summary_df["variable"] = skills_summary_df["variable"].astype(str)
new_col = skills_summary_df["variable"].str.split(pat='_', expand=True)
skills_summary_df["attribute"] = new_col[0]
skills_summary_df["type"] = new_col[1]

#skills_summary_df.columns = ["variable", "value"]
skills_summary_df.to_csv("./data/vancouver_skills_summary_df.csv", index=False)