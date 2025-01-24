from queue import Queue
from server.database import SessionLocal
from server.models.run import Run
from server.models.tournament import Tournament
from server.models.turn import Turn
from server.models.submission_run_info import SubmissionRunInfo
from server.models.team import Team
from server.models.team_type import TeamType
from server.models.university import University
from server.models.submission import Submission


class DB:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        self.db.begin()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

def worker_main(jobqueue: Queue):
    while not jobqueue.empty():
        job_func = jobqueue.get()
        job_func[0](*job_func[1:])
        jobqueue.task_done()
