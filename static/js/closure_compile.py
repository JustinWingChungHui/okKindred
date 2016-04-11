#!/usr/bin/python2.4

import httplib, urllib
# Define the parameters for the POST request and encode them in
# a URL-safe format.

domain = "https://justinhui.pythonanywhere.com"

# Tree App
params = urllib.urlencode([
    ('code_url', domain + '/static/js/family_tree/tree_app.js'),
    ('compilation_level', 'SIMPLE_OPTIMIZATIONS'),
    ('output_format', 'text'),
    ('output_info', 'compiled_code'),
  ])
# Always use the following value for the Content-type header.
headers = { "Content-type": "application/x-www-form-urlencoded" }
conn = httplib.HTTPConnection('closure-compiler.appspot.com')
conn.request('POST', '/compile', params, headers)
response = conn.getresponse()
data = response.read()
conn.close()

with open("family_tree/tree_app.min.js", "w") as text_file:
    text_file.write(data)

#Require js
params = urllib.urlencode([
    ('code_url', domain + '/static/js/libs/bower_components/requirejs/require.js'),
    ('compilation_level', 'SIMPLE_OPTIMIZATIONS'),
    ('output_format', 'text'),
    ('output_info', 'compiled_code'),
  ])
# Always use the following value for the Content-type header.
headers = { "Content-type": "application/x-www-form-urlencoded" }
conn = httplib.HTTPConnection('closure-compiler.appspot.com')
conn.request('POST', '/compile', params, headers)
response = conn.getresponse()
data = response.read()
conn.close()

with open("libs/bower_components/requirejs/require.min.js", "w") as text_file:
    text_file.write(data)