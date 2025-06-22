import whois
import dns.resolver

def whois_dns(domain):
    res = {}
    try:
        res['whois'] = whois.whois(domain)
    except Exception as e:
        res['whois_error'] = str(e)

    try:
        res['dns'] = {t: [r.to_text() for r in dns.resolver.resolve(domain, t)]
                      for t in ['A', 'MX', 'NS', 'TXT']}
    except Exception as e:
        res['dns_error'] = str(e)

    return res