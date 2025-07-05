#!/usr/bin/env python3
import os, argparse, pandas as pd, requests
from dotenv import load_dotenv

load_dotenv()
OPENCAGE_KEY = os.getenv('OPENCAGE_KEY')
IP_API_URL = 'https://ipapi.co/{ip}/json/'
GEOCODE_API_URL = 'https://api.opencagedata.com/geocode/v1/json'

def enrich_ip(ip):
    r = requests.get(IP_API_URL.format(ip=ip), timeout=5)
    d = r.json()
    return {
        'ip_country': d.get('country_name'),
        'ip_region': d.get('region'),
        'ip_city': d.get('city'),
        'ip_lat': d.get('latitude'),
        'ip_lng': d.get('longitude'),
    }

def enrich_coords(lat, lng):
    params = {'q':f'{lat},{lng}','key':OPENCAGE_KEY,'limit':1,'no_annotations':1}
    r = requests.get(GEOCODE_API_URL, params=params, timeout=5)
    res = r.json().get('results', [{}])[0]
    comp = res.get('components', {})
    return {
        'geo_country': comp.get('country'),
        'geo_state': comp.get('state'),
        'geo_city': comp.get('city') or comp.get('town'),
        'geo_lat': res.get('geometry',{}).get('lat'),
        'geo_lng': res.get('geometry',{}).get('lng'),
    }

def main():
    p = argparse.ArgumentParser(description='Enrich CSV of IPs or coords')
    p.add_argument('input')
    p.add_argument('output')
    p.add_argument('--ip-col', default='ip')
    p.add_argument('--coord-cols', default='lat,lng')
    args = p.parse_args()

    df = pd.read_csv(args.input)
    rows = []
    if args.ip_col in df.columns:
        for ip in df[args.ip_col].dropna().astype(str):
            rows.append(enrich_ip(ip))
    else:
        lat_col,lng_col = args.coord_cols.split(',')
        for lat,lng in df[[lat_col,lng_col]].dropna().itertuples(index=False):
            rows.append(enrich_coords(lat,lng))

    out = pd.concat([df.reset_index(drop=True), pd.DataFrame(rows)], axis=1)
    out.to_csv(args.output, index=False)
    print(f'Enriched {len(df)} rows → {args.output}')

if __name__=='__main__':
    main()
