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
            short_form = item['location_in_short']
            location = item['location']
            continent_value = item['continent_value']
            result.append({'location_in_short': short_form, 'location': location, 'continent_value': continent_value})

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
        plt.show()
        # plt.title('%s region search pie chart '%'cityu')
        # plt.savefig('cityu_region.png',bbox_inches='tight')
        # buf = BytesIO()
        # FigureCanvasAgg(fig).print_png(buf)
        # buf_str = "data:image/png;base64,"
        # buf_str += base64.b64encode(buf.getvalue()).decode('utf8')

    elif type == 'cityu_queries.json':
        df['queries_value'] = df['queries_value'].str.extract('(\d+)')
        df['queries_value'] = df['queries_value'].astype('int')
        fig, ax = plt.subplots()
        ax.bar(df['queries_title'], df['queries_value'])
        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)
        plt.xticks(rotation=90, ha='center', fontsize=8)
        ax.grid(color='grey',
                linestyle='-.', linewidth=0.5,
                alpha=0.2)
        ax.set_title('%s queries search bar chart'%'cityu', loc='center',)
        # plt.savefig('cityu_queries.png',bbox_inches='tight')
        # buf = BytesIO()
        # FigureCanvasAgg(fig).print_png(buf)
        # buf_str = "data:image/png;base64,"
        # buf_str += base64.b64encode(buf.getvalue()).decode('utf8')

    elif type == 'cityu_topics.json':
        df['value'] = df['value'].str.extract('(\d+)')
        df['value'] = df['value'].astype('int')
        df.loc[df['value'] < 3, 'Other'] = 'Yes'
        df['Other'] = df['Other'].fillna('No')
        df.loc[df['Other'] == 'Yes', 'Topic_Type'] = 'Other'
        df_gp = df.groupby(['Topic_Type']).agg(value=('value', 'sum'))
        df_gp = df_gp.reset_index()
        plt.pie(df_gp['value'], labels=df_gp['Topic_Type'], autopct='%1.1f%%', startangle=0)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.04), ncol=3)
        plt.title('%s topics search pie chart'%'cityu')
        plt.show()
        # plt.savefig('cityu_topics.png',bbox_inches='tight')
        # buf = BytesIO()
        # FigureCanvasAgg(fig).print_png(buf)
        # buf_str = "data:image/png;base64,"
        # buf_str += base64.b64encode(buf.getvalue()).decode('utf8')

chart('cityu_topics.json')
'''
related_topics.json
related_queries.json
interest_by_region.json
'''
