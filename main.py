import pandas as pd
import numpy as np
import panel as pn

pn.extension('tabulator')

import hvplot.pandas

df = pd.read_csv("https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv")
if 'data' not in pn.state.cache.keys():

    df = pd.read_csv('https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv')

    pn.state.cache['data'] = df.copy()

else:

    df = pn.state.cache['data']

print(df)

print("THe new dataframe is :", df[df['country'] == 'North America'])
print(df[df['country'] == 'World'])

df = df.fillna(0)
df['gdp_per_capita'] = np.where(df['population'] != 0, df['gdp'] / df['population'], 0)

idf = df.interactive()



year_slider = pn.widgets.IntSlider(name='Year slider', start=1750, end=2020, step=5, value=1850)
print(year_slider)

yaxis_co2 = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=['co2', 'co2_per_capita', ],
    button_type='success'
)

print(yaxis_co2)

continents = ['World', 'Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica']

co2_pipeline = (
    idf[
        (idf.year <= year_slider) &
        (idf.country.isin(continents))
        ]
        .groupby(['country', 'year'])[yaxis_co2].mean()
        .to_frame()
        .reset_index()
        .sort_values(by='year')
        .reset_index(drop=True)
)

print(co2_pipeline)

co2_plot = co2_pipeline.hvplot(x='year', by='country', y=yaxis_co2, line_width=2, title="CO2 emission by continent")
print(co2_plot)

co2_table = co2_pipeline.pipe(pn.widgets.Tabulator, pagination='remote', page_size=10, sizing_mode='stretch_width')
print(co2_table)

co2_vs_gdp_scatterplot_pipeline = (
    idf[
        (idf.year == year_slider) &
        (~ (idf.country.isin(continents)))
        ]
        .groupby(['country', 'year', 'gdp_per_capita'])['co2'].mean()
        .to_frame()
        .reset_index()
        .sort_values(by='year')
        .reset_index(drop=True)
)

print(co2_vs_gdp_scatterplot_pipeline)

yaxis_co2_source = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=['coal_co2', 'oil_co2', 'gas_co2'],
    button_type='success'
)

continents_excl_world = ['Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica']

co2_source_bar_pipeline = (
    idf[
        (idf.year == year_slider) &
        (idf.country.isin(continents_excl_world))
        ]
        .groupby(['year', 'country'])[yaxis_co2_source].sum()
        .to_frame()
        .reset_index()
        .sort_values(by='year')
        .reset_index(drop=True)
)

co2_source_bar_plot = co2_source_bar_pipeline.hvplot(kind='bar',
                                                     x='country',
                                                     y=yaxis_co2_source,
                                                     title='CO2 source by continent')
print(co2_source_bar_plot)

template = pn.template.FastListTemplate(
    title='World CO2 emission dashboard',
    sidebar=[pn.pane.Markdown("# CO2 Emissions and Climate Change"),
             pn.pane.Markdown(
                 "#### Carbon dioxide emissions are the primary driver of global climate change. It???s widely "
                 "recognised that to avoid the worst impacts of climate change, the world needs to urgently reduce "
                 "emissions. But, how this responsibility is shared between regions, countries, and individuals has "
                 "been an endless point of contention in international discussions."),
             pn.pane.Markdown("## Settings"),
             year_slider],
    main=[pn.Row(pn.Column(yaxis_co2,
                           co2_plot.panel(width=700), margin=(0, 25)),
                 co2_table.panel(width=500)),
          pn.Row(pn.Column(co2_vs_gdp_scatterplot_pipeline.panel(width=600), margin=(0, 25)),
                 pn.Column(yaxis_co2_source, co2_source_bar_plot.panel(width=600)))],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)
#template.show()

