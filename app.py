from communication.website.website import app
from config import oauth_secret
app.config['SECRET_KEY'] = oauth_secret

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,threaded=True)
