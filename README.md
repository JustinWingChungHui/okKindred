okKindred
============

Collaborative Family Tree
-------------------------
Web app to track my family history using a family tree.

I have family across several continents, and this is a project to create a private web app to keep a history of who is who and where they are.

The idea of this app is to provide a collaborative multilingual family tree with some social networking features like photosharing and tagging.

You can sign up to the instance I run at https://www.okkindred.com
or you are welcome to clone this repository and set up your own instance.  

If you need help setting it up, drop me a message on info@okkindred.com 


If you have ideas or want to add to this, please feel free!


Architecture
------------
The project is built using `Python Django <https://www.djangoproject.com/>` running on Python3.5

https://www.okkindred.com is hosted with `PythonAnywhere <https://www.PythonAnywhere.com/>`  

It also uses `Amazon Web Services S3 <https://aws.amazon.com/s3/>`  to store potentially a huge number of images for very little cost. 

It also uses `Google Maps Geocoding API <https://developers.google.com/maps/documentation/geocoding/start>` and `Bing Maps API <https://www.microsoft.com/maps/>` to geolocate addresses
so that it can plot where your family is on a map.



How To Deploy
-------------
Here are instructions to get it running on PythonAnywhere

1. Sign up with `PythonAnywhere <https://www.PythonAnywhere.com/>`  

2. In PythonAnywhere, open the console and clone this repository
e.g. ``git clone https://github.com/YOURUSERNAME/okKindred.git``

3. Change to the directory of the repository, create a virtualenv and install all the Python requirements:
 ``cd okKindred``
 ``mkvirtualenv YOURVIRTUALENVNAME --python=/usr/bin/python3.5``
 ``pip install -r requirements.txt``

4. Create two new databases on PythonAnywhere, one for live and one to run the tests against.  Make a note of their login details.  MySQL and Postgres should both work however, MySQL is free!

5. Sign up to `Google Maps Geocoding API <https://developers.google.com/maps/documentation/geocoding/start>` and `Bing Maps API <https://www.microsoft.com/maps/>` and make a note of their API keys.

6. Sign up to `Amazon Web Services S3 <https://aws.amazon.com/s3/>` and create a new bucket.  Make the bucket publically readable but not listable.  

7. Create an AWS external Access ID and Secret


8. In the PythonAnyWhere console run the following commands
 ``python manage.py migrate``
 ``python manage.py collectstatic``
 
