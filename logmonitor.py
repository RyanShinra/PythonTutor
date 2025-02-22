from pathlib import Path
import logging
from datetime import datetime
import sys

def main(path: str = '.'):
    # Get all .log files
    log_files_paths: list[str] = list(Path(path).glob('*.log'))

    log_files: list[LogFile] = []
    first_time: datetime = datetime.max
    last_time: datetime = datetime.min
    total_errors = 0
    total_warnings = 0
    
    print(f'Log report for directory: {path} : {len(log_files_paths)} Files \n')
    
    # Maybe consider doing all this reading in a separate function to be called later
    for log_file_path in log_files_paths:
        current_log: LogFile = LogFile(log_file_path)
        log_files.append(current_log)
        
        first_time = min(first_time, current_log.first_time())
        last_time = max(last_time, current_log.last_time())
        error_count = len(current_log.error_lines())
        warn_count = len(current_log.warn_lines())
        
        total_errors += error_count
        total_warnings += warn_count
        print(f'{log_file_path} : {error_count} Errors, {warn_count} Warnings')
        
    print(f'''Timespan: {first_time} ~ {last_time}
          Errors for directory: {total_errors}
          Warnings for directory: {total_warnings}''')
        

class LogFile():
    
    def __init__(self, log_file_path: str):
        self._error_lines: list[str] = []
        self._warn_lines: list[str] = []
        self._first_time: datetime = datetime(3000, 1, 1)
        self._last_time: datetime = datetime(1970, 1, 2)
        try:
            with open(log_file_path) as log_file:
                
                for line in log_file:
                    
                    line_pieces: list[str] = line.split()
                    if len(line_pieces) < 2:
                        logging.warning(f'{log_file_path} : Invalid log line, timestamp seems to be missing: {line}')
                        continue
                    
                    try:
                        timestamp_str: str = f"{line_pieces[0]} {line_pieces[1]}"
                        timestamp: datetime = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                        self._first_time = min(self._first_time, timestamp)
                        self._last_time = max(self._last_time, timestamp)
                        
                    except ValueError:
                        logging.warning(f'{log_file_path} : Invalid log line, cannot parse timestamp: {line}')
                        continue
                    
                    if line.find('[ERROR]') > -1:
                        self._error_lines.append(line)
                    elif '[WARN]' in line:
                        self._warn_lines.append(line)

        except FileNotFoundError as e:
            logging.error(f'Error: File Not Found: {log_file_path}')
            raise e
        except PermissionError as e:
            logging.error(f'Error: Cannot read file: {log_file_path}')
            raise e
        

        
    def error_lines(self) -> list[str]: return self._error_lines
    
    def warn_lines(self) -> list[str]: return self._warn_lines
    
    def first_time(self) -> datetime: return self._first_time
    
    def last_time(self) -> datetime: return self._last_time

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = '.'
    main(path)