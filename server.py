import os
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = BackgroundScheduler(daemon=True)

def prompt():
    print("Executing Task...")

scheduler.add_job(
    prompt,
    CronTrigger(hour='*', minute='*', second='*'),
    timezone='Australia/Perth'
)
scheduler.start()  

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)
