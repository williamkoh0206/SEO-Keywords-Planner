from matplotlib import pyplot as plt
from api_handler import *
from Get_Continent import *


def chart(type):
    if type == "interest_by_region.json":
        df = jsonHandler("interest_by_region.json")
        df['value'] = df['value'].str.extract('(\d+)')
        df['value'] = df['value'].astype('int')
        df['continent'] = df['location_short_form'].map(
            continent.set_index('country')['continent'])
        df = df.drop(columns=['location', 'location_short_form'])
        print(df)
        df_gp = df.groupby(['continent']).agg(value=('value', 'sum'))
        df_gp = df_gp.reset_index()
        plt.pie(df_gp['value'], labels=df_gp['continent'],
                autopct='%1.1f%%', startangle=0)
        plt.show()
    if type == "related_topics.json":
        df = jsonHandler("related_topics.json")
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
    if type == 'related_queries.json':
        df = jsonHandler("related_queries.json")
        df['value'] = df['value'].str.extract('(\d+)')
        df['value'] = df['value'].astype('int')
        print(df)
        fig, ax = plt.subplots()
        ax.bar(df['Queries'], df['value'])
        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)
        plt.xticks(rotation=90, ha='center', fontsize=5)
        ax.grid(b=True, color='grey',
                linestyle='-.', linewidth=0.5,
                alpha=0.2)
        ax.set_title('Query',
                     loc='center', )
        plt.show()


chart("related_queries.json")