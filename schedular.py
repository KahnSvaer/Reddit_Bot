import schedule
import time


class Scheduler:
    """
    A scheduler class to create daily jobs at specified times.
    """
    @staticmethod
    def start_daily_scheduler(func, time_str: str):
        """
               Sets up and starts the scheduler to run the job at specific times.

               Args:
                   func (callable): The function to be scheduled.
                   time_str (str): The time to run the job in HH:MM format (24-hour format).

               Raises:
                   ValueError: If the time format is invalid.
        """
        if len(time_str) == 1:
            time_str = f"0{time_str}:00"
        elif time_str == "12":
            time_str = "12:00"
        elif len(time_str) == 5:
            time_str = time_str
        else:
            print("Invalid time format provided. Scheduler will not start.")
            return
        schedule.every().day.at(time_str).do(func)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    def check_Schedular():
        print(time.time())

    Scheduler.start_daily_scheduler(check_Schedular, "22:31")

