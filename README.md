# AI-Powered SOC Alert Triage System

An AI-assisted Security Operations Center (SOC) alert triage pipeline built with Python. The system automatically enriches security alerts with live threat intelligence, classifies severity using rule-based logic, and generates investigation summaries using a local LLM — reducing manual analyst workload.

## What It Does

Security teams deal with hundreds of alerts every day. This pipeline automates the first layer of investigation:

1. Ingests simulated SIEM alerts in JSON format
2. Checks each IP against AbuseIPDB for live threat intelligence
3. Classifies alert severity using rule-based logic
4. Sends enriched alert data to a local LLM (Llama3 via Ollama)
5. LLM generates investigation summary and recommended next steps
6. Saves structured output to JSON

## Real Example Output

IP: 185.220.101.45
AbuseIPDB Score: 91/100
Reports: 103
Category: Tor Exit Node
Classification: CRITICAL
LLM Output: Escalate immediately — known malicious IP involved in brute force activity. Block at firewall, review affected accounts, check for lateral movement. MITRE ATT&CK: T1110 Brute Force.

IP: 10.0.0.15
AbuseIPDB Score: 0
Classification: LOW
LLM Output: Monitor — internal IP with no abuse history. No immediate action required.

## Tech Stack

- Python
- AbuseIPDB API — live IP threat intelligence
- Ollama — local LLM runner
- Llama3 — local language model (no data sent to cloud)
- JSON — alert ingestion and output

## Project Structure

ai-alert-triage/
├── src/
│   ├── main.py          # Main pipeline runner
│   ├── enricher.py      # AbuseIPDB API integration
│   ├── triage.py        # Rule-based classification logic
│   └── llm.py           # LLM prompt and response handler
├── data/
│   └── alerts.json      # Simulated SIEM alerts
├── .gitignore
├── requirements.txt
└── README.md

## How To Run

1. Install dependencies
   pip install -r requirements.txt

2. Install Ollama and pull Llama3
   ollama pull llama3

3. Add your AbuseIPDB API key to a .env file
   ABUSEIPDB_API_KEY=your_key_here

4. Run the pipeline
   python src/main.py

## Classification Logic

CRITICAL  — abuse score above 80 + high event count → Escalate immediately
HIGH      — abuse score above 50 + medium event count → Investigate urgently  
MEDIUM    — abuse score above 20 or medium event count → Review
LOW       — abuse score near 0 + low event count → Monitor

## Key Learning

This project demonstrates how AI and automation can reduce the manual workload of SOC analysts by handling the first layer of alert investigation — enrichment, classification, and initial guidance — so analysts can focus on complex decisions rather than repetitive lookups.
