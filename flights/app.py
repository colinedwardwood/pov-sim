from flasgger import Swagger
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import get_random_int
import logging

# OpenTelemetry imports
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry import _logs
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
import os

app = Flask(__name__)
Swagger(app)
CORS(app)

# Configure OpenTelemetry logging
_logs.set_logger_provider(LoggerProvider())
otlp_exporter = OTLPLogExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://alloy:4318") + "/v1/logs"
)
_logs.get_logger_provider().add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))
handler = LoggingHandler(level=logging.NOTSET, logger_provider=_logs.get_logger_provider())

# Configure logging
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)

# Enable logging instrumentation
LoggingInstrumentor().instrument(set_logging_format=True)

@app.route('/health', methods=['GET'])
def health():
    """Health endpoint
    ---
    responses:
      200:
        description: Returns healthy
    """
    logger.info("Health check endpoint called")
    return jsonify({"status": "healthy"}), 200

@app.route("/", methods=['GET'])
def home():
    """No-op home endpoint
    ---
    responses:
      200:
        description: Returns ok
    """
    logger.info("Home endpoint called")
    return jsonify({"message": "ok"}), 200

@app.route("/flights/<airline>", methods=["GET"])
def get_flights(airline):
    """Get flights endpoint. Optionally, set raise to trigger an exception.
    ---
    parameters:
      - name: airline
        in: path
        type: string
        enum: ["AA", "UA", "DL"]
        required: true
      - name: raise
        in: query
        type: str
        enum: ["500"]
        required: false
    responses:
      200:
        description: Returns a list of flights for the selected airline
    """
    status_code = request.args.get("raise")
    logger.info("Get flights endpoint called for airline=%s, raise=%s", airline, status_code)
    if status_code:
      logger.error("Exception intentionally raised in flights endpoint for airline=%s", airline)
      raise Exception(f"Encountered {status_code} error") # pylint: disable=broad-exception-raised
    random_int = get_random_int(100, 999)
    logger.info("Returning flight %s for airline %s", random_int, airline)
    return jsonify({airline: [random_int]}), 200

@app.route("/flight", methods=["POST"])
def book_flight():
    """Book flights endpoint. Optionally, set raise to trigger an exception.
    ---
    parameters:
      - name: passenger_name
        in: query
        type: string
        enum: ["John Doe", "Jane Doe"]
        required: true
      - name: flight_num
        in: query
        type: string
        enum: ["101", "202", "303", "404", "505", "606"]
        required: true
      - name: raise
        in: query
        type: str
        enum: ["500"]
        required: false
    responses:
      200:
        description: Booked a flight for the selected passenger and flight_num
    """
    passenger_name = request.args.get("passenger_name")
    flight_num = request.args.get("flight_num")
    status_code = request.args.get("raise")
    logger.info("Book flight endpoint called for passenger=%s, flight_num=%s, raise=%s", passenger_name, flight_num, status_code)
    if status_code:
      logger.error("Exception intentionally raised in book flight endpoint for passenger=%s", passenger_name)
      raise Exception(f"Encountered {status_code} error") # pylint: disable=broad-exception-raised
    booking_id = get_random_int(100, 999)
    logger.info("Booked flight %s for passenger %s with booking_id %s", flight_num, passenger_name, booking_id)
    return jsonify({"passenger_name": passenger_name, "flight_num": flight_num, "booking_id": booking_id}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)
