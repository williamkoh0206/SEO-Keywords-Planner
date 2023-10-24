import pandas as pd
import json

def jsonHandler(type):
    file_path = f"result_json/{type}"
    with open(file_path, encoding='utf-8') as file:
        data = json.load(file)
    result = []
    if type == "interest_by_region.json":
        for item in data:
            location = item['location']
            value = item['value']
            result.append({'location': location, 'value': value})
    elif type == "related_topics.json":
        for item in data['top']:
            title = item['topic']['title']
            topic_value = item['value']
            result.append({'Topic': title, 'value': topic_value})
    elif type == "related_queries.json":
        for item in data['top']:
            queries_title = item['query']
            queries_value = item['value']
            result.append({'Queries': queries_title, 'value': queries_value})
    df = pd.DataFrame(result)
    print(df.head(10))

jsonHandler("interest_by_region.json")

'''
related_topics.json
related_queries.json
interest_by_region.json
'''
