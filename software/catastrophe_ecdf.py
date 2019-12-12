import numpy as np
import pandas as pd
import holoviews as hv

import bokeh
import bokeh.io
import bokeh.plotting

bokeh.io.output_notebook()

def ecdf_vals(data):
    '''
    Takes a one-dimensional Numpy array or Pandas Series and returns
    x and y values for plotting an ECDF in the "dots" style
    '''
    # Get the number of data points as well as the unique
    # values and their counts
    n = len(data)
    unique, counts = np.unique(data, return_counts=True)
    
    # ecdfs[i] corresponds to the ecdf for ith unique value 
    ecdfs = [counts[0]]
    
    # Go through the unique values, accumulating the count
    # of values we've seen below the value as well
    for i in range(1, len(unique)):
        ecdfs += [ecdfs[i-1] + counts[i]]
    
    # Normalize
    ecdfs = np.array(ecdfs)
    ecdfs = ecdfs / np.amax(ecdfs)
        
    # Return a list of tuples: (point, ecdf)
    return list(zip(unique, ecdfs))

# Get data on microtubule catastrophes
mic_df = pd.read_csv('../data/gardner_time_to_catastrophe_dic_tidy.csv')
mic_df.drop(mic_df.columns[0], axis=1)

# Get ecdfs for the labeled and unlabeled tubulin
labeled_ecdfs = np.array( \
                ecdf_vals( \
                [mic_df.values[i, 1] for i in range(mic_df.shape[0]) \
                 if mic_df.values[i, 2]]))
unlabeled_ecdfs = np.array( \
                    ecdf_vals( \
                    [mic_df.values[i, 1] for i in range(mic_df.shape[0]) \
                     if not mic_df.values[i, 2]]))

# Make the plot, like the one in Figure 2A of the given paper
ecdf_plot = bokeh.plotting.figure(
    plot_width=300, 
    plot_height=300, 
    x_axis_label="Catastrophe time (s)",
    y_axis_label="Cumulative distribution",
    title="ECDFs of Catastrophe Times"
    
)
ecdf_plot.circle(
    x=labeled_ecdfs[:, 0], 
    y=labeled_ecdfs[:, 1], 
    legend_label="Labeled",
    color='lime'
)
ecdf_plot.circle(
    x=unlabeled_ecdfs[:, 0], 
    y=unlabeled_ecdfs[:, 1], 
    legend_label="Unlabeled",
    color='royalblue'
)
ecdf_plot.legend.location = "bottom_right"

bokeh.io.show(ecdf_plot)