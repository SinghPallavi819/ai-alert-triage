import requests


def build_prompt(alert):
    prompt = f"""
You are a SOC analyst assistant.

Analyze the following alert and provide:
1. A short summary
2. Whether the alert should be escalated, reviewed, or monitored
3. The reason for that decision
4. The next investigation step

Alert details:
- Alert Name: {alert['alert_name']}
- Source: {alert['source']}
- Timestamp: {alert['timestamp']}
- User: {alert['user']}
- Source IP: {alert['src_ip']}
- Destination Host: {alert['destination_host']}
- Event Count: {alert['event_count']}
- Status: {alert['status']}
- Severity: {alert['severity']}
- Notes: {alert['notes']}
- Abuse Score: {alert['abuse_score']}
- Total Reports: {alert['total_reports']}
- Country Code: {alert['country_code']}
- IP Reputation: {alert['ip_reputation']}
"""
    return prompt


def generate_triage(alert):
    if alert["severity"] == "High":
        triage_decision = "Escalate"
        reason = "High number of failed login attempts suggests possible brute-force activity."
        recommended_action = "Investigate source IP, review authentication logs, and verify MFA."

    elif alert["severity"] == "Medium":
        triage_decision = "Review"
        reason = "Repeated failed logins detected but not yet critical."
        recommended_action = "Check login history and monitor the account."

    else:
        triage_decision = "Monitor"
        reason = "Low volume of failed login attempts."
        recommended_action = "Continue monitoring for unusual login activity."

    return {
        "triage_decision": triage_decision,
        "reason": reason,
        "recommended_action": recommended_action
    }


def ai_analysis(alert):
    prompt = build_prompt(alert)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    return result["response"]