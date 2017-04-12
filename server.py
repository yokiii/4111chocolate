#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.135.151/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@104.196.135.151/proj1part2"
#
DATABASEURI = "postgresql://yy2738:0744@104.196.135.151/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
##engine.execute("""CREATE TABLE IF NOT EXISTS test (
##  id serial,
##  name text
##);""")
##engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args


##Stock and Reorders
  #1.2. Chocolate where number on hand less than 20
  numbercursor = g.conn.execute("SELECT chocolate_id, chocolate_name, type, chocolate_price, number_on_hand, number_to_reorder FROM chocolate WHERE number_on_hand < 20")
  cnames = []
  for result in numbercursor:
    cnames.append(', '.join(unicode(r) for r in result))
  if len(cnames) == 0:
    cnames.append("No chocolate number under 20")
  numbercursor.close()

  #1.4. Show company contact information for chocolates where number on hand is under 20
  companycursor = g.conn.execute("SELECT chocolate.chocolate_name, company.company_name, company.phone_number, company.email FROM chocolate,company,makes WHERE (chocolate.number_on_hand < 20 and chocolate.chocolate_id = makes.chocolate_id) and makes.company_id = company.company_id")
  companyslist = []
  for result in companycursor:
    companyslist.append(', '.join(unicode(r) for r in result))
  if len(companyslist) == 0:
    companyslist.append("No chocolate number under 20")
  companycursor.close()

#### Profit and Revenue

  
  
  #3.2 Total Profit Gained
  tprofitcursor = g.conn.execute("SELECT SUM((ch.chocolate_price - ch.cost_per_piece) * i.quantity) FROM chocolate AS ch INNER JOIN \
                                  item AS i ON ch.chocolate_id = i.chocolate_id;")
  total = []
  for result in tprofitcursor:
    total.append(', '.join(unicode(r) for r in result))
  if len(total) == 0:
    total.append("No profit gainning yet")
  tprofitcursor.close();
  
  
  #3.3 Average revenue per order
  arevenuecursor = g.conn.execute("SELECT AVG(orders.order_price) FROM orders")
  average = []
  for result in arevenuecursor:
    average.append(', '.join(unicode(r) for r in result))
  if len(average) == 0:
    average.append("There is no order yet")
  arevenuecursor.close();
  

  
 

##Orders
  #4.1. Show order history
  allordercursor =  g.conn.execute("SELECT order_number, order_date, order_price FROM orders")
  allorders = []
  for result in allordercursor:
    allorders.append(', '.join(unicode(r) for r in result))
  if len(allorders) == 0:
    allorders.append("No order.")
  allordercursor.close()

  #4.2. Show incomplete orders
  incorderscursor = g.conn.execute("SELECT order_number, order_date, method_of_delivery, date_of_delivery FROM orders WHERE date_delivery_completed IS NULL")
  incorders = []
  for result in incorderscursor:
    incorders.append(', '.join(unicode(r) for r in result))
  if len(incorders) == 0:
    incorders.append("No incomplete order.")
  incorderscursor.close()
  

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(cnames = cnames, cname = stocks, ctypes=entries, companys=cinfos, ordersnotc=incorders, todayorders=oondate, specificorder=onum, allorders = orders, chocolateinfo = cbeans)
  context = dict(cnames = cnames, reorders = companyslist, orders = allorders, ordersnotc = incorders, profits = total, avgrevenues = average)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#


#1.1. Show the amount of number on hand based on one specific chocolate id
@app.route('/chocolatenumber', methods=['POST'])
def chocolatenumber():
  chocolateid = request.form['chocolate_id']
  ccursor = g.conn.execute("SELECT number_on_hand FROM chocolate WHERE chocolate_id= %s", chocolateid)
  cname = []
  for result in ccursor:
    cname.append(', '.join(unicode(r) for r in result))
  ccursor.close()
  context = dict(stocks = cname)
  if len(cname) > 0:
    return render_template("chocolatenumber.html", **context)
  else:
    return render_template("no.html")

#1.3. Find the company info of a chocolate by its id
@app.route('/companyinfo', methods=['POST'])
def companyinfo():
  cid = request.form['chocolate_id']
  cidcursor = g.conn.execute("SELECT company.company_id, company.company_name,company.company_country, company.phone_number, company.email FROM makes,company WHERE chocolate_id= %s and makes.company_id = company.company_id", cid)
  cinfos = []
  for result in cidcursor:
    cinfos.append(result)
  cidcursor.close()
  context = dict(companys= cinfos)
  if len(cinfos) > 0:
    return render_template("cinfo.html", **context)
  else:
    return render_template("no.html")

#1.5. updating db and print out what is updating
@app.route('/update', methods=['POST'])
def update():
  chocolateid = request.form['chocolate_id']
  reordern = request.form['number_to_reorder']
  if int(reordern) <= 0:
    r = "FALSE"
  else:
    r = "TRUE"
  reordercursor = g.conn.execute("UPDATE chocolate SET reorder = %s, number_to_reorder = %s WHERE chocolate_id = %s",r,reordern,chocolateid)
  reordercursor.close()
  updatecursor = g.conn.execute("SELECT chocolate_name, number_to_reorder, number_on_hand FROM chocolate WHERE chocolate_id = %s",chocolateid)
  updateinfo = []
  for result in updatecursor:
    updateinfo.append(', '.join(unicode(r) for r in result))
  updatecursor.close()
  context = dict(updates = updateinfo)
  if len(updateinfo) > 0:
    return render_template("update.html", **context)
  else:
    return render_template("no.html")

#2.1. Chocolate information for all chocolates of the selected type
@app.route('/typec', methods=['POST'])
def typec():
  kind = request.form['chtype']
  kcursor = g.conn.execute("SELECT * FROM chocolate WHERE type = %s", kind)
  entries = []
  for result in kcursor:
  	entries.append(', '.join(unicode(r) for r in result))
  kcursor.close()
  context = dict(typechoco = entries)
  if len(entries) > 0:
    return render_template("typec.html", **context)
  else:
    return render_template("no.html")

#2.2. Chocolate information for chocolates made with beans from this country
@app.route('/country', methods=['POST'])
def country():
  beancountry = request.form['bean_country']
  beancursor = g.conn.execute("SELECT c.chocolate_name, bs.bean_name, bs.bean_country \
    FROM blend bl INNER JOIN bean_source bs ON (bl.bean_id=bs.bean_id) \
    INNER JOIN chocolate c ON (c.chocolate_id=bl.chocolate_id) WHERE bs.bean_country=%s", beancountry)
  chocolateinfo = []
  for result in beancursor:
    chocolateinfo.append(', '.join(unicode(r) for r in result))
  beancursor.close()
  context = dict(chocos = chocolateinfo)
  if len(chocolateinfo) > 0:
    return render_template("country.html", **context)
  else:
    return render_template("no.html")
  
#3.1 Popularity of the chocolate
@app.route('/popular', methods=['POST'])
def popular():
  choiceone = request.form.get('chocolatep')
  choicetwo = request.form.get('chocolatenp')
 #print choiceone
  #print choicetwo
  if (choiceone == "popular" and choicetwo == "npopular"):
    bpopularcursor = g.conn.execute("SELECT i.chocolate_id, ch.chocolate_name, COUNT(i.chocolate_id) as inxorders \
                                          FROM item i INNER JOIN chocolate ch ON i.chocolate_id=ch.chocolate_id \
                                          GROUP BY i.chocolate_id, ch.chocolate_name \
                                          HAVING COUNT(i.chocolate_id)=(SELECT MAX(countc) \
                                           FROM (SELECT chocolate_id, count(chocolate_id) AS countc FROM item GROUP BY chocolate_id) AS a);")
    bpopular = []
    bpopular.append("The Most Popular one:  ")
    for result in bpopularcursor:
      bpopular.append(', '.join(unicode(r) for r in result))
    bpopularcursor.close()
    bpopularcursor = g.conn.execute("SELECT i.chocolate_id, ch.chocolate_name, COUNT(i.chocolate_id) as inxorders \
                                          FROM item i INNER JOIN chocolate ch ON i.chocolate_id=ch.chocolate_id \
                                          GROUP BY i.chocolate_id, ch.chocolate_name \
                                          HAVING COUNT(i.chocolate_id)=(SELECT MIN(countc) \
                                           FROM (SELECT chocolate_id, count(chocolate_id) AS countc FROM item GROUP BY chocolate_id) AS a);")
    bpopular.append("The Least Popular one: ")
    for result in bpopularcursor:
      bpopular.append(', '.join(unicode(r) for r in result))
    bpopularcursor.close()
    context = dict(cpopulars = bpopular)
    return render_template("bpopular.html", **context)
  else:
    if (choiceone is None and choicetwo is None):
      return render_template("noselection.html")
    else:
      if (choiceone == "popular" and choicetwo is None):
        popularcursor = g.conn.execute("SELECT i.chocolate_id, ch.chocolate_name, COUNT(i.chocolate_id) as inxorders \
                                          FROM item i INNER JOIN chocolate ch ON i.chocolate_id=ch.chocolate_id \
                                          GROUP BY i.chocolate_id, ch.chocolate_name \
                                          HAVING COUNT(i.chocolate_id)=(SELECT MAX(countc) \
                                           FROM (SELECT chocolate_id, count(chocolate_id) AS countc FROM item GROUP BY chocolate_id) AS a);")
        popular = []
        for result in popularcursor:
          popular.append(', '.join(unicode(r) for r in result))
        popularcursor.close()
        context = dict(populars = popular)
        return render_template("popular.html", **context)
      else:
        npopularcursor = g.conn.execute("SELECT i.chocolate_id, ch.chocolate_name, COUNT(i.chocolate_id) as inxorders \
                                          FROM item i INNER JOIN chocolate ch ON i.chocolate_id=ch.chocolate_id \
                                          GROUP BY i.chocolate_id, ch.chocolate_name \
                                          HAVING COUNT(i.chocolate_id)=(SELECT MIN(countc) \
                                           FROM (SELECT chocolate_id, count(chocolate_id) AS countc FROM item GROUP BY chocolate_id) AS a);")
        npopular = []
        for result in npopularcursor:
          npopular.append(', '.join(unicode(r) for r in result))
        npopularcursor.close()
        context = dict(npopulars = npopular)
        return render_template("npopular.html", **context)
    
    


#4.3. See orders made on a certain day
@app.route('/another', methods=['POST'])
def dorder():
  date = request.form['order_date']
  oondatecursor = g.conn.execute("SELECT order_number, order_date , order_price FROM orders WHERE order_date = %s",date)
  oondate = []
  for result in oondatecursor:
    oondate.append(', '.join(unicode(r) for r in result))
  oondatecursor.close()
  context = dict(todayorders = oondate)
  if len(oondate) > 0:
    return render_template("another.html", **context)
  else:
    return render_template("no.html")


#4.4. Find order by order number
@app.route('/orderinfo', methods=['POST'])
def orderinfo():
  onumber = request.form['order_number']
  onumcursor = g.conn.execute("SELECT order_number, order_date, method_of_delivery,date_of_delivery,date_delivery_completed,order_price,notes FROM orders WHERE order_number = %s", onumber)
  orders = []
  for result in onumcursor:
    orders.append(', '.join(unicode(r) for r in result))
  onumcursor.close()
  context = dict(specificorders= orders)
  if len(orders) > 0:
    return render_template("orderinfo.html", **context)
  else:
    return render_template("no.html")
  



@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
