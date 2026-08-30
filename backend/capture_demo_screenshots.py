import os
import time
# pyrefly: ignore [missing-import]
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ARTIFACT_DIR = r"C:\Users\HP\.gemini\antigravity-ide\brain\846b1636-6e11-4243-a2bb-65eb907e975d"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1366,900")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

print("[*] Launching headless browser...")
driver = webdriver.Chrome(options=chrome_options)

try:
    # 1. Landing Page
    print("[1] Navigating to Landing Page...")
    driver.get("http://localhost:5173/")
    time.sleep(2)
    path_landing = os.path.join(ARTIFACT_DIR, "demo_01_landing_page.png")
    driver.save_screenshot(path_landing)
    print(f"    Saved: {path_landing}")

    # 2. Login Page
    print("[2] Navigating to Login Page...")
    driver.get("http://localhost:5173/login")
    time.sleep(1.5)
    path_login = os.path.join(ARTIFACT_DIR, "demo_02_login_page.png")
    driver.save_screenshot(path_login)
    print(f"    Saved: {path_login}")

    # 3. Perform 1-Click Demo Login
    print("[3] Performing 1-Click Demo Authentication...")
    demo_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Quick Academic Evaluation') or contains(., 'Autofill')]"))
    )
    demo_btn.click()
    time.sleep(2.5)

    # 4. Clinician Dashboard
    print("[4] Capturing Dashboard...")
    path_dashboard = os.path.join(ARTIFACT_DIR, "demo_03_dashboard.png")
    driver.save_screenshot(path_dashboard)
    print(f"    Saved: {path_dashboard}")

    # 5. New Analysis Page
    print("[5] Navigating to New Analysis...")
    driver.get("http://localhost:5173/analyses/new")
    time.sleep(2)

    # Click Load Sample Histology Scan
    try:
        sample_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Load Sample Histology Scan')]"))
        )
        sample_btn.click()
        time.sleep(1.5)
    except Exception as e:
        print(f"    Notice: {e}")

    path_new = os.path.join(ARTIFACT_DIR, "demo_04_new_analysis.png")
    driver.save_screenshot(path_new)
    print(f"    Saved: {path_new}")

    # 6. Launch Pipeline
    print("[6] Launching Hybrid Pipeline...")
    submit_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    submit_btn.click()
    time.sleep(1)

    # Process page
    path_process = os.path.join(ARTIFACT_DIR, "demo_05_processing_pipeline.png")
    driver.save_screenshot(path_process)
    print(f"    Saved: {path_process}")

    # Wait for result page
    print("[7] Waiting for Quantum ML Result...")
    WebDriverWait(driver, 20).until(
        EC.url_contains("/result")
    )
    time.sleep(2)
    path_result = os.path.join(ARTIFACT_DIR, "demo_06_result_quantum_telemetry.png")
    driver.save_screenshot(path_result)
    print(f"    Saved: {path_result}")

    # 7. Technology Page
    print("[8] Capturing Technology Guide...")
    driver.get("http://localhost:5173/technology")
    time.sleep(1.5)
    path_tech = os.path.join(ARTIFACT_DIR, "demo_07_technology_architecture.png")
    driver.save_screenshot(path_tech)
    print(f"    Saved: {path_tech}")

    print("\n[+] All demo screenshots successfully captured!")

finally:
    driver.quit()
