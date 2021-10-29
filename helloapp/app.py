"""
    This is the main file for the API.
"""
# Imports
import logging
from datetime import datetime
from os import getenv

from flask import Flask, request

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database initialization
MONGO_URI = getenv("MONGO_URI")

# By default, the collection and database names will be the similar to the module name
MONGO_DATABASE = getenv("MONGO_COLLECTION", "helloapp")
MONGO_COLLECTION = getenv("MONGO_COLLECTION", "helloapp")

DATE_FORMAT = "%Y-%m-%d"

"""
In case if you want to use a different database, you can do it like this:
 - Pass the MONGO_URI variable to connect to the real Mongo DB
 - Leave it empty to connect to the local Mongo DB (in case if you want to test the API)
"""
if not MONGO_URI:
    from mongita import MongitaClientDisk

    logger.warning(
        "!!!APPLICATION WILL WRITE EVERYTHING TO THE LOCAL DISK\n"
        "PLEASE, USE 'MONGO_URI' TO STORE IN PERSISTENT BASE!!!"
    )

    client = MongitaClientDisk(host="/tmp/helloapp")
else:
    from pymongo import MongoClient

    client = MongoClient(MONGO_URI)

# App initialization
app = Flask(__name__)
# Database initialization
db = client.MONGO_DATABASE.MONGO_COLLECTION


def is_valid_date_format(date, format=DATE_FORMAT):
    """
        This function will check if the date is in the correct format.
    :param date:
    :param format:
    :return:
    """
    try:
        return datetime.strptime(date, format)
    except (ValueError, TypeError) as e:
        logger.exception(e)
        return False


@app.route("/hello/<username>", methods=["PUT"])
def store(username):
    """
        This endpoint will store the data in the database.
    :param username:
    :return:
    """
    data = request.get_json()

    if "dateOfBirth" not in data:
        return "Missing 'dateOfBirth'", 400

    if not is_valid_date_format(data.get("dateOfBirth")):
        return "Invalid 'dateOfBirth' format", 400

    if not db.find_one({"username": username}):
        db.insert_one({"username": username, "dateOfBirth": data.get("dateOfBirth")})
        return "", 204
    else:
        return f"You already have a date of birth stored for current user.", 400


def parse_date(date):
    """
        This function will parse the date.
    :param date:
    :return:
    """
    return datetime.strptime(date, DATE_FORMAT)


@app.route("/hello/<username>", methods=["GET"])
def retrieve(username):
    """
        This endpoint will retrieve the data from the database.
    :param username:
    :return:
    """
    data = db.find_one({"username": username})
    if not data:
        return f"You didn't have a date of birth stored for current user.", 400

    # Calculate the age
    dd = (datetime.now() - parse_date(data.get("dateOfBirth"))).days

    if dd == 0:
        message = "Happy Birthday!"
    else:
        message = f"Your birthday is in {dd} day(s)!"

    return f'{{"message": "Hello, {username}! {message}"}}', 200


@app.route("/ping", methods=["GET"])
def ping():
    """
        This endpoint will return a pong message.
    :return:
    """
    return "ok"


if __name__ == "__main__":
    app.run(port=80, debug=False, )

