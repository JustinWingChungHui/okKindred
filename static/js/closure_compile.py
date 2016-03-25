#!/usr/bin/python2.4

import httplib, urllib
# Define the parameters for the POST request and encode them in
# a URL-safe format.

params = urllib.urlencode([
    ('code_url', 'https://www.okkindred.com/static/js/jquery/jquery-2.1.4.min.js'),
    ('code_url', 'https://www.okkindred.com/static/js/bootstrap/bootstrap.min.js'),
    ('code_url', 'https://www.okkindred.com/static/js/mustache/mustache.min.js'),
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

# File Upload

params = urllib.urlencode([
    ('code_url', 'https://www.okkindred.com/static/js/jquery/jquery-ui.min.js'),
    ('code_url', 'https://www.okkindred.com/static/js/jquery/jquery.iframe-transport.min.js'),
    ('code_url', 'https://www.okkindred.com/static/js/jquery/jquery.fileupload.min.js'),
    ('code_url', 'https://www.okkindred.com/static/js/jquery/jquery.cookie.js'),
    ('code_url', 'https://www.okkindred.com/static/js/family_tree/profile_photo_upload.js'),
    ('code_url', 'https://www.okkindred.com/static/js/gallery/upload_images.js'),
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


with open("file_upload.min.js", "w") as text_file:
    text_file.write(data)


# Mapping

params = urllib.urlencode([
    ('code_url', 'https://www.okkindred.com/static/js/mapping/leaflet.js'),
    ('code_url', 'https://www.okkindred.com/static/js/mapping/person_map.js'),
    ('code_url', 'https://www.okkindred.com/static/js/mapping/image_map.js'),
    ('code_url', 'https://www.okkindred.com/static/js/mapping/gallery_map.js'),
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


with open("mapping.min.js", "w") as text_file:
    text_file.write(data)


# Editable tables
params = urllib.urlencode([
    ('code_url', 'https://www.okkindred.com/static/js/editable/moment.min.js'),
    ('code_url', 'https://www.okkindred.com/static/js/editable/validator.min.js'),
    ('code_url', 'https://www.okkindred.com/static/js/editable/bootstrap-editable.min.js'),
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


with open("editable.min.js", "w") as text_file:
    text_file.write(data)

# Tree App
params = urllib.urlencode([
    ('code_url', 'https://www.okkindred.com/static/js/family_tree/tree_app.js'),
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