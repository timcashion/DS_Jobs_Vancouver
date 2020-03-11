#Dependencies:
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
import numpy as np
import plotnine as p9

def pca_df(df: pd.DataFrame, num_components: int, pca_title: pd.DataFrame):
    """
    Returns df with values of output from PCA with num_components.  
    Parameters
    ----------
    df: Dataframe to fit PCA on. 
    num_components: Number of components to fit in PCA. 

    Returns
    ----------
    Dataframe of fitted PCA values. 


    """
    pca = PCA(n_components = num_components)
    pca.fit(df)
    print(pca.explained_variance_ratio_)
    #pca.get_params
    col_names = ['pc' + str(x) for x in np.arange(1, num_components+1)]
    principalComponents = pca.fit_transform(df)

    principalDf = pd.DataFrame(data = principalComponents, 
                columns = col_names)
    principalDf['type'] = pca_title['type']
    return(principalDf)

def pca_plot(pca_data: pd.DataFrame, dim1: str, dim2: str, dim3: str):
    """ 
    Returns plot displaying 3 PCA variables (including color). 
    Parameters
    ----------
    pca: Fitted pca object to plot. 
    df: Dataframe pca was fit on. Used for column names. 
    dim1: String of column name of principal component to plot on x-axis. 
    dim2: String of column name of principal component to plot on y-axis.
    dim3: String of column name of principal component to plot as colour.

    Returns
    ----------
    Plot of PCA with dim1 on x-axis, dim2 on y-axis, and coloured by dim3


    """
    #Set plot theme within function: 
    p9.theme_set(p9.theme_classic())

    num_components = len(pca_data.columns) - 1
    color_type = type(pca_data.loc[0, dim3])
    p = (p9.ggplot(pca_data, p9.aes(x=dim1, y=dim2, fill=dim3))
        + p9.geom_point()
    )
    if(color_type==str):
        print('color type is qualitative')
        #Can't find a better colour palette yet.
        #p = p + (p9.scale_fill_brewer(type="qual", palette='Accent'))
    return(p)

def sort_df(df: pd.DataFrame, var_col: str, val_col: str="value", ascending: bool=False):
    """ 
    Returns df sorted by value with categorical labels for aesthetic sorted plots. 
    Parameters
    ----------
    pca: Fitted pca object to plot. 
    df: Dataframe pca was fit on. Used for column names. 
    var_col: String of column containg column to sort on.  
    val_col: String of column containg column to sort on. 
    ascending: Number of contributing elements to include for each axis. 

    Returns
    ----------
    sorted df with categorical var_col sorted by val_col. Defaults to a


    """
    if len(set(var_col))<len(df):
        df_temp = df.groupby(var_col, as_index=False).sum()
        var_ordered = df_temp[var_col][df_temp[val_col].sort_values(ascending=ascending).index.tolist()] 
    else:
        var_ordered = df[var_col][df[val_col].sort_values(ascending=ascending).index.tolist()]    
    df.loc[:, var_col] = pd.Categorical(df.loc[:, var_col], categories=list(reversed(list(var_ordered))), ordered=True)
    return(df)

def plot_pca_vis(pca: PCA, df: pd.DataFrame, pc_x: int = 0, pc_y: int = 1, num_dims: int = 5) -> plt:

    """
    Plot contribution of different dimensions to principal components. 
    
    Parameters
    ----------
    pca: Fitted pca object to plot. 
    df: Dataframe pca was fit on. Used for column names. 
    pc_x: Index of principal component to plot on x-axis. 
    pc_y: Index of principal component to plot on y-axis. 
    num_dims: Number of contributing elements to include for each axis. 

    Returns
    ----------
    Null

    Prints matplotlib.plt object. 

    https://stackoverflow.com/questions/45148539/project-variables-in-pca-plot-in-python
    Adapted into function by Tim Cashion
    """
    #Set plot theme within function: 
    p9.theme_set(p9.theme_classic())

    # Get the PCA components (loadings)
    PCs = pca.components_
    
    PC_x_index = PCs[pc_x, : ].argsort()[-num_dims:][::-1]
    PC_y_index = PCs[pc_y, : ].argsort()[-num_dims:][::-1]
    combined_index = set(list(PC_x_index) + list(PC_y_index))
    combined_index = sorted(combined_index)
    PCs = PCs[:, combined_index]
    # Use quiver to generate the basic plot
    fig = plt.figure(figsize=(5,5))
    plt.quiver(np.zeros(PCs.shape[1]), np.zeros(PCs.shape[1]),
            PCs[pc_x,:], PCs[pc_y,:], 
            angles='xy', scale_units='xy', scale=1)

    # Add labels based on feature names (here just numbers)
    feature_names = df.columns[combined_index]
    for i,j,z in zip(PCs[pc_y,:]+0.02, PCs[pc_x,:]+0.02, feature_names):
        plt.text(j, i, z, ha='center', va='center')

    # Add unit circle
    circle = plt.Circle((0,0), 1, facecolor='none', edgecolor='b')
    plt.gca().add_artist(circle)

    # Ensure correct aspect ratio and axis limits
    plt.axis('equal')
    plt.xlim([-1.0,1.0])
    plt.ylim([-1.0,1.0])

    # Label axes
    plt.xlabel('PC ' + str(pc_x))
    plt.ylabel('PC ' + str(pc_y))
    
    plt.tight_layout()
    return plt

