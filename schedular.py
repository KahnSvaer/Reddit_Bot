import schedule
import time
from datetime import datetime


class Scheduler:
    """
    A schedular clas to be able to easily create schedulars to do some functions at intervals
    """
    @staticmethod
    def start_scheduler(func):
        """This method sets up and starts the scheduler to run the job at specific times."""
        schedule.every().day.at("00:00").do(func) # Talk at 12:00 AM

        print(f"Scheduler started. Jobs will run at: {datetime.now()}")

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    def check_Schedular():
        print(time.time())

    Scheduler.start_scheduler(check_Schedular)

