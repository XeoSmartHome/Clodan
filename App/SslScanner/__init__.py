import datetime
import socket
import ssl

from App.Database.Models.ScanResult import ScanResult
from App.IpLocator import get_ip_location_from_ip


def ssl_scan(host_name: str):
    context = ssl.create_default_context()

    with socket.create_connection((host_name, 443)) as sock:
        ip_address = sock.getpeername()[0]
        is_secure = False
        protocol = None
        certificate = '{}'

        try:
            with context.wrap_socket(sock, server_hostname=host_name) as secure_socket:
                protocol = secure_socket.version()
                certificate = secure_socket.getpeercert()
                is_secure = True
        except socket.error as e:
            pass

    country_code, country = get_ip_location_from_ip(ip_address)

    return ScanResult(
        hostname=host_name,
        ip_address=ip_address,
        encrypted_connection=is_secure,
        protocol=protocol,
        certificate=certificate,
        timestamp=datetime.datetime.now(),
        country_code=country_code,
        country=country
    )
