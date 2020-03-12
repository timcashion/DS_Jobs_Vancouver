import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
import numpy as np
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

