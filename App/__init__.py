import datetime

from flask import Flask, request, jsonify
from .Database import db
from .Database.Models.IpRange import IpRange
import csv

from .Database.Models.ScanResult import ScanResult
from .SslScanner import ssl_scan
from .utils import timed

app = Flask(__name__)


def init_app():
    db.init_app(app)


@app.get('/')
def _handle_index():
    return 'Hello from Clodan'


@app.get('/scan')
@timed
def _handle_scan():
    start = datetime.datetime.now()
    hostname = request.args['hostname']

    cached_scan_result: ScanResult
    cached_scan_result = ScanResult.objects(hostname=hostname).first()

    if cached_scan_result is not None and datetime.datetime.now() - cached_scan_result.timestamp < datetime.timedelta(seconds=60):
        return jsonify({
            **cached_scan_result.to_dict(),
            'fresh': False
        })

    try:
        scan_result = ssl_scan(host_name=hostname)
    except Exception as e:
        return {
                   'error': {
                       'type': 'ScanError',
                       'message': str(e)
                   }
               }, 400

    if cached_scan_result is None:
        scan_result.save()
    else:
        cached_scan_result.protocol = scan_result.protocol
        cached_scan_result.certificate = scan_result.certificate
        cached_scan_result.timestamp = scan_result.timestamp
        cached_scan_result.save()

    return jsonify({
        **scan_result.to_dict(),
        'fresh': True,
    })


@app.get('/load-ip-locations')
def _handle_load_ip_locations():
    with open(app.config['IP_LOCATIONS_FILE']) as csv_file:
        csv_stream = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in csv_stream:
            [first_ip, last_ip, country_code, country] = row
            new_ip_range = IpRange(first_ip=first_ip, last_ip=last_ip, country_code=country_code, country=country)
            new_ip_range.save()

    return 'Ip locations loaded'
