# scheduler.py
import schedule
import time
from agent import run_agent

def start_scheduler():
    schedule.every().day.at("08:00").do(run_agent)
    print("Scheduler started — will run daily at 08:00")
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    start_scheduler()
