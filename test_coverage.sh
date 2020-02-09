coverage run --source='.' manage.py test

coverage report --omit="okkindred/secrets.py"

coverage html -d ../reporting/okkindred_dev/coverage_html