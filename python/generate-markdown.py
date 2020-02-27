import os
import pandas as pd
from datetime import datetime


def str2dt(s):
    return datetime.strptime(s, '%Y-%m-%d')


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

                mdf.write("%s  |  %s  |  %s  |  %d  \n" %
                          (row[1]['ADM1_NAME'], row[1]['ADM2_NAME'], row[1]['NAME'], row[1]['floodArea']))
                print("%s  |  %s  |  %s  |  %d  \n" %
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
            mdf.write("%s  |  %s  |  %.4f  |  %d  |  %d  \n" %
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


base_dir = os.path.dirname(os.path.dirname(__file__))

# ag_impacts_csv = os.path.join(base_dir, r'./data/csv/2020-01-31_impacts_Congo_ag_impacts_s1_2020-01-31.csv')
# pop_impacts_csv = os.path.join(base_dir, r'./data/csv/2020-01-31_impacts_Congo_pop_impacts_s1_2020-01-31.csv')
# generate_report_markdown(ag_impacts_csv, pop_impacts_csv, os.path.join(base_dir, r'./output/md/slide3-pop-ag-impacts.md'))

project_dir = r'data/congo/2020-01-31'
base_dir = os.path.join(base_dir, project_dir)

raster_impacts_csv = os.path.join(base_dir, r"csv/2020-01-31_impacts_RasterImpactsSummary.csv")
generate_raster_impacts(raster_impacts_csv, os.path.join(base_dir, r"output/raster-impacts-summary.md"))

point_impacts_csv = os.path.join(base_dir, r"csv/2020-01-31_impacts_PointImpactsSummary.csv")
generate_point_impacts(point_impacts_csv, os.path.join(base_dir, r"output/point-impacts-summary.md"))

