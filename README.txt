Pip Dependencies:
- Flask
- sklearn
- numpy

Recommendation: Use virtual environment

To initiate dev server:
> set FLASK_APP=app
> set FLASK_ENV=development
> python app.py

example routes:
    With No ML model Routes: 
        - "/countries"
        - "/countries?id=1"
        - "/"
    With ML model Routes:
        - "/test"
        - "/test?rooms=3"
        - "/test?landSize=100&bathroom=4"

sources: 
https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application
https://phoenixnap.com/kb/install-flask
https://realpython.com/api-integration-in-python/#flask
https://www.vantage-ai.com/blog/build-an-api-for-a-machine-learning-model-in-5-minutes-using-flask