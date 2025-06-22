import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()  # Converts to "2024-01-01T12:34:56" format
        return super().default(o)

def report_osint(data, outfile='osint_report.json'):
    with open(outfile, 'w') as f:
        json.dump(data, f, indent=2, cls=DateTimeEncoder)
