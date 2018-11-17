from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os
import settings

app = Flask(__name__)
app.secret_key = os.urandom(24)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
subscription_key = os.getenv('SUBSCRIPTION_KEY')

authorization_base_url = 'https://partners-login.eliotbylegrand.com/authorize'
token_url = 'https://partners-login.eliotbylegrand.com/token'
redirect_uri = 'https://smarther.gallochri.com/callback'
api_version = 'v1.0'


@app.route('/')
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """

    legrand = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = legrand.authorization_url(authorization_base_url)
    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)

    # Step 2: User authorization, this happens on the provider.


@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """
    code = request.args.get('code')
    legrand = OAuth2Session(client_id)
    token = legrand.fetch_token(token_url, code=code, client_secret=client_secret)
    return jsonify(token)


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    # Run in DEBUG mode
    # app.run(debug=True)
    app.run()