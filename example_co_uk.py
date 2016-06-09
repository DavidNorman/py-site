# This is an example of how to extend the functionality of a website
# with a cherrypy handler class

import cherrypy
import json
import uuid
import random

class Site:

    @cherrypy.expose
    def randomnum(self):
        raise cherrypy.HTTPRedirect("/random")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def random(self):
      out = {
        'uuid' : uuid.uuid1().hex,
        'random' : random.randint(0, 100)
      }
      return out

