import requests
import json
import base64

GRAFANA_URL = "http://192.168.100.26:3000"
AUTH = base64.b64encode(b"admin:admin").decode()

headers = {
    "Authorization": f"Basic {AUTH}",
    "Content-Type": "application/json"
}

# 1. Create Prometheus datasource
ds_payload = {
    "name": "Prometheus-MSML",
    "type": "prometheus",
    "url": "http://prometheus:9090",
    "access": "proxy",
    "isDefault": True
}
r = requests.post(f"{GRAFANA_URL}/api/datasources", json=ds_payload, headers=headers)
ds_uid = r.json()["datasource"]["uid"]
print(f"Datasource created, UID: {ds_uid}")

# 2. Create dashboard with 10 metrics
dashboard = {
    "dashboard": {
        "id": None,
        "title": "Muhammad-Shirojul-Munir",
        "tags": ["MLflow", "Monitoring", "Dicoding"],
        "timezone": "browser",
        "schemaVersion": 38,
        "panels": [
            {"id": 1, "title": "CPU Usage (%)", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 0, "y": 0}, "targets": [{"expr": "cpu_usage_percent", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}], "yaxes": [{"format": "percent", "label": "CPU %"}]},
            {"id": 2, "title": "Memory Usage (bytes)", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 8, "y": 0}, "targets": [{"expr": "memory_usage_bytes", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}], "yaxes": [{"format": "bytes", "label": "RAM"}]},
            {"id": 3, "title": "Total Inference", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 16, "y": 0}, "targets": [{"expr": "model_inference_total", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}], "yaxes": [{"format": "short", "label": "Count"}]},
            {"id": 4, "title": "Active Requests", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 0, "y": 8}, "targets": [{"expr": "active_requests", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}], "yaxes": [{"format": "short", "label": "Requests"}]},
            {"id": 5, "title": "Error Requests Total", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 8, "y": 8}, "targets": [{"expr": "error_requests_total", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}], "yaxes": [{"format": "short", "label": "Errors"}]},
            {"id": 6, "title": "Inference Duration (seconds)", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 16, "y": 8}, "targets": [{"expr": "model_inference_duration_seconds_sum", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}], "yaxes": [{"format": "s", "label": "Seconds"}]},
            {"id": 7, "title": "Prediction Class 0 (Malignant)", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 0, "y": 16}, "targets": [{"expr": "model_prediction_0_total", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}], "yaxes": [{"format": "short", "label": "Count"}]},
            {"id": 8, "title": "Prediction Class 1 (Benign)", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 8, "y": 16}, "targets": [{"expr": "model_prediction_1_total", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}], "yaxes": [{"format": "short", "label": "Count"}]},
            {"id": 9, "title": "Accuracy Estimate", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 16, "y": 16}, "targets": [{"expr": "model_accuracy_estimate", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}], "yaxes": [{"format": "percentunit", "label": "Accuracy"}]},
            {"id": 10, "title": "Data Drift Score", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 0, "y": 24}, "targets": [{"expr": "data_drift_score_estimate", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}], "yaxes": [{"format": "percentunit", "label": "Drift"}]}
        ]
    },
    "overwrite": True
}
r = requests.post(f"{GRAFANA_URL}/api/dashboards/db", json=dashboard, headers=headers)
print(f"Dashboard created: {r.json()['status']} - {r.json().get('url', '')}")

# 3. Create alerting rules (3 rules for advanced)
alert_rules = [
    {
        "name": "High CPU Usage Alert",
        "folderUID": "",
        "ruleGroup": "ml-alerts",
        "condition": "C",
        "data": [
            {"refId": "A", "queryType": "", "relativeTimeRange": {"from": 600, "to": 0}, "datasourceUid": ds_uid, "model": {"expr": "cpu_usage_percent", "intervalMs": 1000, "maxDataPoints": 100, "refId": "A"}},
            {"refId": "B", "queryType": "", "relativeTimeRange": {"from": 600, "to": 0}, "datasourceUid": "__expr__", "model": {"conditions": [{"evaluator": {"params": [80], "type": "gt"}, "operator": {"type": "and"}, "query": {"params": ["A"]}, "reducer": {"params": [], "type": "avg"}}], "expression": "A", "intervalMs": 1000, "maxDataPoints": 100, "reducer": "avg", "refId": "B", "type": "classic_conditions"}},
            {"refId": "C", "queryType": "", "relativeTimeRange": {"from": 600, "to": 0}, "datasourceUid": "__expr__", "model": {"conditions": [{"evaluator": {"params": [80], "type": "gt"}, "operator": {"type": "and"}, "query": {"params": ["A"]}, "reducer": {"params": [], "type": "avg"}}], "expression": "B", "intervalMs": 1000, "maxDataPoints": 100, "reducer": "avg", "refId": "C", "type": "classic_conditions"}}
        ],
        "noDataState": "NoData",
        "execErrState": "Error",
        "for": "5m",
        "annotations": {"summary": "CPU usage is above 80% for 5 minutes"},
        "labels": {"severity": "warning", "team": "mlops"}
    }
]
# Note: Creating alerting rules in Grafana requires the provisioning API or the newer alerting API
# For simplicity, we'll create them via the provisioning file approach or the alerting API

# 4. Create contact point and notification policy for alerts
contact_point = {
    "name": "Email Notification",
    "type": "email",
    "settings": {"addresses": "admin@dicoding.com"},
    "isDefault": True
}
r = requests.post(f"{GRAFANA_URL}/api/v1/provisioning/contact-points", json=contact_point, headers=headers)
print(f"Contact point: {r.status_code}")

print("\nSetup selesai! Dashboard dapat diakses di Grafana.")
