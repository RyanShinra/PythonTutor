# test_logs.py
from pathlib import Path
from datetime import datetime, timedelta

def create_test_logs():
    # Create test directory if it doesn't exist
    test_dir = Path("test_logs")
    test_dir.mkdir(exist_ok=True)
    
    # Service 1 log - normal log with errors and warnings
    service1 = test_dir / "service1.log"
    with open(service1, "w") as f:
        base_time = datetime(2024, 2, 22, 15, 0, 0)
        f.write(f"{base_time} [INFO]: Service starting\n")
        f.write(f"{base_time + timedelta(minutes=1)} [ERROR]: Database connection failed\n")
        f.write(f"{base_time + timedelta(minutes=2)} [WARN]: Retrying connection\n")
        f.write(f"{base_time + timedelta(minutes=3)} [ERROR]: Retry limit exceeded\n")
    
    # Service 2 log - some malformed lines
    service2 = test_dir / "service2.log"
    with open(service2, "w") as f:
        base_time = datetime(2024, 2, 22, 16, 0, 0)
        f.write(f"{base_time} [WARN]: Memory usage high\n")
        f.write("Malformed line with no timestamp\n")
        f.write(f"{base_time + timedelta(minutes=5)} [ERROR]: Out of memory\n")
        f.write("2024-02-22 BadTime [WARN]: Bad timestamp\n")
    
    # Service 3 log - just info messages
    service3 = test_dir / "service3.log"
    with open(service3, "w") as f:
        base_time = datetime(2024, 2, 22, 14, 0, 0)
        f.write(f"{base_time} [INFO]: Service starting\n")
        f.write(f"{base_time + timedelta(minutes=30)} [INFO]: Healthy checkpoint\n")

if __name__ == "__main__":
    create_test_logs()