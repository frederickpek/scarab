from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta
from AppScheduler import AppScheduler

import dummy

# python -m flask run

def create_app():
    app = Flask(__name__)
    app_scheduler = AppScheduler()

    @app.route("/")
    def index():
        return "Hello, Flask!"

    def job1():
        timenow = datetime.utcnow()
        print(f"job1 done at {timenow}")

    @app.route("/start_job1")
    def start_job1():
        job = {
            'id': 'job1',
            'func': job1,
            'trigger': 'interval',
            'seconds': 4,
        }
        app_scheduler.scheduler.add_job(**job)
        return "job1 started"

    @app.route("/stop_job1")
    def stop_job1():
        app_scheduler.scheduler.delete_job(id='job1')
        return "job1 deleted!"

    def job2():
        timenow = datetime.now()
        print(f"job2 done at {timenow}")

    @app.route("/start_job2")
    def start_job2():
        job = {
            'id': 'job2',
            'func': job2,
            'trigger': 'interval',
            'seconds': 4,
        }
        app_scheduler.scheduler.add_job(**job)
        return "job1 started"

    @app.route("/start_date_job")
    def start_date_job():
        timenow = datetime.now()
        print(f"date job started at {timenow}")
        job = {
            'id': 'job2',
            'func': job2,
            'trigger': 'date',
            'run_date': timenow + timedelta(seconds=10),
            'misfire_grace_time': None,
        }
        app_scheduler.scheduler.add_job(**job)
        return "DATE JOB STARTED"

    @app.route("/past_job")
    def past_job():
        timenow = datetime.now()
        print(f"past job issued at {timenow}")
        job = {
            'id': 'job2',
            'func': job2,
            'trigger': 'date',
            'run_date': timenow - timedelta(seconds=30),
            'misfire_grace_time': None,
        }
        app_scheduler.scheduler.add_job(**job)
        return "PAST JOB ISSUED"

    @app.route("/print_all_jobs")
    def print_all_jobs():
        return jsonify([{'id':job.id, 'name':job.name, 'func_name': job.func.__name__, 'trigger': str(job.trigger)} for job in app_scheduler.scheduler.get_jobs()])


    # behaviour of adding jobs with same ID

    def time_now_str() -> str:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def job_A():
        print(f"job_A done at {time_now_str()}")

    @app.route("/start_job_A1")
    def start_job_A1():
        job = {
            'id': 'job_A',
            'name': 'job_A1',
            'func': job_A,
            'trigger': 'interval',
            'seconds': 4,
            'replace_existing': True,
        }
        app_scheduler.scheduler.add_job(**job)
        return "job_A1 started"

    @app.route("/start_job_A2")
    def start_job_A2():
        job = {
            'id': 'job_A',
            'name': 'job_A2',
            'func': job_A,
            'trigger': 'interval',
            'seconds': 4,
            'replace_existing': True,
        }
        app_scheduler.scheduler.add_job(**job)
        return "job_A2 started"

    app_scheduler.start()
    return app

