import requests
import json
import base64

GRAFANA = "http://192.168.100.26:3000"
auth = base64.b64encode(b"admin:admin").decode()
headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}

# Get datasource UID
r = requests.get(f"{GRAFANA}/api/datasources", headers=headers)
ds_list = r.json()
ds_uid = None
for ds in ds_list:
    if ds["type"] == "prometheus":
        ds_uid = ds["uid"]
        break
print(f"Datasource UID: {ds_uid}")

if not ds_uid:
    # Create datasource
    ds_payload = {"name": "Prometheus-MSML", "type": "prometheus", "url": "http://prometheus:9090", "access": "proxy", "isDefault": True}
    r = requests.post(f"{GRAFANA}/api/datasources", json=ds_payload, headers=headers)
    ds_uid = r.json()["datasource"]["uid"]
    print(f"Created datasource: {ds_uid}")

# Create dashboard
DASHBOARD_TITLE = "Muhammad-Shirojul-Munir"
panels = [
    {"id": 1, "title": "CPU Usage (%)", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 0, "y": 0}, "targets": [{"expr": "cpu_usage_percent", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}]},
    {"id": 2, "title": "Memory Usage (bytes)", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 8, "y": 0}, "targets": [{"expr": "memory_usage_bytes", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}]},
    {"id": 3, "title": "Total Inference", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 16, "y": 0}, "targets": [{"expr": "model_inference_total", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}]},
    {"id": 4, "title": "Active Requests", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 0, "y": 8}, "targets": [{"expr": "active_requests", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}]},
    {"id": 5, "title": "Error Requests", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 8, "y": 8}, "targets": [{"expr": "error_requests_total", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}]},
    {"id": 6, "title": "Inference Duration", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 16, "y": 8}, "targets": [{"expr": "model_inference_duration_seconds_sum", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}]},
    {"id": 7, "title": "Prediction Class 0", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 0, "y": 16}, "targets": [{"expr": "model_prediction_0_total", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}]},
    {"id": 8, "title": "Prediction Class 1", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 8, "y": 16}, "targets": [{"expr": "model_prediction_1_total", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}]},
    {"id": 9, "title": "Accuracy Estimate", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 16, "y": 16}, "targets": [{"expr": "model_accuracy_estimate", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}]},
    {"id": 10, "title": "Data Drift Score", "type": "graph", "gridPos": {"h": 8, "w": 8, "x": 0, "y": 24}, "targets": [{"expr": "data_drift_score_estimate", "refId": "A", "datasource": {"type": "prometheus", "uid": ds_uid}}]}
]
dashboard = {"dashboard": {"id": None, "title": DASHBOARD_TITLE, "tags": ["MLflow", "Monitoring", "Dicoding"], "timezone": "browser", "schemaVersion": 38, "panels": panels}, "overwrite": True}
r = requests.post(f"{GRAFANA}/api/dashboards/db", json=dashboard, headers=headers)
result = r.json()
print(f"Dashboard: {result['status']} - {result.get('url', '')}")

# Create alerting contact point
contact = {"name": "Dicoding Email", "type": "email", "settings": {"addresses": "admin@dicoding.com"}, "isDefault": True}
r = requests.post(f"{GRAFANA}/api/v1/provisioning/contact-points", json=contact, headers=headers)
print(f"Contact point: {r.status_code} - {r.text[:100]}")

# Create alert rules via provisioning API
alert_rules = [
    {
        "name": "High CPU Usage",
        "ruleGroup": "ml-alerts",
        "folderUID": "",
        "for": "5m",
        "labels": {"severity": "warning"},
        "annotations": {"summary": "CPU usage > 80% for 5 min"},
        "data": [{
            "refId": "A",
            "relativeTimeRange": {"from": 600, "to": 0},
            "datasourceUid": ds_uid,
            "model": {"expr": "cpu_usage_percent > 80", "intervalMs": 10000, "maxDataPoints": 100, "refId": "A"}
        }],
        "noDataState": "NoData",
        "execErrState": "Error"
    },
    {
        "name": "High Error Rate",
        "ruleGroup": "ml-alerts",
        "folderUID": "",
        "for": "5m",
        "labels": {"severity": "critical"},
        "annotations": {"summary": "Error requests detected"},
        "data": [{
            "refId": "A",
            "relativeTimeRange": {"from": 600, "to": 0},
            "datasourceUid": ds_uid,
            "model": {"expr": "rate(error_requests_total[5m]) > 0", "intervalMs": 10000, "maxDataPoints": 100, "refId": "A"}
        }],
        "noDataState": "NoData",
        "execErrState": "Error"
    },
    {
        "name": "Memory Usage High",
        "ruleGroup": "ml-alerts",
        "folderUID": "",
        "for": "5m",
        "labels": {"severity": "warning"},
        "annotations": {"summary": "Memory > 8GB"},
        "data": [{
            "refId": "A",
            "relativeTimeRange": {"from": 600, "to": 0},
            "datasourceUid": ds_uid,
            "model": {"expr": "memory_usage_bytes > 8e9", "intervalMs": 10000, "maxDataPoints": 100, "refId": "A"}
        }],
        "noDataState": "NoData",
        "execErrState": "Error"
    }
]
for rule in alert_rules:
    r = requests.post(f"{GRAFANA}/api/v1/provisioning/alert-rules", json=rule, headers=headers)
    if r.status_code in [200, 201]:
        print(f"Alert rule created: {rule['name']}")
    else:
        print(f"Alert rule error {r.status_code}: {r.text[:100]}")

print("\nSetup selesai! Akses Grafana di http://192.168.100.26:3000")
