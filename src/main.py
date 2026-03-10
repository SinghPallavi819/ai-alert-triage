import json
from parser import load_alerts
from enricher import enrich_alert
from ai_triage import generate_triage, build_prompt, ai_analysis


def main():
    alerts = load_alerts("data/sample_alert.json")
    results = []

    for alert in alerts:
        enriched_alert = enrich_alert(alert)
        triage = generate_triage(enriched_alert)
        prompt = build_prompt(enriched_alert)
        ai_result = ai_analysis(enriched_alert)

        print("\n=== Alert Loaded Successfully ===")
        print(f"Alert Name       : {enriched_alert['alert_name']}")
        print(f"Source           : {enriched_alert['source']}")
        print(f"Timestamp        : {enriched_alert['timestamp']}")
        print(f"User             : {enriched_alert['user']}")
        print(f"Source IP        : {enriched_alert['src_ip']}")
        print(f"Destination Host : {enriched_alert['destination_host']}")
        print(f"Event Count      : {enriched_alert['event_count']}")
        print(f"Status           : {enriched_alert['status']}")
        print(f"Severity         : {enriched_alert['severity']}")
        print(f"Notes            : {enriched_alert['notes']}")
        print(f"Summary          : {enriched_alert['summary']}")
        print(f"Triage Decision  : {triage['triage_decision']}")
        print(f"Reason           : {triage['reason']}")
        print(f"Next Step        : {triage['recommended_action']}")

        print("\n--- AI Prompt Preview ---")
        print(prompt)

        print("\n--- AI Analysis ---")
        print(ai_result)

        results.append({
            "alert": enriched_alert,
            "triage": triage,
            "prompt": prompt,
            "ai_analysis": ai_result
        })

    with open("output/triage_results.json", "w") as file:
        json.dump(results, file, indent=4)

    print("\nAll triage results saved to output/triage_results.json")


if __name__ == "__main__":
    main()