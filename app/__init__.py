from flask import Flask
from app.config import Config
from app.database import db
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


swagger = Swagger(app, template={
    "info": {
        "title": "User API",
        "version": "0.01"
    },
})

from app.user import controller
