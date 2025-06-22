import shodan

def shodan_scan(ip, api_key):
    result = {}
    try:
        api = shodan.Shodan(api_key)
        host = api.host(ip)

        result['ip'] = host.get('ip_str')
        result['organization'] = host.get('org', 'n/a')
        result['os'] = host.get('os', 'n/a')
        result['isp'] = host.get('isp', 'n/a')
        result['country'] = host.get('country_name', 'n/a')
        result['city'] = host.get('city', 'n/a')
        result['last_update'] = host.get('last_update', 'n/a')

        ports_info = []
        for item in host.get('data', []):
            ports_info.append({
                "port": item.get("port"),
                "banner": item.get("data", "").strip()[:200]  # limit size
            })

        result['open_ports'] = ports_info

    except shodan.APIError as e:
        result['error'] = f"Shodan API Error: {e}"

    return result
