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

    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                  xanchor='left', yanchor='bottom',
                                  text=title,
                                  font=dict(family='Arial',
                                            size=30,
                                            color='rgb(37,37,37)'),
                                  showarrow=False))

    fig.update_layout(annotations=annotations)

    fig.write_image(ofile)
    print('Saved precip chart: %s' % ofile)


def generate_point_impacts(point_impacts_csv, md_file_name):
    # markdown table
    # https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
    if os.path.exists(md_file_name):
        os.remove(md_file_name)

    df = pd.read_csv(point_impacts_csv)

    with open(md_file_name, 'w') as mdf:
        mdf.write(
        """
        ### Population and cropland most likely impacted by flood detection this week\n
        > Population and cropland located in areas detected as flood this week\n
        """)

        mdf.write("Department  |  District |  Village  |  Flood Area \n")
        mdf.write("---|---|---|---\n")

        for department in ['Cuvette', 'Likouala', 'Plateaux']:
            df_sub = df[df['ADM1_NAME'] == department]
            df_sub_copy = df_sub.copy()
            df_sub_copy.sort_values('floodArea', inplace=True, ascending=False)
            count = 0
            for row in df_sub_copy.iterrows():
                if count == 5:
                    break

                mdf.write("%s  |  %s  |  %s  |  %f  \n" %
                          (row[1]['ADM1_NAME'], row[1]['ADM2_NAME'], row[1]['NAME'], row[1]['floodArea']))
                print("%s  |  %s  |  %s  |  %f  \n" %
                          (row[1]['ADM1_NAME'], row[1]['ADM2_NAME'], row[1]['NAME'], row[1]['floodArea']))
                count += 1

    print('Saved %s' % md_file_name)


def generate_raster_impacts(raster_impacts_csv, md_file_name):
    # markdown table
    # https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
    if os.path.exists(md_file_name):
        os.remove(md_file_name)

    df = pd.read_csv(raster_impacts_csv)

    with open(md_file_name, 'w') as mdf:
        mdf.write(
        """
        ### Population and cropland most likely impacted by flood detection this week\n
        > Population and cropland located in areas detected as flood this week\n
        """)

        mdf.write("Department  |  District |  Agriculture impacted [km<sup>2</sup>] |  Potential population impacted  |  Roads impacted (m) \n")
        mdf.write("---|---|---|---|---\n")

        cond1 = (df['agSum'] > 0) & (df['popSum'] > 0)
        cond2 = (df['roadSum'] > 0) & (df['popSum'] > 0)
        cond3 = (df['roadSum'] > 0) & (df['agSum'] > 0)
        df = df[
            cond1 & cond2 & cond3
        ]

        df.sort_values("agSum", inplace=True)
        count = 0
        for row in df.iterrows():
            if count == 20:
                break
            mdf.write("%s  |  %s  |  %f  |  %f  |  %f  \n" %
                      (row[1]['Admin1Name'], row[1]['Admin2Name'], row[1]['agSum'], row[1]['popSum'], row[1]['roadSum']))
            print("%s  |  %s  |  %f  |  %f  |  %f  \n" % (row[1]['Admin1Name'], row[1]['Admin2Name'], row[1]['agSum'], row[1]['popSum'], row[1]['roadSum']))
            count += 1

    print('Saved %s' % md_file_name)



def generate_report_markdown(ag_impacts_csv, pop_impacts_csv, md_file_name):
    # markdown table
    # https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
    if os.path.exists(md_file_name):
        os.remove(md_file_name)

    ag_df = pd.read_csv(ag_impacts_csv)
    pop_df = pd.read_csv(pop_impacts_csv)

    ag_df.set_index('Admin2Name')
    pop_df.set_index('Admin2Name')
    df = pop_df.join(ag_df, lsuffix='_pop', rsuffix='_ag')

    with open(md_file_name, 'w') as mdf:
        mdf.write(
        """
        ### Population and cropland most likely impacted by flood detection this week\n
        > Population and cropland located in areas detected as flood this week\n
        """)

        mdf.write("Top 10 Departments  |  Potential population most likely impacted  |  Potential crops most likely impacted [km<sup>2</sup>]\n")
        mdf.write("---|---|---\n")

        df.sort_values("popImpacted", inplace=True)
        count = 0
        for row in df.iterrows():
            if count == 10:
                break

            mdf.write("%s  |  %f  |  %f\n" % (row[1]['Admin2Name_pop'], row[1]['popImpacted'], row[1]['agImpacted_km2']))
            # print (row[1]['Admin2Name_pop'], row[1]['popImpacted'], row[1]['agImpacted_km2'])
            count += 1
    print('Saved %s' % md_file_name)


base_dir = os.path.dirname(__file__)
precip_csv_file = os.path.join(base_dir,
                               r"./data/csv/2020-01-31_Precip_Congo_Precip_gsmapGC_20200101-20200131.csv")

ofile = os.path.join(base_dir, r'./output/precip_plot.svg')
# make_plot(precip_csv_file, ofile)

ag_impacts_csv = os.path.join(base_dir,
                              r'./data/csv/2020-01-31_impacts_Congo_ag_impacts_s1_2020-01-31.csv')
pop_impacts_csv = os.path.join(base_dir,
                               r'./data/csv/2020-01-31_impacts_Congo_pop_impacts_s1_2020-01-31.csv')
# generate_report_markdown(ag_impacts_csv, pop_impacts_csv, os.path.join(base_dir, r'./output/md/slide3-pop-ag-impacts.md'))

# raster_impacts_csv = r"./data/csv/2020-01-31_impacts_RasterImpactsSummary.csv"
# generate_raster_impacts(raster_impacts_csv,
#                         os.path.join(base_dir, r'./output/md/raster-impacts.md')
#                         )

point_impacts_csv = r"./data/csv/2020-01-31_impacts_PointImpactsSummary.csv"
generate_point_impacts(point_impacts_csv,
                        os.path.join(base_dir, r'./output/md/point-impacts.md')
                        )
