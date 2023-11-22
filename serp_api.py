from serpapi.google_search import GoogleSearch
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['MingLiU']
from Get_Continent import *
# keyword = "youtube"
# type = ["GEO_MAP_0","RELATED_QUERIES","RELATED_TOPICS"]
# key = ["interest_by_region","related_queries","related_topics"] 
'''
[0]: Type: GEO_MAP_0 | interest_by_region
[1]: Type: RELATED_QUERIES | related_queries
[2]: Type: RELATED_TOPICS | related_topics
'''
def fetch_data(keyword,type):
    #type = ["GEO_MAP_0","RELATED_QUERIES","RELATED_TOPICS"]
    #key = ["interest_by_region","related_queries","related_topics"] 
    params = {
        "engine": "google_trends",
        "q": keyword,
        "data_type": type,
        "api_key": "3d66e3d130aa6d290fd34915f7ec82fb77a8942ee8a4d5d2756b7b710f03f483"
    }
    key = ''
    if type == 'GEO_MAP_0':
        key = "interest_by_region"
    elif type == 'RELATED_QUERIES':
        key = "related_queries"
    elif type == 'RELATED_TOPICS':
        key = "related_topics"

    search = GoogleSearch(params)
    results = search.get_dict()
    #print('Results: ',results)
    data_list = []
    if key in results:
        if type == "GEO_MAP_0":
            for item in results[key]:
                location = {
                    "location_in_short": item['geo'],
                    "location": item["location"],
                    "continent_value": item["value"],
                    'continent_match': continent.loc[continent['country'] == item["geo"], 'continent'].values[0]
                }
                data_list.append(location)
            df = pd.DataFrame.from_dict(data_list)
            df['continent_value'] = df['continent_value'].replace('<1', '0')  # Replace '<1' with '0'
            df['continent_value'] = df['continent_value'].astype('int')
            #print(df['continent_value'].dtype)
            df['location_in_short'] = df['location_in_short'].map(
            continent.set_index('country')['continent'])
            df = df.drop(columns=['location'])
            df_gp = df.groupby(['location_in_short']).agg(value=('continent_value', 'sum'))
            df_gp = df_gp.reset_index()
            df_gp.rename(columns={"location_in_short": "continent"}, inplace=True)
            df_gp.rename(columns={"value": "continent_value"}, inplace=True)
            df_gp = df_gp[df_gp['continent_value'] >= 1]
            plt.pie(df_gp['continent_value'], labels=df_gp['continent'],
                    autopct='%1.1f%%', startangle=0, pctdistance=0.65, textprops={'fontsize': 8.5})
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.04), ncol=3)
            plt.title('%s region search pie chart '%keyword)
            image_filename = f'static/img/{keyword}_region.png'
            plt.savefig(image_filename,bbox_inches='tight')
            data_list.append({"image_filename": image_filename})
            plt.close()
            #plt.show()             
            #print('Location_Data: ',data_list)
        elif type == "RELATED_QUERIES":
            for item in results[key]["top"]:
                query = {
                    "queries_title": item["query"],
                    "queries_value": item["value"]
                }
                data_list.append(query)
            df = pd.DataFrame.from_dict(data_list)
            df['queries_value'] = df['queries_value'].str.extract('(\d+)')
            df['queries_value'] = df['queries_value'].astype('int')
            fig, ax = plt.subplots()
            ax.barh(df['queries_title'], df['queries_value'])
            ax.invert_yaxis()
            for s in ['top', 'bottom', 'left', 'right']:
                ax.spines[s].set_visible(False)
            plt.xticks(rotation=0, ha='center', fontsize=6)
            ax.grid(color='grey',
                    linestyle='-.', linewidth=0.5,
                    alpha=0.2)
            ax.set_title('%s queries search bar chart '%keyword,
                         loc='center', )
            image_filename = f'static/img/{keyword}_queries.png'
            plt.savefig(image_filename,bbox_inches='tight')
            data_list.append({"image_filename": image_filename})
            plt.close()
            #print('Queries: ',data_list)    
        elif type == "RELATED_TOPICS":
            for item in results[key]["top"]:
                topic = {
                    "title": item["topic"]["title"],
                    "type": item['topic']['type'],
                    "value": item["value"]
                }
                data_list.append(topic)
            #print('Topic: ',data_list)
            df = pd.DataFrame.from_dict(data_list)
            df['value'] = df['value'].str.extract('(\d+)')
            df['value'] = df['value'].astype('int')
            df.loc[df['value'] < 10, 'title'] = 'Other'
            df_gp = df.groupby(['title']).agg(value=('value', 'sum'))
            # df.loc[df['value'] < 10, 'Other'] = 'Yes'
            # df['Other'] = df['Other'].fillna('No')
            # df.loc[df['Other'] == 'Yes', 'Topic_Type'] = 'Other'
            # df_gp = df.groupby(['Topic_Type']).agg(value=('value', 'sum'))
            df_gp = df_gp.reset_index()
            plt.pie(df_gp['value'], labels=df_gp['title'],
                    autopct='%1.1f%%', startangle=0, textprops={'fontsize': 8.5})
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.04), ncol=3)
            plt.title('%s topics search pie chart'%keyword)
            image_filename = f'static/img/{keyword}_topics.png'
            plt.savefig(image_filename,bbox_inches='tight')
            data_list.append({"image_filename": image_filename})
            plt.close()
            #plt.show()
    #print(df)
    return data_list
__all__ = ['fetch_data']
#Each time print = call once api or once (Free: 100 tokens)
#fetch_data('cityu','RELATED_TOPICS')