#!/usr/bin/env python3
"""
Returns the car's current location as a Google Maps URL.
Reads credentials from environment variables:
  BLUELINK_USERNAME, BLUELINK_PASSWORD, BLUELINK_PIN, BLUELINK_REGION, BLUELINK_BRAND
"""

import os
import sys
from hyundai_kia_connect_api import VehicleManager

# REGIONS: 1=Europe, 2=Canada, 3=USA, 4=China, 5=Australia, 6=India, 7=NZ, 8=Brazil
# BRANDS:  1=Hyundai, 2=Kia, 3=Genesis
REGION_MAP = {"EU": 1, "EUROPE": 1, "CA": 2, "CANADA": 2, "USA": 3}
BRAND_MAP = {"HYUNDAI": 1, "KIA": 2, "GENESIS": 3}


def parse_int_or_name(val: str, mapping: dict) -> int:
    if val.isdigit():
        return int(val)
    return mapping.get(val.upper(), 1)


def main():
    username = os.environ.get("BLUELINK_USERNAME")
    password = os.environ.get("BLUELINK_PASSWORD")
    pin = os.environ.get("BLUELINK_PIN")
    region = parse_int_or_name(os.environ.get("BLUELINK_REGION", "1"), REGION_MAP)
    brand = parse_int_or_name(os.environ.get("BLUELINK_BRAND", "1"), BRAND_MAP)

    if not all([username, password, pin]):
        print("Error: BLUELINK_USERNAME, BLUELINK_PASSWORD, and BLUELINK_PIN must be set", file=sys.stderr)
        sys.exit(1)

    # The EU API uses the refresh token in place of the password
    refresh_token = os.environ.get("BLUELINK_REFRESH_TOKEN", password)
    manager = VehicleManager(region=region, brand=brand, username=username, password=refresh_token, pin=pin)

    manager.check_and_refresh_token()
    manager.update_all_vehicles_with_cached_state()

    vehicle = list(manager.vehicles.values())[0]
    lat = vehicle.location_latitude
    lng = vehicle.location_longitude
    name = vehicle.name or "Car"

    if lat is None or lng is None:
        print(f"{name}: location unavailable (GPS may be off or vehicle in garage)")
        sys.exit(0)

    maps_url = f"https://maps.google.com/?q={lat},{lng}"
    print(f"{name}: {maps_url}")


if __name__ == "__main__":
    main()
