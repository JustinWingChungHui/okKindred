#!/usr/bin/python2.4

import httplib, urllib, sys
# Define the parameters for the POST request and encode them in
# a URL-safe format.

params = urllib.urlencode([
    ('code_url', 'https://www.okkindred.com/static/js/jquery-1.11.2.min.js'),
    ('code_url', 'https://www.okkindred.com/static/js/bootstrap.min.js'),
    ('code_url', 'https://www.okkindred.com/static/js/jquery-ui.min.js'),
    ('code_url', 'https://www.okkindred.com/static/js/jquery.ui.touch-punch.min.js'),
    ('code_url', 'https://www.okkindred.com/static/js/jquery.jsPlumb-1.7.2-min.js'),
    #('code_url', 'https://www.okkindred.com/static/js/leaflet.js '), Disables mouse wheel scroll
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

with open("app.js", "w") as text_file:
    text_file.write(data)



params = urllib.urlencode([
    ('code_url', 'https://www.okkindred.com/static/js/jquery.iframe-transport.min.js'),
    ('code_url', 'https://www.okkindred.com/static/js/jquery.fileupload.min.js'),
    ('code_url', 'https://www.okkindred.com/static/js/jquery.cookie.js'),
    ('compilation_level', 'WHITESPACE_ONLY'),
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


with open("jquery.file_upload.compiled.js", "w") as text_file:
    text_file.write(data)
