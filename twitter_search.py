import requests
import os
import json
import urllib


bearer_token = ""
search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields



def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    listid=[]
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    js = (json.loads(response.content.decode()))
    for i in js["data"]:
        listid.append("https://twitter.com/x/status/"+i["id"])
    return (listid[0:4])



def tsearch(company_name):
    qry = "(" + company_name + ") (-is:retweet) (lang:en)"
    # ((from:porinju) OR (from:Iamsamirarora) OR (from:BMTheEquityDesk) OR (from:bibekdebroy) OR (from:dugalira) OR (from:Moneylifers) OR (from:andymukherjee70) OR (from:Moneylifers) OR (from:udaytharar) OR (from:Moneylifers))
    query_params = {'query': qry,}
    json_response = connect_to_endpoint(search_url, query_params)
    return(json_response)
   







