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


  #
  # example of a database query
  #
##  cursor = g.conn.execute("SELECT name FROM test")
##  names = []
##  for result in cursor:
##    names.append(result['name'])  # can also be accessed using result[0]
##  cursor.close()


  
##
##  #1. Show the amount of number on hand based on one specific chocolate id
##  chocolateid = request.form.['chocolate_id']
##  ccursor = g.conn.execute("SELECT * FROM chocolate WHERE chocolate_id='%s'", chocolateid)
##  cname = []
##  for result in ccursor:
##    cname.append(result)
##  ccursor.close()
##
##  #2. The amount of number on hand less than 10
##  numbercursor = g.conn.execute("SELECT * FROM chocolate WHERE number_on_hand < 20")
##  cnames = []
##  for result in numbercursor:
##    cnames.append(result)
####    cnames.append(result['number_on_hand'])
##  numbercursor.close()
##
##  #3. find the company info of a chocolate by its id
##  cid = request.form.['chocolate_id']
##  cidcursor = g.conn.execute("SELECT * FROM makes WHERE chocolate_id='%s'", cid)
##  cinfos = []
##  for result in cidcursor:
##    cinfos.append(result)
##  cidcursor.close()
##
##  #4. combinational query
##  
## 
##  #5. updating... no idea how to update. 
##
##  #1. see chocolates of a certain type
##  kind = request.form.get(['type'])
##  if kind = 'Dark':
##  	kcursor = g.conn.execute("SELECT * FROM chocolate WHERE type = 'dark'")
##  elif kind = 'Milk':
##  	kcursor = g.conn.execute("SELECT * FROM chocolate WHERE type = 'milk'")
##  elif kind = 'White':
##   	kcursor = g.conn.execute("SELECT * FROM chocolate WHERE type = 'white'")
##  entries = []
##  for result in kcursor:
##  	entries.append(result)
##  kcursor.close()
##
##  #2. Find chocolate information based on specific bean country
##   beancountry = request.form.['bean_country']
##   beancursor = g.conn.execute("SELECT * FROM blend WHERE bean_country='%s'", beancountry)
##   chocolateinfo = []
##   for result in beancursor:
##     chocolateinfo.append(result)
##   beancursor.close()
  


  #1. show orders history
  allordercursor =  g.conn.execute("SELECT order_number, order_date , order_price FROM orders")
  allorders = []
  for result in allordercursor:
    allorders.append(', '.join(unicode(r) for r in result))
  allordercursor.close()

  #2. see incomplete orders
  incorderscursor = g.conn.execute("SELECT order_number, order_date, method_of_delivery, date_of_delivery FROM orders WHERE date_delivery_completed IS NOT NULL")
  incorders = []
  for result in incorderscursor:
    incorders.append(', '.join(unicode(r) for r in result))
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
  context = dict(orders = allorders, ordersnotc = incorders)


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

#3. see orders made on a certain day
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


####  #4. find order by order number
##@app.route('/orderinfo', methods=['POST'])
##def orderinfo():
##  onumber = request.form['order_number']
##  onumcursor = g.conn.execute("SELECT * FROM orders WHERE order_number = %d", onumber)
##  orders = []
##  for result in onumcursor:
##    orders.append(', '.join(unicode(r) for r in result))
##  onumcursor.close()
##  context = dict(specificorders= orders)
##  if len(orders) > 0:
##    return render_template("orderinfo.html", **context)
##  else:
##    return render_template("no.html")
  



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
