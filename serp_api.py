from serpapi.google_search import GoogleSearch

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
        "api_key": "17211ecac1162f32835e7e803dc8f7c1d6325fbe4aaf3b47cdb8b6101a43d83f"
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
    print('Results: ',results)
    data_list = []
    if key in results:
        if type == "GEO_MAP_0":
            for item in results[key]:
                location = {
                    "continent": item['geo'],
                    "location": item["location"],
                    "continent_value": item["value"]
                }
                data_list.append(location)             
            print('Location_Data: ',data_list)
        elif type == "RELATED_QUERIES":
            for item in results[key]["top"]:
                query = {
                    "queries_title": item["query"],
                    "queries_value": item["value"]
                }
                data_list.append(query)
            print('Queries: ',data_list)    
        elif type == "RELATED_TOPICS":
            for item in results[key]["top"]:
                topic = {
                    "title": item["topic"]["title"],
                    "type": item['topic']['type'],
                    "value": item["value"]
                }
                data_list.append(topic)
            print('Topic: ',data_list)
    return data_list
__all__ = ['fetch_data']
#Each time print = call once api for once (Free: 100 tokens)
#fetch_data('youtube','GEO_MAP_0')

