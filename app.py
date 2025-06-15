from flask import Flask
from flasgger import Swagger
from iam.infrastructure.routes import iam as iam_routes
from inventory.interfaces.services import supply_api, supply_request_api, rfid_api
from operations_and_monitoring.interfaces.services import monitoring_api as monitoring_routes
from operations_and_monitoring.interfaces.services import operations_api as operations_routes

from shared.infrastructure.database import db

# creating the tables in the database
db.create_all()

app = Flask(__name__)

# Register the routes as blueprints, which allows for modular organization of the application
app.register_blueprint(iam_routes, url_prefix='/api/v1', name='iam')
app.register_blueprint(supply_api, name='SupplyAPI')
app.register_blueprint(supply_request_api, name='SupplyRequestAPI')
app.register_blueprint(rfid_api, name='RfidAPI')  # Nueva línea agregad
app.register_blueprint(monitoring_routes, url_prefix='/api/v1', name='monitoring')
app.register_blueprint(operations_routes, url_prefix='/api/v1', name='operations')

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "SweetManager IoT Fog API",
        "description": "API Restful for managing IoT devices in the SweetManager system.",
        "version": "1.0.0",
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    }}
)

@app.route("/routes")
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    return {"routes": routes}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

