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
Here are instructions to get this project running on `PythonAnywhere <https://www.PythonAnywhere.com/>`_ 

1. Sign up to `Google Maps Geocoding API <https://developers.google.com/maps/documentation/geocoding/start>`_  service and `Bing Maps API <https://www.microsoft.com/maps/>`_ service and make a note of their API keys.

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

9. Create a copy of the file ``~/okKindred/okkindred/secrets_example.py`` as ``~/okKindred/okkindred/secrets.py`` and edit the file with the AWS, Google API, Bing API details and database settings

10. In the PythonAnyWhere console run the following command to create the database:

 ``python manage.py migrate``

12. Follow instructions on PythonAnyWhere to set up your Web app and WSGI file https://help.pythonanywhere.com/pages/DeployExistingDjangoProject using the virtualenv we have just set up


Code Sections Overview
----------------------

okkindred
~~~~~~~~~~

This is the core Django created app that contains the settings and wsgi config

custom_user
~~~~~~~~~~~

A Django app to customize the user model, so that the Django username is an email address

family_tree
~~~~~~~~~~~

Django app that contains the key models to build a family tree:

- family: this defines a family.  Currently every person, user and picture has a single family.

- person: this is a profile and a node on the family tree

- relation: defines how a person is related to another person.  

 Designed to be as simple and inclusive as possible, the only types of relations can be 
 ``partnered`` which encompasses married/divorced/cohabiting etc... and ``raised`` which encompasses given birth to/adopted etc...  These terms are difficult to 
 translate cross culturally.  Note that the relation ``raised by`` resolves to ``raised`` and inverts when saved.

gallery
~~~~~~~

Django app that provides galleries, images and image tagging functionality

emailer
~~~~~~~

Django app to email out a summary of all the changes to family tree (if any) that have happened in the last 24 hours to every user in the family.  
So will in effect inform users by email of any new family members or changes to any existing profiles within a 24 hour period.  
The app also tries to send out the emails over a time to avoid traffic spikes.  This probably needs to use a message queue in the future!

email_confirmation
~~~~~~~~~~~~~~~~~~

Django app that handles inviting members of your family to become users and collaborate on the family tree.  It handles converting a person to a user.

maps
~~~~

Django app that handles displaying the map view for family members.  Note `MapBox <https://www.mapbox.com/> _ is used to display the maps as Google Maps isn't available in China over https.

sign_up
~~~~~~~

Django app that allows new users to sign up to the service

schedule
~~~~~~~~

Shell files that can be called by system scheduled tasks that trigger off various different things in the project


Javascript/UI Overview
----------------------

The initial idea of the project was to use only small amounts of JavaScript and render as much on the server as possible to enable a good experience on lower end mobile browsers.
However as the project grew, this made the user experience poor.  At some point the UI probably needs a major overhaul!

The js files are located in ``static\js``

Asynchronous Module Definition 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`require.js <http://requirejs.org/>`_ is used to implement the Asynchronous Module Definition (AMD) pattern in order to tame some of the js that got everywhere.

Note in ``static\js\common.js`` we also use multiple CDNs because certain CDNs are blocked in different parts of China on different das of the week.

Bootstrap/JQuery/Bower
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The UI is primarily driven by Bootstrap and JQuery and Bower is used as a package manager (yes I know!) ``static\js\libs``


Mapping
~~~~~~~

Mapping is provided by `MapBox <https://www.mapbox.com/>`_ .  This was chosen as it is available in China over an https connection.  

This is used in conjunction with `LeafletJS <http://leafletjs.com/>`_ .
