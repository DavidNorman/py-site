import cherrypy
import json
import os

# Load the site mapping dictionary
import sites

# The location of the script and site directories
root_dir = "/var/local/www"

# A class for the root
class Root:
  @cherrypy.expose
  def index(self):
    return "Site not recognised"

# Security headers for all HTTP responses
def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"

# Create a root application and mount
root = Root()

# Set up server bindings
cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 80 })

# Add site aliases (www)
site_dispatch = {}
for s in sites.sites:
  site_dispatch[s] = sites.sites[s]
  site_dispatch['www.' + s] = sites.sites[s]

# Basic root level configuration
conf = {
  "/": {
    "request.dispatch": cherrypy.dispatch.VirtualHost(**site_dispatch),
    "tools.sessions.on": True,
    #"tools.sessions.secure": True,
    "tools.sessions.httponly": True,
    "tools.secureheaders.on": True,
  }
}

# Process site specific details
for key in site_dispatch:
  path = site_dispatch[key]

  # Add static directory config
  conf[path] = {
    "tools.staticdir.on": True,
    "tools.staticdir.index": "index.html",
    "tools.staticdir.dir": root_dir + path
  }

  # Add site specific application is one exists
  site_module = path[1:]
  if os.path.exists(site_module + '.py'):
    mod = __import__(site_module)
    setattr(root, path[1:], mod.Site())

# Apply the secure headers finalize hook
cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize', secureheaders, priority=60)

# Start the service
cherrypy.quickstart(root, "/", conf)

