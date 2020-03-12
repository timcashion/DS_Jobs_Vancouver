
### Setup
import pandas as pd
import numpy as np
import plotnine as p9
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans 
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
from dimension_reduction_fx import plot_pca_vis, pca_df, pca_plot, sort_df
import umap

#Define default plot theme:
p9.theme_set(p9.theme_classic())

#Read in data:
jobs_df = pd.read_csv("jobs_df_clean.csv")
skills_summary_df = pd.read_csv("skills_summary_df.csv")

#Clean jobs data 
#jobs_df.columns #Inspect columns
jobs_df = jobs_df.fillna(value="None")
jobs_df['title'] = jobs_df['title'].str.lower()

#Assign 'type' based on simple rules:
jobs_df['type'] = str(0)
jobs_df.loc[jobs_df['title'].str.contains('analyst'), 'type'] = 'analyst'
jobs_df.loc[jobs_df['title'].str.contains('engineer'), 'type'] = 'engineer'
jobs_df.loc[jobs_df['title'].str.contains('scientist'), 'type'] = 'scientist'
jobs_df.loc[jobs_df['title'].str.contains('manager'), 'type'] = 'manager'
jobs_df.loc[jobs_df['title'].str.contains('director'), 'type'] = 'manager'
#len(jobs_df.loc[jobs_df['type'].str.contains('0'), :]) #950 jobs don't have a 'type'. 
jobs_df.loc[jobs_df['type'].str.contains('0'), 'type'] = 'unknown'
jobs_df = jobs_df.loc[jobs_df['type'] != 'unknown', :] #Remove job postings with an 'unknown' type

jobs_df.reset_index(inplace=True, drop=True)
pca_jobs_df = jobs_df.iloc[:,10:] #Take only the job attribute columns (numerics)
pca_jobs_df = pca_jobs_df.drop(columns='type') #Drop the type colunm from the df for PCA
pca_title = jobs_df[['title', 'type']] #Keep record of job titles and corresponding types for later


#determine number of components by MLE
pca = PCA(n_components='mle')
pca.fit(pca_jobs_df)
pca.explained_variance_ratio_ #Inspect explained variance ratio 

#Determine cut-off of 5% variance explained. Thus, select 5 elements. 
pca = PCA(n_components=5)
pca.fit(pca_jobs_df)

#pca_plot(pca_jobs_df, num_components= 5)
#Determine number of components through intuition (analyst, scientist, engineer, manager)
pca_5 = pca_df(pca_jobs_df, 5, pca_title)
pca_plot(pca_5, 'pc1', 'pc2', 'type')


#Plot all variations of this
#Find all unique combinations of principal components:
col_names = ['pc' + str(x) for x in np.arange(1, 5+1)]
combos = []
for i in range(0,5):
    for n in range(i+1, 5):
        new_pattern = [col_names[i], col_names[n]]
        combos.append(new_pattern)

#Plot each combo and save in figure folder. 
for combo in combos:
    p = pca_plot(pca_5, combo[0], combo[1], 'type')
    p.save("./figs/pca_5_" + combo[0] + "_" + combo[1] + ".png", dpi=600)


#Try out with UMAP as well:
umap_mod = umap.UMAP()
umap_mod.fit(pca_jobs_df)
umap.plot.points(umap_mod, color_key_cmap='Paired', labels=pca_title["type"])
plt.savefig("./figs/UMAP_Job_Title.png", dpi=300)
plt.show()


# K-means cluster analysis
clusters = 5
kmeans = KMeans(n_clusters = clusters) 
kmeans.fit(pca_jobs_df) 

#Try again with kmeans labels 
umap.plot.points(umap_mod, color_key_cmap='Paired', labels=kmeans.labels_)
plt.savefig("./figs/UMAP_Kmeans_5.png", dpi=300)
plt.show()


#Then fit PCA:
pca_result = pca_5
pca_result['kmean_label'] = kmeans.labels_

p = pca_plot(pca_result, dim1="pc1", dim2="pc2", dim3="type")
p.save("./figs/pca_5_type.png", dpi=600)
pca_result['kmean_label'] = pca_result['kmean_label'].astype(str)
p = pca_plot(pca_result, dim1="pc1", dim2="pc2", dim3="kmean_label")
p.save("./figs/pca_5_kmean_label.png", dpi=600)

map = pd.DataFrame(pca.components_, columns=pca_jobs_df.columns)
plt.figure(figsize=(12,9))
sns.heatmap(map, cmap='coolwarm', center = 0)
#plt.savefig('./figs/PCA_heatmap_clusters.png', dpi=600)
plt.show()

#Summarize different roles by their difference from each other
pca_jobs_df_labeled = pca_jobs_df
pca_jobs_df_labeled['kmean_label'] = kmeans.labels_
summary_table = pca_jobs_df_labeled.groupby('kmean_label').mean()
summary_table['kmean_label'] = summary_table.index

#Divide by minimum value to compute distance
noise_val = 1e-21
min_val = summary_table.min() + noise_val
x = summary_table/min_val

#Determine normalized difference:
pca_jobs_df_labeled = pca_jobs_df
pca_jobs_df_labeled['kmean_label'] = kmeans.labels_
summary_table = pca_jobs_df_labeled.groupby('kmean_label').mean()
summary_table['kmean_label'] = summary_table.index
summary_table_standardized = (summary_table - summary_table.mean()) / summary_table.std()
stack_table_standardized = summary_table_standardized.stack()
stack_table_standardized = stack_table_standardized.reset_index()
stack_table_standardized.columns = ['kmean_label', 'var', 'value']
(p9.ggplot(stack_table_standardized, p9.aes(x="kmean_label", y="value", fill="value"))
+ p9.geom_col()
+ p9.facet_wrap("~var") 
+ p9.coord_flip()
)

#Determine greatest difference skills
pca_jobs_df_labeled = pca_jobs_df
pca_jobs_df_labeled['kmean_label'] = kmeans.labels_
summary_table = pca_jobs_df_labeled.groupby('kmean_label').mean()
#summary_table['kmean_label'] = summary_table.index
perc_diff = summary_table.max() - summary_table.min()
perc_diff = perc_diff[perc_diff>0.4]
summary_table_diff = summary_table.loc[:, list(perc_diff.index)]
stack_table_diff = summary_table_diff.stack()
stack_table_diff = stack_table_diff.reset_index()
stack_table_diff.columns = ['kmean_label', 'var', 'value']
stack_table_diff['value'] = stack_table_diff['value'] * 100

(p9.ggplot(stack_table_diff, p9.aes(x="kmean_label", y="value", fill="kmean_label"))
+ p9.geom_col()
+ p9.facet_wrap("~var") 
+ p9.coord_flip()
+ p9.labs(x="K-Mean Cluster Label", y="Percentage of Jobs with Requirement Included") 
+ p9.theme(legend_position='none')
).save("./figs/KmeanLabel_GreatestDifference_Panel.png", dpi=600, width=14, height=8)
#Summarize different roles:
pca_jobs_df_labeled = pca_jobs_df
pca_jobs_df_labeled['kmean_label'] = kmeans.labels_
summary_table = pca_jobs_df_labeled.groupby('kmean_label').mean()
summary_table['kmean_label'] = summary_table.index
stack_table = summary_table.stack()
stack_table = stack_table.reset_index()
stack_table.columns = ['kmean_label', 'var', 'value']
stack_table['value'] = stack_table['value'] * 100
(p9.ggplot(stack_table, p9.aes(x="kmean_label", y="value", fill="kmean_label"))
+ p9.geom_col()
+ p9.facet_wrap("~var", scales="free_x") 
+ p9.coord_flip()
).save("./figs/KmeanLabel_Requirements_Panel.png", dpi=300)


stack_table_req = stack_table.loc[stack_table['var'].str.endswith('_Requirements'), :]
stack_table_req['var'] = stack_table_req['var'].str.replace('_Requirements', '')

for i in range(0,5):
    stack_table_req_temp = stack_table_req.loc[stack_table_req['kmean_label']==i, :]
    stack_table_req_temp = sort_df(stack_table_req_temp, var_col='var', val_col='value')
    stack_table_req_temp["var"] = pd.Categorical(stack_table_req_temp["var"])
    (p9.ggplot(stack_table_req_temp, p9.aes(x="var", y="value", fill="var"))
    + p9.geom_col()
    + p9.facet_wrap("~kmean_label", nrow=5) 
    + p9.coord_flip()
    + p9.labs(x="", y="Percentage of Jobs with Requirement Included") 
    + p9.theme(legend_position='none')
    ).save("./figs/KmeanLabel_Requirements_Panel" + str(i) + ".png", dpi=300, height=12, width=8)

stack_table_ass = stack_table.loc[stack_table['var'].str.endswith('_Assets'), :]
stack_table_ass['var'] = stack_table_ass['var'].str.replace('_Assets', '')

for i in range(0,5):
    stack_table_ass_temp = stack_table_ass.loc[stack_table_ass['kmean_label']==i, :]
    stack_table_ass_temp = sort_df(stack_table_ass_temp, var_col='var', val_col='value')
    stack_table_ass_temp["var"] = pd.Categorical(stack_table_ass_temp["var"])
    (p9.ggplot(stack_table_ass_temp, p9.aes(x="var", y="value", fill="var"))
    + p9.geom_col()
    + p9.facet_wrap("~kmean_label", nrow=5) 
    + p9.coord_flip()
    + p9.labs(x="", y="Percentage of Jobs with Assets Included") 
    + p9.theme(legend_position='none')
    ).save("./figs/KmeanLabel_Assets_Panel" + str(i) + ".png", dpi=300, height=12, width=8)


#Correlation heatmap:
req_cols = list(pca_jobs_df.columns[pca_jobs_df.columns.str.endswith('_Requirements')])
asset_cols = list(pca_jobs_df.columns[pca_jobs_df.columns.str.endswith('_Assets')])

reqs = pca_jobs_df.loc[:, req_cols]
reqs.columns = reqs.columns.str.replace("_Requirements", "")
reqs_heat = sns.heatmap(reqs.corr(), annot = False) 
plt.tight_layout()
plt.savefig("./figs/Requirements_Heatmap.png", dpi=300)

assets = pca_jobs_df.loc[:, asset_cols]
assets.columns = assets.columns.str.replace("_Assets", "")
assets_heat = sns.heatmap(assets.corr(), annot = False) 
plt.tight_layout()
plt.savefig("./figs/Asset_Heatmap.png", dpi=300)
plt.show()
# posting correlation heatmap to output console  

#Contribution of various PCA attribtues
for i in range(0,5):
    for n in range(i+1, 5):
        p = plot_pca_vis(pca, pca_jobs_df, pc_x=i, pc_y=n, num_dims=2)
        p.savefig("./figs/pca_5_contribution_" + col_names[i] + "_" + col_names[n] + ".png", dpi=600)


PCs = pca.components_
for i in range(0,5):
    pc1 = pd.DataFrame(zip(PCs[i,:], pca_jobs_df.columns))
    pc1.columns = ['pc', 'var']
    pc1 = pc1[np.abs(pc1.pc) > 0.2]
    pc1 = sort_df(pc1, var_col='var', val_col='pc')
    pc1["var"] = pd.Categorical(pc1["var"])
    (p9.ggplot(pc1, p9.aes(x='var', y='pc', fill='pc')) 
    + p9.geom_col() 
    + p9.coord_flip()
    + p9.labs(y='Principal Comoponent Weights', x= '')
    + p9.theme(legend_position='none')
    ).save("./figs/pca_5_contribution_bar_chart_limited_" + col_names[i] + ".png", dpi=600, height=9, width=6)


