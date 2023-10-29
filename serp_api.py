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
    print(results)
    data_list = results[key]
    return data_list
__all__ = ['fetch_data']
#Each time print = call once api for once (Free: 100 tokens)
#print(data_list)

