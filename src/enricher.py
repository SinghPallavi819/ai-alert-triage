import os
import requests
from dotenv import load_dotenv

load_dotenv()

ABUSEIPDB_API_KEY = os.getenv("2d4f2d8d7e4fe86608f50c509ff4bbd709dbcf1f60beae59a7dc3378fbd0979a8a4aa191a670dca2")


def get_ip_reputation(ip_address):
    if not ABUSEIPDB_API_KEY:
        return {
            "abuse_score": "N/A",
            "total_reports": "N/A",
            "country_code": "N/A",
            "ip_reputation": "Unknown"
        }

    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip_address,
        "maxAgeInDays": 90
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()["data"]

        abuse_score = data.get("abuseConfidenceScore", 0)
        total_reports = data.get("totalReports", 0)
        country_code = data.get("countryCode", "N/A")

        if abuse_score >= 75:
            ip_reputation = "Known malicious"
        elif abuse_score >= 25:
            ip_reputation = "Suspicious"
        else:
            ip_reputation = "Low risk"

        return {
            "abuse_score": abuse_score,
            "total_reports": total_reports,
            "country_code": country_code,
            "ip_reputation": ip_reputation
        }

    except requests.RequestException:
        return {
            "abuse_score": "Error",
            "total_reports": "Error",
            "country_code": "Error",
            "ip_reputation": "Lookup failed"
        }


def enrich_alert(alert):
    if alert["status"] == "failed" and alert["event_count"] >= 20:
        alert["severity"] = "High"
    elif alert["status"] == "failed" and alert["event_count"] >= 10:
        alert["severity"] = "Medium"
    else:
        alert["severity"] = "Low"

    alert["summary"] = (
        f"This alert shows {alert['event_count']} failed login attempts "
        f"for user {alert['user']} from source IP {alert['src_ip']} "
        f"targeting {alert['destination_host']}. "
        f"The activity is classified as {alert['severity']} severity "
        f"and may indicate a possible brute-force attempt."
    )

    ip_data = get_ip_reputation(alert["src_ip"])
    alert["abuse_score"] = ip_data["abuse_score"]
    alert["total_reports"] = ip_data["total_reports"]
    alert["country_code"] = ip_data["country_code"]
    alert["ip_reputation"] = ip_data["ip_reputation"]

    return alert