# """Functions plotting results."""

# import plotly.express as px
# import plotly.graph_objects as go
# import seaborn as sns
# import pandas as pd

# def plot_weights(IO_naics_2_digit,weights):
#     """Plot consumption (solid line) and investment weights (dashed line) for each industry."""
#     weights_graph=weights.merge(IO_naics_2_digit,on='IOCode',how='left')
#     weights_graph['Year'] = pd.to_datetime(weights_graph.year, format="%Y")
#     weights_graph=weights_graph.melt(id_vars=['Year','naics'],
#                    value_vars=['consumption weights', 'investment weights'],
#                   value_name='Weight',var_name='Industry')
#     weights_graph['Industry']=weights_graph.Industry.map({'consumption weights':'Consumption',
#                            'investment weights':'Investment'})
#     weights_graph.rename(columns={'naics':'Naics'},inplace=True)
#     g = sns.relplot(x='Year',y='Weight',hue='Naics',style='Industry',
#                 facet_kws=dict(sharey=False,sharex=False),
#            linewidth=4,col='Naics',col_wrap=3,kind='line',
#             aspect=1.5,data=weights_graph)
#     fig=g.set_titles('{col_name}')
#     fig=g._legend.remove()
#     return fig
