from flask_apscheduler import APScheduler

_scheduler = APScheduler()
print("_scheduler init-ed")

class AppScheduler:
    
    def __init__(self):
        self.scheduler = _scheduler

    def start(self):
        self.scheduler.start()
