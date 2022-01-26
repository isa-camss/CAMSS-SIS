import cfg.ctt as ctt
from flask import Flask, redirect
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from apis.api_microservices import blueprint as api


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

swagger_url = ctt.END_POINT_SWAGGER
swagger_ui_api_text = get_swaggerui_blueprint(base_url=swagger_url,
                                              api_url=ctt.END_POINT_SWAGGER_JSON,
                                              blueprint_name=ctt.NAME_BLUEPRINT)

app.register_blueprint(api)
app.register_blueprint(swagger_ui_api_text, url_prefix=swagger_url)

CORS(app)


@app.route("/")
def starting_url():
    return redirect(f"{ctt.API_PREFIX}")
