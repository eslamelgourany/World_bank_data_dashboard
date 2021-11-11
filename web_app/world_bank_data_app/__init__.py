from flask import Flask

app = Flask(__name__)

from world_bank_data_app import routes
