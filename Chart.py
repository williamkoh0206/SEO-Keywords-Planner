from matplotlib import pyplot as plt
from serp_api import *
from Get_Continent import *
#from api_handler import *


def chart(keyword,type):
    df = fetch_data(keyword,type)
    #df = jsonHandler(type)
    if type == 'GEO_MAP_0':
    #if type == 'interest_by_region.json':
        df['continent_value'] = df['continent_value'].str.extract('(\d+)')
        df['continent_value'] = df['continent_value'].astype('int')
        df['location_in_short'] = df['location_in_short'].map(
            continent.set_index('country')['continent'])
        df = df.drop(columns=['location'])
        df_gp = df.groupby(['location_in_short']).agg(value=('continent_value', 'sum'))
        df_gp = df_gp.reset_index()
        df_gp.rename(columns={"location_in_short": "continent"}, inplace=True)
        df_gp.rename(columns={"value": "continent_value"}, inplace=True)
        plt.pie(df_gp['continent_value'], labels=df_gp['continent'],
                autopct='%1.1f%%', startangle=0)
        plt.show()
    if type == "RELATED_TOPICS":
    #if type == "related_topics.json":
        df['value'] = df['value'].str.extract('(\d+)')
        df['value'] = df['value'].astype('int')
        df.loc[df['value'] < 10, 'Other'] = 'Yes'
        df['Other'] = df['Other'].fillna('No')
        df.loc[df['Other'] == 'Yes', 'Topic_Type'] = 'Other'
        df_gp = df.groupby(['Topic_Type']).agg(value=('value', 'sum'))
        df_gp = df_gp.reset_index()
        print(df_gp)
        plt.pie(df_gp['value'], labels=df_gp['Topic_Type'],
                autopct='%1.1f%%', startangle=0)
        plt.show()
    if type == 'RELATED_QUERIES':
    #if type == 'related_queries.json':
        df['queries_value'] = df['queries_value'].str.extract('(\d+)')
        df['queries_value'] = df['queries_value'].astype('int')
        print(df)
        fig, ax = plt.subplots()
        ax.bar(df['queries_title'], df['queries_value'])
        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)
        plt.xticks(rotation=90, ha='center', fontsize=6)
        ax.grid(color='grey',
                linestyle='-.', linewidth=0.5,
                alpha=0.2)
        ax.set_title('Query',
                    loc='center', )
        plt.show()


chart('youtube','GEO_MAP_0')
