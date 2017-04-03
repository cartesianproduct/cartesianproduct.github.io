# import pandas as pd
# import json
# import requests
# import re
# from nltk.corpus import stopwords
# from nltk.stem.porter import PorterStemmer
# import os
from flask import Flask, render_template
# stopwords = set(stopwords.words("english"))
# stemmer = PorterStemmer()
# from watson_developer_cloud import AuthorizationV1 as WatsonAuthorization
# from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage
# alchemy = AlchemyLanguage(api_key=os.environ.get("ALCHEMY_API_KEY"))




app = Flask(__name__, static_url_path="/static", static_folder="static")

@app.route("/")
def index():
    # day_rank, words = get_value_and_words('20070130')
    day_rank = 10
    # return app.send_static_file("index.html")
    return render_template('index.html', result = day_rank)
    # return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(debug=True)
    # app.debug = True
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
