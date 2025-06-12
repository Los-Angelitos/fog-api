from flask import Blueprint, request, jsonify

from operations_and_monitoring.application.services import MonitoringService

monitoring_api = Blueprint('monitoring_api', __name__)
monitoring_service = MonitoringService()

@monitoring_api.route('/monitoring/devices', methods=['GET'])
def get_devices():
    try:
        thermostats = monitoring_service.get_thermostats()
        smoke_sensors = monitoring_service.get_smoke_sensors()

        devices = {
            "thermostats": [thermostat.to_dict() for thermostat in thermostats],
            "smoke_sensors": [smoke_sensor.to_dict() for smoke_sensor in smoke_sensors]
        }
        return jsonify(devices), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@monitoring_api.route('/monitoring/devices/thermostats', methods=['POST'])
def add_thermostat():
    try:
        data = request.json
        thermostat = monitoring_service.add_thermostat(data)
        return jsonify(thermostat.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@monitoring_api.route('/monitoring/devices/smoke_sensors', methods=['POST'])
def add_smoke_sensor():
    try:
        data = request.json
        smoke_sensor = monitoring_service.add_smoke_sensor(data)
        return jsonify(smoke_sensor.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
