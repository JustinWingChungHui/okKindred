coverage run --source='.' manage.py test

coverage report --omit="familyroot/secrets.py"

coverage html -d ./coverage_html