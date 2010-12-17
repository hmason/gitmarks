"""
Web frontend to gitmarks for use as a bookmarklet:

javascript:(function(){void(open('http://localhost:8080/new?url='+window.location,'gitmark','resizable,scrollbars,width=250,height=250'))})();
"""

import bottle
bottle.debug(True)

from bottle import route, run, request, response, template
from gitmark import gitMark

@route("/new")
def new():
  url = request.GET.get('url')

  return template("new", url=url, tags=None, message=None, error=None)

@route("/create", method = "POST")
def create():
  url     = request.forms.get('url', '').strip()
  tags    = request.forms.get('tags', '').strip()
  message = request.forms.get('message', '').strip()
  push    = False if (request.forms.get('nopush', '').strip() == '1') else True

  if url == "":
    return template("new", url=url, tags=tags, message=message, error="URL is required")

  else:
    options = {}
    options['tags'] = tags
    options['push'] = push
    options['msg']  = message

    args = [url]

    g = gitMark(options, args)

    return template("create")

@route("/:name")
def index(name = "World"):
  hi = request.GET.get('hi')
  return "<b>Hello %s</b> (%s)" % (name, hi)

run(host="localhost", port="8080", reloader=True)
