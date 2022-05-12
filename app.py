#from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify,make_response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import *
import requests
from helpers import video_id,login_required
import yfinance as yf
from crawler_app import c_app, yt_search_concall,yt_search_buzz
from twitter_search import tsearch
from symbol_gen import symbolgen
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



apikey = "AIzaSyDItQskhnKsjc3zd5XOCQd1GcvY9hN6uGE"

cred = credentials.Certificate('firebase-adminsdk.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://slpfapp-1640204388019-default-rtdb.firebaseio.com/'
})
# configure application
app = Flask(__name__)

app.config['SECRET_KEY'] = 'super secret'
# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_FILE_DIR"] = mkdtemp()
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# app.config["SECRET_KEY"] = "super secret key"
# app.secret_key = 'BAD_SECRET_KEY'

# app.config["SESSION_FILE_DIR"] = mkdtemp()
# app.config["SESSION_PERMANENT"] = True
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)


# configure CS50 Library to use SQLite database
# db = SQL("sqlite:///finance1.db")


@app.route("/register", methods=["GET", "POST"])
def register():

    # forget any user_id
    # session.clear()
    session.pop('user_id', default=None)
    session.pop('user_name', default=None)

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        firstname = request.form.get("fname")
        lastname = request.form.get("lname")
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if password != password2:
            flash("Passwords do not match", "error")
            return render_template("register.html")

        details={
                        'email':username,
                        'password':password,
                        'returnSecureToken': True
                }
        try:
            r=requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={}'.format(apikey),data=details)
            if 'error' in r.json().keys():
                print(r.json()['error']['message'])
                flash("Username Already Exists", "error")
                return render_template("register.html")

            #if the registration succeeded
            if 'idToken' in r.json().keys() :
                unique_id = r.json()['localId']
                ref = db.reference('users')
                user_ref = ref.child(unique_id)
                user_ref.set({
                            'username':firstname+" "+lastname,
                            'email' : username
                        })

            # user = auth.create_user_with_email_and_password(username, password)
            # unique_id = auth.get_account_info(user['idToken'])
            # unique_id = (unique_id['users'][0]['localId'])
        except:
            flash("Username Already Exists", "error")
            return render_template("register.html")
        flash("New user registered", "success")
        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    
    # forget any user_id
    # session.clear()
    session.pop('user_id', default=None)
    session.pop('user_name', default=None)
    if request.method == "POST":
        try:
            details={
                        'email':request.form.get("username"),
                        'password':request.form.get("password"),
                        'returnSecureToken': True
                    }
            # send post request
            r=requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}'.format(apikey),data=details)
            #check for errors in result
            if 'error' in r.json().keys():
                print(r.json()['error']['message'])
                flash("Invalid Username/Password", "error")
                return redirect(url_for("login"))
            #if the registration succeeded
            if 'idToken' in r.json().keys() :
                unique_id = r.json()['localId']
            # user = auth.sign_in_with_email_and_password(request.form.get("username"), request.form.get("password"))

            # remember which user has logged in
            # unique_id = auth.get_account_info(user['idToken'])
            # unique_id = (unique_id['users'][0]['localId'])
            res = make_response(redirect(url_for("index_stock")))
            res.set_cookie("user_id", unique_id, max_age=60*60*24*7)
            session["user_id"] = unique_id
            session["user_name"] = db.reference('users').child(unique_id).child('username').get()
            
            # redirect user to home page
            flash("success", "welcome")
            return(res)
            # return redirect(url_for("index_stock"))

        except:
                flash("Invalid Username/Password", "error")
                return redirect(url_for("login"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")




@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    email = db.reference('users').child(request.cookies.get("user_id")).child('email').get()
    try:
        headers = {
        'Content-Type': 'application/json',
        }
        data={"requestType":"PASSWORD_RESET","email":email}
        r = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={}'.format(apikey), data=data)
        if 'error' in r.json().keys():
            flash("The email you provided while signup is not valid", "error")
            return redirect(url_for("changepass"))
        if 'email' in r.json().keys():
            flash("Password Change Email Successfully Sent", "success")
            return redirect(url_for("index_stock"))
    except:
        flash("The email you provided while signup is not valid", "error")
        return redirect(url_for("changepass"))

@app.route("/")
@login_required
def index_stock():

    # user = session['user_name']
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    return render_template("stock-index.html", user=user)

@app.route("/quote_stock", methods=["GET", "POST"])
@login_required
def quote_stock():
    symbollist,BSEList,NSEList,Sectors = symbolgen()
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        try:
            sector=Sectors[symbol]
        except:
            sector="General Sector"

        try:
            stockname = symbollist[symbol.upper()]
            return render_template("stock-buy.html", sector=sector,symbol=symbol, user=user ,name=stockname)
        except:
            flash("invalid stock or Trade Ban on this Script", "error")
            return render_template("stock-quote.html" , user=user)

    else:
        return render_template("stock-quote.html" , user=user)



@app.route("/trade_stock")
@login_required
def trade_stock():
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    symbol = list()
    ref = db.reference('stock').child('portfolio').child(request.cookies.get("user_id"))
    snapshot = ref.order_by_key().get()
    if(snapshot != None):
        sy = list(snapshot.keys())
        sy = (list(sy))
        if len(sy) != 0:
            for i in range(len(sy)):
                symbol.append(sy[i])
        data = zip(symbol)
        return render_template("stock-trade.html", data=data , user=user)
    else:
        data = zip([])
        return render_template("stock-trade.html", data=data , user=user)


@app.route("/buy_stock", methods=["GET", "POST"])
@login_required
def buy_stock():

    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    ref = db.reference('stock').child('portfolio').child(request.cookies.get("user_id"))
    snapshot = ref.order_by_key().get()
    if snapshot == None:
        symbol = request.form.get("symbol").upper()
        ref = db.reference('stock').child('portfolio').child(request.cookies.get("user_id")).child(symbol)
        ref.set({'last transacted': datetime.timestamp(datetime.now())})
        flash("Added New Stock to Portfolio", "success")
        return redirect(url_for("trade_stock"))
        
    else:
        user_folio = list(snapshot.keys())
        symbollist,BSEList,NSEList,Sectors = symbolgen()

        if request.method == "POST":
            symbol = request.form.get("symbol").upper()

            if(user_folio == None or symbol not in user_folio):
                print("Hello")
                ref = db.reference('stock').child('portfolio').child(request.cookies.get("user_id")).child(symbol)
                ref.set({'last transacted': datetime.timestamp(datetime.now())})

            else:
                flash("Already Present in your Folio", "success")
                return redirect(url_for("trade_stock"))
                # return render_template("stock-index.html" , user=user)
            flash("Added New Stock to Portfolio", "success")
            return redirect(url_for("trade_stock"))
            # return render_template("stock-index.html" , user=user)

        else:
            return render_template("stock-buy.html", user=user )


@app.route("/sell_stock", methods=["GET", "POST"])
@login_required
def sell_stock():
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    ref = db.reference('stock').child('portfolio').child(request.cookies.get("user_id"))
    snapshot = ref.order_by_key().get()
    user_folio = list(snapshot.keys())

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if symbol not in user_folio:
            flash("You don't have it your portfolio", "error")
            return redirect(url_for("trade_stock"))

        ref = db.reference('stock').child('portfolio').child(request.cookies.get("user_id")).child(symbol.upper())
        ref.delete()
        flash("Stock Removed from Portfolio", "success")
        return redirect(url_for("trade_stock"))
    else:
        return render_template("stock-sell.html", user=user )



@app.route("/portfolio_stock")
@login_required
def portfolio_stock():
     
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    symbollist,BSECodes,NSEList,Sectors = symbolgen()
    # user = db.execute("SELECT username FROM users WHERE id = :id", id= request.cookies.get("user_id"))
    symbol = list()
    name = list()
    sector = list()
    screenerlink = list()
    valuelink = list()

    ref = db.reference('stock').child('portfolio').child(request.cookies.get("user_id"))
    snapshot = ref.order_by_key().get()
    sy = list(snapshot.keys())
    if(sy != None):
        sy = (list(sy))
        if len(sy) != 0:
            for i in range(len(sy)):
                symbol.append(sy[i])
                name.append(symbollist[sy[i]])
                try:
                    sector.append(Sectors[sy[i]])
                    
                except:
                    sector.append("General Sector")
                if(sy[i] not in NSEList):
                    screenerlink.append("https://www.screener.in/company/"+BSECodes[sy[i]]+"/consolidated/")
                else:
                    screenerlink.append("https://www.screener.in/company/"+sy[i]+"/consolidated/")
                valuelink.append("https://forum.valuepickr.com/search?q="+sy[i]+"%20order%3Alatest")
            data = zip(symbol, name, sector, screenerlink,valuelink)
            return render_template("stock-portfolio.html", data=data, lat_value=0, top_gain='-', top_loss='-', overall_gl=0 , user=user)
        else:
            return render_template("stock-portfolio.html", lat_value=0, top_gain='-', top_loss='-', overall_gl=0 , user=user)

    else:
        return render_template("stock-portfolio.html", lat_value=0, top_gain='-', top_loss='-', overall_gl=0 , user=user)



@app.route("/concall_stock", methods=["GET", "POST"])
@login_required
def concall_stock():

     
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    if request.method == "POST":
        date = request.form.get("date")
        symbol = list()
        concall = list()
        element = datetime.strptime(date,"%Y-%m-%d")
        timestamp = datetime.timestamp(element)
        dtobj = datetime.fromtimestamp(timestamp)
        yt_time=(dtobj.isoformat("T") + "Z")
        ref = db.reference('stock').child('portfolio').child(request.cookies.get("user_id"))
        snapshot = ref.order_by_key().get()
        sy = list(snapshot.keys())
        if(sy != None):
            sy = (list(sy))

            if len(sy) != 0:
                for i in range(len(sy)):

                    full_name = sy[i]
                    x_cc = yt_search_concall(full_name.replace(" ",""),yt_time)
                    if((x_cc)!=-1):
                        concall.append("https://www.youtube.com/embed/"+x_cc)
                        symbol.append(sy[i])
                data = zip(symbol, concall)

                return render_template("stock-concall.html", data=data, user=user )
            else:
                return render_template("stock-concall.html", user=user )

        else:
            return render_template("stock-concall.html", user=user )

    else:
        date = "2021-08-01"
        symbol = list()
        concall = list()
        element = datetime.strptime(date,"%Y-%m-%d")
        timestamp = datetime.timestamp(element)
        dtobj = datetime.fromtimestamp(timestamp)
        yt_time=(dtobj.isoformat("T") + "Z")
        symbol = list()
        concall = list()
        ref = db.reference('stock').child('portfolio').child(request.cookies.get("user_id"))
        snapshot = ref.order_by_key().get()
        sy = list(snapshot.keys())
        if(sy != None):
            sy = (list(sy))

            if len(sy) != 0:
                for i in range(len(sy)):

                    full_name = sy[i]
                    x_cc = yt_search_concall(full_name.replace(" ",""),yt_time)
                    if((x_cc)!=-1):
                        concall.append("https://www.youtube.com/embed/"+x_cc)
                        symbol.append(sy[i])

                data = zip(symbol, concall)

                return render_template("stock-concall.html", data=data, user=user )
            else:
                return render_template("stock-concall.html", user=user )

        else:
            return render_template("stock-concall.html", user=user )

@app.route("/videos_stock" ,methods=["GET", "POST"])
@login_required
def videos_stock():

     
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    if request.method == "POST":
        date = request.form.get("date")
        element = datetime.strptime(date,"%Y-%m-%d")
        timestamp = datetime.timestamp(element)
        dtobj = datetime.fromtimestamp(timestamp)
        yt_time=(dtobj.isoformat("T") + "Z")
        symbol = list()
        buzz = list()
        ref = db.reference('stock').child('portfolio').child(request.cookies.get("user_id"))
        snapshot = ref.order_by_key().get()
        sy = list(snapshot.keys())
        if(sy != None):
            sy = (list(sy))

            if len(sy) != 0:
                for i in range(len(sy)):

                    full_name = sy[i]
                    x_cc = yt_search_buzz(full_name.replace(" ",""),yt_time)
                    if(len(x_cc)>0):
                        for j in range(len(x_cc)):
                            symbol.append(sy[i])
                            buzz.append("https://www.youtube.com/embed/"+x_cc[j])

                data = zip(symbol, buzz)

                return render_template("stock-videos.html", data=data, user=user )
            else:
                return render_template("stock-videos.html", user=user )

        else:
            return render_template("stock-videos.html", user=user )
    else:
        date = "2021-10-01"
        element = datetime.strptime(date,"%Y-%m-%d")
        timestamp = datetime.timestamp(element)
        dtobj = datetime.fromtimestamp(timestamp)
        yt_time=(dtobj.isoformat("T") + "Z")
        symbol = list()
        buzz = list()
        ref = db.reference('stock').child('portfolio').child(request.cookies.get("user_id"))
        snapshot = ref.order_by_key().get()
        sy = list(snapshot.keys())
        if(sy != None):
            sy = (list(sy))

            if len(sy) != 0:
                for i in range(len(sy)):

                    full_name = sy[i]
                    x_cc = yt_search_buzz(full_name.replace(" ",""),yt_time)
                    if(len(x_cc)>0):
                        for j in range(len(x_cc)):
                            symbol.append(sy[i])
                            buzz.append("https://www.youtube.com/embed/"+x_cc[j])

                    else:
                        buzz.append("No Meeting Records seem to be there for this Script")
                        symbol.append(sy[i])

                data = zip(symbol, buzz)

                return render_template("stock-videos.html", data=data, user=user)
            else:
                return render_template("stock-videos.html", user=user)

        else:
            return render_template("stock-videos.html", user=user)

@app.route("/tweets_stock")
@login_required
def tweets_stock():
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()

    symbol = list()
    tweetids = list()
    ref = db.reference('stock').child('portfolio').child(request.cookies.get("user_id"))
    snapshot = ref.order_by_key().get()
    sy = list(snapshot.keys())
    if(sy != None):
        sy = (list(sy))
   
        if len(sy) != 0:
            for i in range(len(sy)):
                # try:
                #     ticksym = yf.Ticker(sy[i]+".NS")
                #     full_name = ticksym.info['longName']
                # except:
                #     full_name = sy[i]
                full_name = sy[i]
                x_cc = tsearch(full_name.replace(" ",""))
                x_cc.reverse()
                if(len(x_cc)>0):
                    for j in range(len(x_cc)):
                        symbol.append(sy[i])
                        tweetids.append(x_cc[j])

                else:
                    tweetids.append("807811447862468608")
                    symbol.append(sy[i])


            data = zip(symbol, tweetids)

            return render_template("stock-tweets.html", data=data, user=user)
        else:
            return render_template("stock-tweets.html", user=user)

    else:
        return render_template("stock-tweets.html", user=user)

@app.route("/investor_stock", methods=["GET", "POST"])
@login_required
def investor_stock():
    
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    investor = list()
    ref = db.reference('stock').child('investor').child(request.cookies.get("user_id"))
    snapshot = ref.order_by_key().get()
    if(snapshot != None):
        sy = list(snapshot.keys())
    
        sy = (list(sy))

        if len(sy) != 0:
            for i in range(len(sy)):
                investor.append(sy[i])
    
        data = zip(investor)
        return render_template("stock-investors.html", data=data, user=user)
    else:
        data = zip([])
        return render_template("stock-investors.html", data=data, user=user)

@app.route("/addinvestor_stock", methods=["GET", "POST"])
@login_required
def addinvestor_stock():
    
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    ref = db.reference('stock').child('investor').child(request.cookies.get("user_id"))
    snapshot = ref.order_by_key().get()
    if(snapshot == None):
        investor = request.form.get("investor")
        ref = db.reference('stock').child('investor').child(request.cookies.get("user_id")).child(investor)
        ref.set({'last transacted': datetime.timestamp(datetime.now())})
        flash("Added New Investor to Watchlist", "success")
        return redirect(url_for("investor_stock"))
    else:
        user_folio = list(snapshot.keys())
        if request.method == "POST":
            investor = request.form.get("investor")
            if(user_folio == None or investor not in user_folio):
                ref = db.reference('stock').child('investor').child(request.cookies.get("user_id")).child(investor)
                ref.set({'last transacted': datetime.timestamp(datetime.now())})

            else:
                flash("Already Present in your Watchlist", "success")
                return redirect(url_for("investor_stock"))
                # return render_template("stock-index.html", user=user)
            flash("Added New Investor to Watchlist", "success")
            return redirect(url_for("investor_stock"))
            # return render_template("stock-index.html", user=user)


@app.route("/removeinvestor_stock", methods=["GET", "POST"])
@login_required
def removeinvestor_stock():

    
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    ref = db.reference('stock').child('investor').child(request.cookies.get("user_id"))
    snapshot = ref.order_by_key().get()
    user_folio = list(snapshot.keys())

    if request.method == "POST":
        investor = request.form.get("investor")
        if investor not in user_folio:
            flash("You don't have it your watchlist", "error")
            return redirect(url_for("investor_stock"))

        ref = db.reference('stock').child('investor').child(request.cookies.get("user_id")).child(investor)
        ref.delete()

        flash("Investor Removed from Watchlist", "success")
        return redirect(url_for("investor_stock"))

@app.route("/sharktweets_stock")
@login_required
def sharktweets_stock():
    
    
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    investors = list()
    tweetids = list()
    ref = db.reference('stock').child('investor').child(request.cookies.get("user_id"))
    snapshot = ref.order_by_key().get()
    sy = list(snapshot.keys())
    if(sy != None):
        sy = (list(sy))
   
        if len(sy) != 0:
            for i in range(len(sy)):
                full_name = sy[i]
                x_cc = tsearch(full_name.replace(" ","+"))
                x_cc.reverse()
                if(len(x_cc)>0):
                    for j in range(len(x_cc)):
                        investors.append(sy[i])
                        tweetids.append(x_cc[j])

            data = zip(investors, tweetids)

            return render_template("stock-sharktweets.html", data=data, user=user)
        else:
            return render_template("stock-sharktweets.html", user=user)

    else:
        return render_template("stock-sharktweets.html", user=user)

@app.route("/user_stock",methods=["GET", "POST"])
@login_required
def user_stock():
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    userlist = list()
    idlist = list()
    ref = db.reference('users')
    snapshot = ref.order_by_key().get()
    if(snapshot != None):
        sy = list(snapshot.keys())
        sy = (list(sy))
        if len(sy) != 0:
            for i in range(len(sy)):
                idlist.append(sy[i])
                userlist.append(db.reference('users').child(sy[i]).child('username').get())
        data = zip(userlist,idlist)
        return render_template("stock-user.html", data=data , user=user)
    else:
        data = zip([])
        return render_template("stock-user.html", data=data , user=user)

@app.route("/buddyfolio_stock",methods=["GET", "POST"])
@login_required
def buddyfolio_stock():
    user = db.reference('users').child(request.cookies.get("user_id")).child('username').get()
    symbol = list()
    buddyid = request.form.get("buddyid")
    ref = db.reference('stock').child('portfolio').child(buddyid)
    snapshot = ref.order_by_key().get()
    if(snapshot != None):
        sy = list(snapshot.keys())
        sy = (list(sy))
        if len(sy) != 0:
            for i in range(len(sy)):
                symbol.append(sy[i])
        data = zip(symbol)
        buddyname=db.reference('users').child(buddyid).child('username').get()
        return render_template("stock-buddyfolio.html", data=data , user=user, buddy=buddyname)
    else:
        buddyname=db.reference('users').child(buddyid).child('username').get()
        symbol.append("Portfolio Empty :( Motivate "+buddyname+" to start Investing")
        data = zip(symbol)
        return render_template("stock-buddyfolio.html", data=data , user=user,buddy=buddyname)

@app.route("/logout")
def logout():
    # forget any user_id
    res = make_response(redirect(url_for("login")))
    res.set_cookie("user_id", "None", max_age=0)
    session.clear()
    # session.pop('user_id', default=None)
    # session.pop('user_name', default=None)
    return res
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run()
