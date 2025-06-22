import requests

def get_ip_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,continent,country,regionName,city,zip,lat,lon,isp,org,as,query", timeout=5)
        data = response.json()
        if data['status'] == 'success':
            return {
                "ip": data.get("query"),
                "continent": data.get("continent"),
                "country": data.get("country"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "zip": data.get("zip"),
                "lat": data.get("lat"),
                "lon": data.get("lon"),
                "isp": data.get("isp"),
                "org": data.get("org"),
                "asn": data.get("as")
            }
        else:
            return {"ip_location_error": data.get("message")}
    except Exception as e:
        return {"ip_location_error": str(e)}
