from flask import Flask,request, render_template, g, redirect, Response,jsonify, make_response, current_app
import os,csv, random
from collections import *
from sqlalchemy import *
from sqlalchemy.pool import NullPool
import traceback
from functools import update_wrapper
from datetime import timedelta

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
public_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=tmpl_dir, static_folder=public_dir,static_url_path='')

#connect to database

# host = "104.196.175.120" 
# password =
# user =  
# DATABASEURI = "postgresql://%s:%s@%s/postgres" % (user, password, host)
movie_meta = {}
genre_hash = defaultdict(lambda: [])
# defaultdict(lambda: [None, None, []])

# engine = create_engine(DATABASEURI)
# import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# @app.before_request
# def before_request():
#   """
#   This function is run at the beginning of every web request
#   (every time you enter an address in the web browser).
#   We use it to setup a database connection that can be used throughout the request
#   The variable g is globally accessible
#   """
#   try:
#         g.conn = engine.connect()
#   except:
#         print "uh oh, problem connecting to database"
#         traceback.print_exc()
#         g.conn = None

# @app.teardown_request
# def teardown_request(exception):
#   """
#   At the end of the web request, this makes sure to close the database connection.
#   If you don't the database could run out of memory!
#   """
#   try:
#     g.conn.close()
#   except Exception:
#     pass
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
@app.route('/insertM')
def insertM():

  # print to_id,from_id
  # with open(public_dir+'/vc.csv', 'rb') as csvfile:
  #   spamreader = csv.reader(csvfile, delimiter=',')

  #   cat ={}
  #   for row in spamreader:
  #     ct=0
  #     print row
  #     for e in row:
  #       if len(e)>0: ct+=1
  #     if ct == len(row):
  #       try:
  #          g.conn.execute("INSERT into movie values (%s,%s,%s,%s)",row[0],row[1],row[2],row[3])
  #       except Exception as e:
  #         print e
  #       try:
  #         try:
  #           cursor =  g.conn.execute("select tid from tags where TNAME=%s;",row[4])
  #           tid = cursor.fetchone()[0]
  #         except:
  #           cursor = g.conn.execute("INSERT into tags(TNAME) values (%s); select max(tid) from tags;",row[4])
  #           tid = cursor.fetchone()[0]

  #         g.conn.execute("INSERT into movie_tag(mid,tid) values(%s,%s);",row[0],tid)
  #       except Exception as e:
  #         print e
  # g.conn.execute("INSERT into msg values (%s,%s,%s,%s)",int(time.time()),from_id,to_id,text)

  return jsonify(data="ok")


@app.route('/getmid', methods=['GET'])
@crossdomain(origin='*')
def getmid():
  uid = request.args.get('uid', 0, type=int)
  mid = request.args.get('mid', "", type=str)
  # print uid, mid
  data={}
  try: 
    data["mid"]=mid
    data["name"]=movie_meta[mid][2]
    data["mlink"]=movie_meta[mid][5]
    data["mimg"]=movie_meta[mid][1]


    ret =[]
    #skip now playing
    total_id = movie_meta.keys()
    total_id.remove(mid)
    #call by value
    same_genre_ids =list(genre_hash[movie_meta[mid][0]])
    same_genre_ids.remove(mid) 
    keep_genre_id = random.choice(same_genre_ids)
    total_id.remove(keep_genre_id)

    in_data={}
    in_data["mid"]=keep_genre_id
    in_data["name"]=movie_meta[keep_genre_id][2]
    in_data["mlink"]=movie_meta[keep_genre_id][5]
    in_data["mimg"]=movie_meta[keep_genre_id][1]
    ret.append(in_data)


    # sample not playing
    for k in random.sample(total_id, 4):
      in_data={}
      in_data["mid"]=k 
      in_data["name"]=movie_meta[k][2]
      in_data["mlink"]=movie_meta[k][5]
      in_data["mimg"]=movie_meta[k][1]
      ret.append(in_data)
  except Exception as e:
         print e
  # try:
  #   ret =[]
  #   cursor = g.conn.execute("select movie.*,movie_tag.tid from movie_tag, movie where movie.mid=movie_tag.mid and movie.mid <> %s and movie_tag.tid in (select tid from movie_tag as t where t.mid=%s)",mid,mid)
  #   for result in cursor:
  #     in_data={}
  #     in_data["mid"]=result["mid"]
  #     in_data["name"]=result["name"]
  #     in_data["mlink"]=result["mlink"]
  #     in_data["mimg"]=result["mimg"]
  #     tid = result["tid"]
  #     ret.append(in_data)
  # except Exception as e:
  #         print e
  
  # try:
  #   cursor = g.conn.execute("select movie.* from movie_tag, movie where movie.mid=movie_tag.mid and movie_tag.tid <> %s order by random() limit 2",tid)
  #   for result in cursor:
  #     in_data={}
  #     in_data["mid"]=result["mid"]
  #     in_data["name"]=result["name"]
  #     in_data["mlink"]=result["mlink"]
  #     in_data["mimg"]=result["mimg"]
  #     ret.append(in_data)
  # except Exception as e:
  #         print e
  
  data["rec_list"] = ret

  return jsonify(data=data)


@app.route('/')
def home():
    data={}
    try:
      # cursor = g.conn.execute("select mid from movie order by random() limit 1 ")
      data["mid"] = random.choice(movie_meta.keys())
    except Exception as e:
          print e   

    # print data
    return render_template('home.html',key=data)



if __name__ == '__main__':
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using

            python server.py

        Show the help text using

            python server.py --help

        """
        HOST, PORT = host, port
        print "running on %s:%d" % (HOST, PORT)
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
   
    with open(public_dir+'/joined.csv', 'rb') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',')
      for row in spamreader:
          mid = row.pop(-1)
          movie_meta[mid]=row
          genre_hash[row[0]].append(mid) 
          
    # print movie_meta
    run()
