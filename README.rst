ok!Kindred
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
The project is built using `Python Django <https://www.djangoproject.com/>`_ running on Python3.5

https://www.okkindred.com is hosted with `PythonAnywhere <https://www.PythonAnywhere.com/>`_  

It also uses `Amazon Web Services S3 <https://aws.amazon.com/s3/>`_  to store potentially a huge number of images for very little cost. 

It also uses `Google Maps Geocoding API <https://developers.google.com/maps/documentation/geocoding/start>`_ and `Bing Maps API <https://www.microsoft.com/maps/>`_ to geolocate addresses
so that it can plot where your family is on a map.



How To Deploy Your Own Instance
-------------------------------
Here are instructions to get it running on `PythonAnywhere <https://www.PythonAnywhere.com/>`_ 

1. Sign up to `Google Maps Geocoding API <https://developers.google.com/maps/documentation/geocoding/start>`_ and `Bing Maps API <https://www.microsoft.com/maps/>`_ and make a note of their API keys.

 Bing is optional, it is used as the backup geocoding service if a location can't be found using Google. 

2. Sign up to `Amazon Web Services S3 <https://aws.amazon.com/s3/>`_ and create a new bucket.  Make the bucket publically readable but not listable.  

 You may need to specify the bucket policy manually ::

    {
    "Version": "2017-01-01",
	"Statement": [
        {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::BUCKETNAME/*"
            }
        ]
    }



3. Create an AWS user with access to S3 and create an external Access Key ID and Secret Key  for the user.  Note this down for later.

4. Sign up with `PythonAnywhere <https://www.PythonAnywhere.com/>`_  

5. Create two new databases on PythonAnywhere, one for live and one to run the tests against.  Make a note of their login details.  MySQL and Postgres should both work however, MySQL is free!

6. In PythonAnywhere, create the AWS credential file ``~/.aws/credentials``::

    [default]
    aws_access_key_id = YOUR_ACCESS_KEY
    aws_secret_access_key = YOUR_SECRET_KEY

    [default]
    region=us-east-1

7. In PythonAnywhere, open the console and clone this repository 
  
 ``git clone https://github.com/JustinWingChungHui/okKindred.git``

8. Change to the directory of the repository, create a virtualenv and install all the Python requirements: 

 ``cd okKindred``

 ``mkvirtualenv YOURVIRTUALENVNAME --python=/usr/bin/python3.5``

 ``pip install -r requirements.txt``

9. Create a copy of the file ``~/okKindred/familyroot/secrets_example.py`` as ``~/okKindred/familyroot/secrets.py`` and edit the file with the AWS, Google API, Bing API details and database settings

10. In the PythonAnyWhere console run the following commands 

 ``python manage.py migrate``

 ``python manage.py collectstatic``

11. Follow instructions on PythonAnyWhere to set up your Web app and WSGI file https://help.pythonanywhere.com/pages/DeployExistingDjangoProject


Code Sections Overview
----------------------

familyroot
custom_user
family_tree
gallery
emailer
email_confirmation
mapssign_up

schedule


Javascript Overview
-------------------
require.js
jquery
bower
