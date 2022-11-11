import pandas as pd
import numpy as np
import panel as pn
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go

import hvplot.pandas

pn.extension('tabulator')

df = pd.read_csv(
    "C:/Users/User/Desktop/My Courses/Honours/Year_Project/Github_repos/Graph_visualization/GenomeData.csv")
print(df)

df2 = pd.read_csv(
    "C:/Users/User/Desktop/My Courses/Honours/Year_Project/Github_repos/Graph_visualization/SpecieData.csv")

print(df2)

print(df['Generation_ID'])

if 'data' not in pn.state.cache.keys():

    df = pd.read_csv('C:/Users/User/Desktop/My Courses/Honours/Year_Project/Github_repos/Graph_visualization'
                     '/GenomeData.csv')
    df2 = pd.read_csv(
        "C:/Users/User/Desktop/My Courses/Honours/Year_Project/Github_repos/Graph_visualization/SpecieData.csv")

    pn.state.cache['data'] = df.copy()
    pn.state.cache['data2'] = df2.copy()

else:

    df = pn.state.cache['data']

df.to_csv('GenomeData.csv')
df2.to_csv('SpecieData.csv')

pdf2 = pd.read_csv('GenomeData.csv')
pdf3 = pd.read_csv('SpecieData.csv')

print("This is the new one", pdf2)
print(pdf2['Generation_ID'])
# making the dataframe interactive
idf = pdf2.interactive()

# get the rows of the dataframe
endGeneration = pdf2.shape[0]
print("The end generation is :", endGeneration)

generation_slider = pn.widgets.IntSlider(name='Generation slider', start=2, end=endGeneration + 1, step=1)

Genome_List = pdf2['Genome_Fitness'].astype(float).tolist()
print(Genome_List)
print(idf.Genome_Fitness)

# creating the two plots (Line graph and the bar graph)
Generation_Fitness_plot = pdf2.hvplot.line(x='Generation_ID', y=['Genome_Fitness', 'Generation Average Fitness'],
                                           line_width=3,
                                           title="Genome Fitness over generations", legend='bottom', height=400,
                                           width=800)

SpecieCount_Generation_plot = pdf2.hvplot.bar(x='Generation_ID', y='Active_Species', line_width=2,
                                              title="Active Species per Generation", width=800)

colors = ['lightslategray', ] * 5
# creating a bar graph for specie average fitness
specieAverageFitness_plot = pdf3.hvplot.bar(x='Specie ID', y='Average Fitness',
                                            legend='top', height=400, width=800, marker_color=colors)

# creating the pie chart

print(pdf2['Genome_SpecieID'])
dominantSpeciePie = px.pie(pdf2, values='Genome_Specie_Members', names='Genome_SpecieID', width=380, height=380,
                           title='Dominant Species', hole=.5)

SpecieStagnationPie = px.pie(pdf2, values='Generation Stagnation', names='Generation_ID', width=380, height=380,
                             title='Stagnation per generation')

# Scatter plot of species and their average fitness
Specie_Average_Fitness_Plot = pdf2.hvplot.scatter(x='Active_Species', y='Specie_Size', by='Generation_ID',
                                                  legend='top', height=400, width=400)

# displaying the neural network
jpgfile = Image.open("image.png")

template = pn.template.FastListTemplate(
    title='NEAT Dashboard',
    sidebar=[pn.pane.Markdown("# NEAT Analytics"),
             pn.pane.Markdown(
                 "#### NEAT is Cool."),
             pn.pane.Markdown("## Settings"),
             generation_slider],
    main=[pn.Row(pn.Column(Generation_Fitness_plot, margin=(0, 25)), dominantSpeciePie),
          pn.Row(pn.Column(SpecieCount_Generation_plot, margin=(0, 25)), SpecieStagnationPie),
          pn.Row(pn.Column(Specie_Average_Fitness_Plot, margin=(0, 25)))],
    accent_base_color="#88d8b0",
    header_background="#88d8b0", theme_toggle=True,
)
template.show()
