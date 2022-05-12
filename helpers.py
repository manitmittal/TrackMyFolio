from functools import wraps
from flask import redirect, render_template, request, session, url_for
import csv
import urllib.request
from urllib.parse import urlparse,parse_qs



def login_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.cookies.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def video_id(value):
   
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

