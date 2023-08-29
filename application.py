import os
import uuid
import jwt
import datetime
from flask import Flask
from flask_cors import cross_origin
from dotenv import load_dotenv

load_dotenv()
application = Flask(__name__)


@application.route('/token', methods=['GET'])
@cross_origin()
def token():
    connected_app_client_id = os.environ.get("APP_CLIENT_ID")
    connected_app_secret_id = os.environ.get("APP_SECRET_ID")
    connected_app_secret_key = os.environ.get("APP_SECRET_KEY")
    user_name = os.environ.get("USER_NAME")

    current_time = datetime.datetime.now()
    expiration_time = current_time + datetime.timedelta(minutes=5)

    data = {
        "sub": user_name,
        "aud": "tableau",
        "scp": [
            "tableau:views:embed",
            "tableau:views:embed_authoring",
            "tableau:metrics:embed"
        ],
        "exp": int(expiration_time.timestamp()),
        "jti": str(uuid.uuid4())
    }

    header = {
        "alg": "HS256",
        "typ": "JWT",
        "iss": connected_app_client_id,
        "kid": connected_app_secret_id
    }

    payload = jwt.encode(payload=data, key=connected_app_secret_key, algorithm="HS256", headers=header)
    return payload


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8000, debug=True)

