from playwright.sync_api import sync_playwright
import time
import os

GRAFANA = "http://192.168.100.26:3000"
PROMETHEUS = "http://192.168.100.26:9090"
BASE_DIR = "D:/dicoding/Membangun-Sistem-Machine-Learning/Monitoring dan Logging"

def take_screenshot(page, url, filepath, wait_selector=None, sleep=3):
    page.goto(url, wait_until="networkidle")
    time.sleep(sleep)
    if wait_selector:
        page.wait_for_selector(wait_selector, timeout=10000)
        time.sleep(2)
    page.screenshot(path=filepath, full_page=True)
    print(f"Saved: {filepath}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    
    # 1. Bukti Serving - curl output simulation
    os.makedirs(f"{BASE_DIR}/1.bukti_serving", exist_ok=True)
    page.goto(PROMETHEUS, wait_until="networkidle")
    # We'll capture serving proof from MLflow
    
    # 2. Prometheus targets - show UP status
    os.makedirs(f"{BASE_DIR}/4.bukti monitoring Prometheus", exist_ok=True)
    take_screenshot(page, f"{PROMETHEUS}/targets", f"{BASE_DIR}/4.bukti monitoring Prometheus/1.monitoring_prometheus_targets.png", wait_selector="table")
    
    # 3. Prometheus graph - cpu_usage_percent
    graph_url = f"{PROMETHEUS}/graph?g0.expr=cpu_usage_percent&g0.tab=0&g0.stacked=0&g0.range_input=15m"
    take_screenshot(page, graph_url, f"{BASE_DIR}/4.bukti monitoring Prometheus/2.monitoring_cpu_usage.png")
    
    # 4. Prometheus - model_inference_total
    graph_url2 = f"{PROMETHEUS}/graph?g0.expr=model_inference_total&g0.tab=0&g0.stacked=0&g0.range_input=15m"
    take_screenshot(page, graph_url2, f"{BASE_DIR}/4.bukti monitoring Prometheus/3.monitoring_inference_total.png")
    
    # 5. Prometheus - memory_usage_bytes
    graph_url3 = f"{PROMETHEUS}/graph?g0.expr=memory_usage_bytes&g0.tab=0&g0.stacked=0&g0.range_input=15m"
    take_screenshot(page, graph_url3, f"{BASE_DIR}/4.bukti monitoring Prometheus/4.monitoring_memory_usage.png")
    
    # 6. Login to Grafana
    page.goto(f"{GRAFANA}/login", wait_until="networkidle")
    time.sleep(2)
    # Fill login form
    page.fill('input[name="user"]', 'admin')
    page.fill('input[name="password"]', 'admin')
    page.click('button[type="submit"]')
    time.sleep(3)
    
    # 7. Grafana Dashboard screenshot
    os.makedirs(f"{BASE_DIR}/5.bukti monitoring Grafana", exist_ok=True)
    page.goto(f"{GRAFANA}/dashboards", wait_until="networkidle")
    time.sleep(3)
    # Find our dashboard and click it
    dashboard_link = page.query_selector('a[href*="Muhammad-Shirojul-Munir"]')
    if dashboard_link:
        dashboard_link.click()
        time.sleep(5)
        page.screenshot(path=f"{BASE_DIR}/5.bukti monitoring Grafana/1.monitoring_dashboard_full.png", full_page=True)
        print("Dashboard screenshot captured")
    
    # 8. Alerting rules screenshot
    os.makedirs(f"{BASE_DIR}/6.bukti alerting Grafana", exist_ok=True)
    page.goto(f"{GRAFANA}/alerting/list", wait_until="networkidle")
    time.sleep(5)
    page.screenshot(path=f"{BASE_DIR}/6.bukti alerting Grafana/1.rules_alerting_rules.png", full_page=True)
    
    # 9. Notification channels
    page.goto(f"{GRAFANA}/alerting/notifications", wait_until="networkidle")
    time.sleep(5)
    page.screenshot(path=f"{BASE_DIR}/6.bukti alerting Grafana/2.notifikasi_alerting.png", full_page=True)
    
    browser.close()
    print("\nAll screenshots captured successfully!")
