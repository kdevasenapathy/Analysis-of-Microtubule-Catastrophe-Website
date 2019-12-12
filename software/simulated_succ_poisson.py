import numpy  as np
import pandas as pd

import bokeh_catplot
import bokeh.io
bokeh.io.output_notebook()

# Below, `t_star` refers to the quantity $t^* = \beta_1 t$ and `r_B` to 
# the quantity $r_\beta = \frac{\beta_2}{\beta_1}$.

# Instantiate the rng
rg = np.random.default_rng()

# Parameters
n = 150
B_1 = 10

# beta ratios to plot ecdfs for
r_Bs = [2 ** i for i in range(-5, 4) if i != 0]

# Sample times for beta_1
t_1s = rg.exponential(1/B_1, size=n * len(r_Bs))

# Sample times for beta_2
t_2s = np.array([])
for r_B in r_Bs:
    t_2s = np.append(t_2s, rg.exponential(1/(r_B * B_1), size=n))

# Add the times together and convert to unitless time
t_stars = (t_1s + t_2s) * B_1

# Create tidy data frame
cols = {'B_2/B_1' : sorted(r_Bs * n), 
        't*'      : t_stars} 
df = pd.DataFrame(data=cols)     

# Plot the ecdfs
p = bokeh_catplot.ecdf(
    df, 
    'B_2/B_1', 
    't*', 
    width=750, 
    height=750, 
    x_axis_label = 'B_1 * t',
    style='staircase',
    title = "Simulated Successive Poisson Process Model"
)

p.legend.title = "B_2/B_1"
bokeh.io.show(p)