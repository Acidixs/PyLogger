import traceback
import os

from datetime import datetime
from enum import Enum

class Logger:
    class LogLevel(Enum):
        OFF = 0
        ERROR = 1
        WARNING = 2
        INFO = 3
        DEBUG = 4
        TRACE = 5
        ALL = 6

    class Color:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    log_level_colors = {
        LogLevel.ERROR: Color.FAIL,
        LogLevel.WARNING: Color.WARNING,
        LogLevel.INFO: Color.OKCYAN,
        LogLevel.DEBUG: Color.OKBLUE,
        LogLevel.TRACE: Color.HEADER
    }

    def __init__(self, log_level=LogLevel.ALL, log_file_path=None, record_logs=False):
        self.log_level = log_level
        self.log_file_path = log_file_path
        self.record_logs = record_logs

    def save_log_to_file(self, msg, level):
        current_date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        max_log_level_length = max(len(level.name) for level in self.LogLevel)
        log_message = f"[{level.name.ljust(max_log_level_length)}] [{current_date_time}] {msg}\n"

        with open(self.log_file_path, "a") as log_file:
            log_file.write(log_message)

    def log_to_console(self, msg, color):
        current_date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        print(f"[{current_date_time}]{color} {msg} {self.Color.ENDC}")        

    def log_message(self, msg, log_level):
        if self.log_level.value >= log_level.value:
            color = self.log_level_colors[log_level]
            self.log_to_console(msg, color)

            if self.record_logs:
                self.save_log_to_file(msg, log_level)

    def log_error(self, msg):
        self.log_message(msg, self.LogLevel.ERROR)

    def log_warning(self, msg):
        self.log_message(msg, self.LogLevel.WARNING)

    def log_info(self, msg):
        self.log_message(msg, self.LogLevel.INFO)

    def log_debug(self, msg):
        self.log_message(msg, self.LogLevel.DEBUG)

    def log_trace(self, msg):
        current_stack_frame = traceback.extract_stack()[0]
        filename = os.path.basename(current_stack_frame.filename)
        line_number = current_stack_frame.lineno
        function_name = current_stack_frame.name

        trace_msg = f"{filename}, {function_name}():{line_number}"
        self.log_message(f"{trace_msg} {msg}", self.LogLevel.TRACE) 


if __name__ == "__main__":
    loggr = Logger(Logger.LogLevel.ALL, "logs.txt", True)
    loggr.log_error("Error")
    loggr.log_warning("Warning")
    loggr.log_info("Info")
    loggr.log_debug("Debug")
    loggr.log_trace("tracing yo")
