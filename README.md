# py-site
A script for maintaining multple websites on a single python server

Install the script (ideally in /var/local/www).  Within the script, you can configure
the root directory by changing the root_dir variable.

Next to the script, add a 'sites.py' file containing the dictionary of sites supported by the
script.  An example is:

```python
sites = {
  "example.co.uk": "/example_co_uk",
  "myweb.site": "/website",
  "another.com": "/anothercom",
  "super.tv": "/super"
}
```

The subdirectories referred to by the dictionary should contain the static files for the
site (index.html and so on).  If the site requires some back end scripting, this can be put
into a file with the same name as the subdirectory, stored in the location of the main sites.py
file.  For instance, with the dictionary above, a file example_co_uk.py could be placed into the
root_dir, containing customisation for the example.co.uk domain.

The site.py script will register handlers for the domain, with and without a 'www.' prefix.

