"""
Web frontend to gitmarks for use as a bookmarklet:

javascript:(function(){void(open('http://localhost:44865/new?url='+window.location,'gitmark','resizable,scrollbars,width=250,height=250'))})();
"""

import bottle
bottle.debug(False)

from bottle import route, run, request, response, template
from gitmark import gitMark
import settings

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

run(host="localhost", port=settings.GITMARKS_WEB_PORT, reloader=False)
