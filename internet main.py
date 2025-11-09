import speedtest
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

# ==========================
# CONFIGURATION
# ==========================
CSV_FILE = "speed_log.csv"  # CSV file name
INTERVAL = 300              # seconds (300s = 5 minutes)
RUNS = 5                    # number of tests before stopping

def test_speed():
    """Run speed test and return ping, download, upload (in Mbps)."""
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000
    ping = st.results.ping
    return ping, round(download, 2), round(upload, 2)

def log_to_csv(timestamp, ping, download, upload):
    """Append test result to CSV file."""
    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, ping, download, upload])

def init_csv():
    """Create CSV file with header."""
    with open(CSV_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Ping (ms)", "Download (Mbps)", "Upload (Mbps)"])

def plot_graph():
    """Plot download/upload trends using matplotlib."""
    df = pd.read_csv(CSV_FILE)
    plt.figure(figsize=(10, 5))
    plt.plot(df["Timestamp"], df["Download (Mbps)"], label="Download", marker="o")
    plt.plot(df["Timestamp"], df["Upload (Mbps)"], label="Upload", marker="o")
    plt.xlabel("Time")
    plt.ylabel("Speed (Mbps)")
    plt.title("Internet Speed Trends")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    print("=" * 60)
    print("        ⚡ INTERNET SPEED MONITOR & LOGGER")
    print("=" * 60)
    init_csv()
    for i in range(RUNS):
        print(f"\n[{i+1}/{RUNS}] Running speed test...")
        ping, download, upload = test_speed()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Ping: {ping} ms | Download: {download} Mbps | Upload: {upload} Mbps")
        log_to_csv(timestamp, ping, download, upload)
        if i < RUNS - 1:
            print(f"⏳ Waiting {INTERVAL/60:.0f} minutes for next test...")
            time.sleep(INTERVAL)
    print("\n✅ Test complete. Results saved to", CSV_FILE)
    plot_graph()

if __name__ == "__main__":
    main()
