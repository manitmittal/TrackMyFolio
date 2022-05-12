from google_search import google_search
from scraper import scrape
from urllib.request import urlopen
import json
from datetime import datetime

LIMIT_WEBSITES = 3

def c_app(company_name):
    search_data = google_search(company_name)
    urls = search_data.get('urls', [])
    urls = urls
    
    return urls
# print(c_app("Acrysil"))

def yt_search_concall(company_name,yt_time):

    q = company_name + "%20Concall%20AlphaStreet"
    query = "https://www.googleapis.com/youtube/v3/search?publishedAfter="+yt_time+"&key=&q="+q
    response = urlopen(query)
    data_json = json.loads(response.read())
    try:
        return(data_json["items"][0]['id']['videoId'])
    except:
        return(-1)

def yt_search_buzz(company_name,yt_time):
    video_list=[]
    q = company_name + "%20Stock%20Latest%20News%20Interview"
    query = "https://www.googleapis.com/youtube/v3/search?publishedAfter="+yt_time+"&key=&q="+q
   
    response = urlopen(query)
    data_json = json.loads(response.read())
    for i in range(0,5):
        try:
            video_list.append(data_json["items"][i]['id']['videoId'])
        except:
            break
    return(video_list)

