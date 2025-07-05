#!/usr/bin/env python3  # noqa: E265
import os
import argparse
import logging
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
from requests.adapters import HTTPAdapter, Retry
from dotenv import load_dotenv

load_dotenv()
OPENCAGE_KEY: Optional[str] = os.getenv("OPENCAGE_KEY")

IP_API_URL = "https://ipapi.co/{ip}/json/"
GEOCODE_API_URL = "https://api.opencagedata.com/geocode/v1/json"

# Configure logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def get_session(timeout: int, retries: int) -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    original_request = session.request

    def timed_request(method: str, url: str, **kwargs) -> requests.Response:
        return original_request(method, url, timeout=timeout, **kwargs)

    session.request = timed_request
    return session


def enrich_ip(
    ip: str,
    timeout: int,
    retries: int,
) -> Dict[str, Any]:
    """Fetch geo data for an IP address."""
    session = get_session(timeout, retries)
    url = IP_API_URL.format(ip=ip)
    logger.debug(f"Requesting IP data: {url}")
    r = session.get(url)
    r.raise_for_status()
    d = r.json()
    return {
        "ip_country": d.get("country_name"),
        "ip_region": d.get("region"),
        "ip_city": d.get("city"),
        "ip_lat": d.get("latitude"),
        "ip_lng": d.get("longitude"),
    }


def enrich_coords(
    lat: float,
    lng: float,
    timeout: int,
    retries: int,
) -> Dict[str, Any]:
    """Fetch reverse-geocode for latitude/longitude pair."""
    if not OPENCAGE_KEY:
        logger.error("OPENCAGE_KEY is not set in environment")
        raise RuntimeError("Missing OpenCage API key")
    session = get_session(timeout, retries)
    params = {
        "q": f"{lat},{lng}",
        "key": OPENCAGE_KEY,
        "limit": 1,
        "no_annotations": 1,
    }
    logger.debug(f"Requesting coords data: {params}")
    r = session.get(GEOCODE_API_URL, params=params)
    r.raise_for_status()
    results = r.json().get("results", [])
    if not results:
        logger.warning(f"No geocode result for {lat},{lng}")
        return {}
    res = results[0]
    comp = res.get("components", {})
    geom = res.get("geometry", {})
    return {
        "geo_country": comp.get("country"),
        "geo_state": comp.get("state"),
        "geo_city": comp.get("city") or comp.get("town"),
        "geo_lat": geom.get("lat"),
        "geo_lng": geom.get("lng"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enrich a CSV of IPs or lat/lng with geographic data."
    )
    parser.add_argument("input", help="Path to input CSV file")
    parser.add_argument("output", help="Path to output enriched CSV")
    parser.add_argument("--ip-col", default="ip", help="Column name for IP addresses")
    parser.add_argument(
        "--coord-cols", default="lat,lng", help="Comma-separated latitude,column names"
    )
    parser.add_argument(
        "--timeout", type=int, default=5, help="HTTP timeout in seconds"
    )
    parser.add_argument("--retries", type=int, default=2, help="Number of HTTP retries")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    logger.info("Starting geoenrich...")

    df = pd.read_csv(args.input)
    results: List[Dict[str, Any]] = []

    if args.ip_col in df.columns:
        for ip in df[args.ip_col].dropna().astype(str):
            results.append(enrich_ip(ip, args.timeout, args.retries))
    else:
        lat_col, lng_col = args.coord_cols.split(",")
        for lat, lng in df[[lat_col, lng_col]].dropna().itertuples(index=False):
            results.append(enrich_coords(lat, lng, args.timeout, args.retries))

    geo_df = pd.DataFrame(results)
    out_df = pd.concat([df.reset_index(drop=True), geo_df], axis=1)
    out_df.to_csv(args.output, index=False)
    logger.info(f"Enriched {len(df)} rows → {args.output}")


if __name__ == "__main__":
    main()
