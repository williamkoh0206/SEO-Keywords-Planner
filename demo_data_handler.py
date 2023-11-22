import json,base64
import pandas as pd
import matplotlib.pyplot as plt
from Get_Continent import *
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg

def jsonHandler(type):
    file_path = f"demo_json_data/{type}"
    with open(file_path, encoding='utf-8') as file:
        data = json.load(file)
    result = []
    if type == "cityu_region.json":
        for item in data:
            loc_short_form = item['location_in_short']
            location = item['location']
            continent_value = item['continent_value']
            continent_match = continent[continent['country'] == loc_short_form]['continent'].values[0]
            result.append({'location_in_short': loc_short_form, 'location': location, 'continent_value': continent_value,'continent':continent_match})

    elif type == "cityu_queries.json":
        for item in data:
            queries_title = item['queries_title']
            queries_value = item['queries_value']
            result.append({'queries_title': queries_title, 'queries_value': queries_value})

    elif type == "cityu_topics.json":
        for item in data:
            title = item['title']
            topic_type = item['type']
            topic_value = item['value']
            result.append({'Topic': title, 'Topic_Type': topic_type, 'value': topic_value})
    #print(result)
    return result

def chart(type):
    data = jsonHandler(type)
    df = pd.DataFrame.from_dict(data)
    if type == 'cityu_region.json':
        df['continent_value'] = df['continent_value'].replace('<1', '0')
        df['continent_value'] = df['continent_value'].astype('int')
        df['location_in_short'] = df['location_in_short'].map(
            continent.set_index('country')['continent'])
        df = df.drop(columns=['location'])
        df_gp = df.groupby(['location_in_short']).agg(value=('continent_value', 'sum'))
        df_gp = df_gp.reset_index()
        df_gp.rename(columns={"location_in_short": "continent"}, inplace=True)
        df_gp.rename(columns={"value": "continent_value"}, inplace=True)
        df_gp = df_gp[df_gp['continent_value'] >= 1]
        plt.pie(df_gp['continent_value'], labels=df_gp['continent'],
                autopct='%1.1f%%', startangle=0, pctdistance=0.65)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.04), ncol=3)
        plt.title('%s region search pie chart '%'cityu')
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png',bbox_inches='tight')
        img_buffer.seek(0)

        img_data = img_buffer.getvalue()
        img_src = 'data:image/png;base64,' + base64.b64encode(img_data).decode()
        plt.close()
        return img_src

    elif type == 'cityu_queries.json':
        df['queries_value'] = df['queries_value'].str.extract('(\d+)')
        df['queries_value'] = df['queries_value'].astype('int')
        fig, ax = plt.subplots()
        ax.barh(df['queries_title'], df['queries_value'])
        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)
        plt.xticks(rotation=0, ha='center', fontsize=8)
        ax.grid(color='grey',
                linestyle='-.', linewidth=0.5,
                alpha=0.2)
        ax.set_title('%s queries search bar chart'%'cityu', loc='center',)
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png',bbox_inches='tight')
        img_buffer.seek(0)
        img_data = img_buffer.getvalue()
        img_src = 'data:image/png;base64,' + base64.b64encode(img_data).decode()
        plt.close()
        return img_src

    elif type == 'cityu_topics.json':
        df['value'] = df['value'].str.extract('(\d+)')
        df['value'] = df['value'].astype('int')
        df['Other'] = ''
        df.loc[df['value'] < 4, 'Other'] = 'Yes'
        df['Other'] = df['Other'].fillna('No')
        df.loc[df['Other'] == 'Yes', 'Topic'] = 'Other'
        df_gp = df.groupby(['Topic']).agg(value=('value', 'sum'))
        df_gp = df_gp.reset_index()
        plt.pie(df_gp['value'], labels=df_gp['Topic'], autopct='%1.1f%%', startangle=0)
        plt.legend(loc='upper center', bbox_to_anchor=(0.4, -0.04), ncol=3)
        plt.title('%s topics search pie chart'%'cityu')
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png',bbox_inches='tight')
        img_buffer.seek(0)
        img_data = img_buffer.getvalue()
        img_src = 'data:image/png;base64,' + base64.b64encode(img_data).decode()
        plt.close()
        return img_src

jsonHandler('cityu_region.json')

'''
cityu_topics.json
cityu_queries.json
cityu_region.json
'''
