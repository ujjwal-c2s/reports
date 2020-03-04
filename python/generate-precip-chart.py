import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import os


def str2dt(s):
    return datetime.strptime(s, '%Y-%m-%d')


def make_plot(precip_csv_file, ofile):
    title = 'GSMaP Precipitation by Region'
    df = pd.read_csv(precip_csv_file)
    departments = df['Admin1Name']
    df1 = df.transpose()
    df2 = df1.drop('Admin1Name', axis=0)
    col = 0

    labels = []
    str_x_data = df2.index.values
    x_data = [ str2dt(s) for s in str_x_data]

    y_data = []

    for department in departments:
        labels.append(department)
        y_data.append(df2[col])
        col += 1

    # https://plot.ly/python/discrete-color/
    colors = [
        "rgb(229, 134, 6)",
        "rgb(93, 105, 177)",
        "rgb(82, 188, 163)",
        "rgb(153, 201, 69)",
        "rgb(204, 97, 176)",
        "rgb(36, 121, 108)",
        "rgb(218, 165, 27)",
        "rgb(47, 138, 196)",
        "rgb(107, 17, 0)",
        "rgb(237, 100, 90)",
        "rgb(165, 170, 153)",
    ]

    fig = go.Figure()

    for i in range(0, min(len(colors), len(labels))):
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data[i],
            mode='lines',
            name=labels[i],
            line=dict(color=colors[i], width=3),
            connectgaps=True,
        ))

    fig.update_layout(
        plot_bgcolor='white',
        xaxis=dict(
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            gridcolor='rgb(204, 204, 204)',
            gridwidth=1,
            title_text='Date (UTC)',
            title_font={"size": 20},
        ),
        yaxis=dict(
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            gridcolor='rgb(204, 204, 204)',
            gridwidth=1,
            title_text='Precipitation (mm)',
            title_font={"size": 20},
        ),
        showlegend=True,
        legend = dict(
            font=dict(
                family='Arial',
                size=18,
                color='rgb(82, 82, 82)',
            ),
        )
    )

    annotations = dict(xref='paper',
                            yref='paper',
                            x=0.0,
                            y=1.05,
                            xanchor='left',
                            yanchor='bottom',
                            text=title,
                            font=dict(family='Arial', size=30, color='rgb(37,37,37)'),
                            showarrow=False)
    fig.update_layout(annotations=annotations)
    fig.write_image(ofile)

    print('Saved precip chart: %s' % ofile)


base_dir = os.path.dirname(os.path.dirname(__file__))
project_dir = r'data/congo/2020-02-29'
base_dir = os.path.join(base_dir, project_dir)

precip_csv_file = os.path.join(base_dir, r"csv/2020-02-29_Precip_Congo_Precip_gsmapGC_20200201-20200229.csv")
ofile = os.path.join(base_dir, r'output/precip_plot_2020-02-29.svg')
make_plot(precip_csv_file, ofile)
