from App import IpRange
from App.utils import ipv4_to_int, timed


def get_ip_location_from_ip(ip_address: str) -> (str, str):
    decimal_ip = ipv4_to_int(ip_address)
    ip_range = IpRange.objects(first_ip__lte=decimal_ip, last_ip__gte=decimal_ip).first()

    return ip_range.country_code, ip_range.country
