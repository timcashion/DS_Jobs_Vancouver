

### Setup
import pandas as pd
import numpy as np
import plotnine as p9

jobs_df = pd.read_csv("./data/vancouver_jobs_df_clean.csv")
skills_summary_df = pd.read_csv("./data/vancouver_skills_summary_df.csv")

#1. analysis

#Set plot aesthetics:
p9.theme_set(p9.theme_classic())

def sort_df(df, var_col, val_col="value", ascending=False):
    if len(set(var_col))<len(df):
        df_temp = df.groupby(var_col, as_index=False).sum()
        var_ordered = df_temp[var_col][df_temp[val_col].sort_values(ascending=ascending).index.tolist()] 
    else:
        var_ordered = df[var_col][df[val_col].sort_values(ascending=ascending).index.tolist()]    
    df[var_col] = pd.Categorical(df[var_col], categories=list(reversed(list(var_ordered))), ordered=True)
    return(df)
skills_summary_df = sort_df(skills_summary_df, var_col="variable")
skills_summary_df["type"] = pd.Categorical(skills_summary_df["type"])

skills_summary_df["type"] = skills_summary_df["type"].cat.reorder_categories(["Requirements", "Assets"])

(p9.ggplot(skills_summary_df, p9.aes('attribute', 'value', fill='variable')) + 
 p9.geom_col() +
 p9.coord_flip() +
 p9.scale_fill_discrete(guide=False)
)
#skills_summary_df["type"]

#Languages
languages = ["R", "sql", "python", "java", "scala", "C", "sas"]

lang_clean = {"sql": "SQL",
             "python": "Python",
             "R": "R",
             "java": "Java",
             "scala": "Scala",
             "C": "C",
             "sas": "SAS"}

skills_summary_lang = skills_summary_df[skills_summary_df.attribute.isin(languages)]
skills_summary_lang = skills_summary_lang.replace(to_replace=lang_clean)
skills_summary_lang = sort_df(skills_summary_lang, var_col="attribute")


lang_plot = (p9.ggplot(skills_summary_lang, p9.aes('attribute', 'value', fill='type', show_legend=False)) + 
 p9.geom_col() + 
 p9.coord_flip() + 
 p9.scale_y_continuous(expand=[0,0]) + 
 p9.labs(y="Frequency", x="Language", fill="") +
 p9.scale_fill_brewer(palette="Blues") +
 p9.facet_wrap('~type')
)
lang_plot.save(filename = 'figs/lang_plot.png', height=5, width=5, units = 'in', dpi=1000)
lang_plot


#Software
programs = ["tableau", "docker", "bigquery", "jira", "spark", "hadoop"]

prog_clean = {"tableau": "Tableau",
             "docker": "Docker",
             "bigquery": "Google BigQuery",
             "jira" : "Jira",
             "spark": "Spark",
             "hadoop": "Hadoop"}

skills_summary_prog = skills_summary_df[skills_summary_df.attribute.isin(programs)]
skills_summary_prog = skills_summary_prog.replace(to_replace=prog_clean)

skills_summary_prog = sort_df(skills_summary_prog, var_col="attribute")

soft_plot = (p9.ggplot(skills_summary_prog, p9.aes('attribute', 'value', fill='type', show_legend=False)) + 
 p9.geom_col() + 
 p9.coord_flip() + 
 p9.scale_y_continuous(expand=[0,0]) + 
 p9.labs(y="Frequency", x="Program", fill="") +
 p9.scale_fill_brewer(palette= "Greens")
)
soft_plot.save(filename = 'figs/soft_plot.png', height=5, width=5, units = 'in', dpi=1000)
soft_plot


#Education basic
education = ["bachelor", "master", "phd"]

education_clean = {"bachelor": "Bachelor's",
             "master": "Master's",
             "phd": "PhD"}

skills_summary_edu = skills_summary_df[skills_summary_df.attribute.isin(education)]
skills_summary_edu = skills_summary_edu.replace(to_replace=education_clean)

edu_plot = (p9.ggplot(skills_summary_edu, p9.aes('attribute', 'value', fill='type', show_legend=False)) + 
 p9.geom_col() + 
 p9.coord_flip() + 
 p9.scale_y_continuous(expand=[0,0]) + 
 p9.labs(y="Frequency", x="Education", fill="") +
 p9.scale_fill_brewer(palette= "Reds")
)
edu_plot.save(filename = 'figs/edu_plot.png', height=5, width=5, units = 'in', dpi=1000)
edu_plot