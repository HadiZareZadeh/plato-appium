import schedule
import time
import subprocess
import os
import psutil

# مسیر پوشه پروژه
project_folder = os.path.dirname(os.path.abspath(__file__))
main_script = os.path.join(project_folder, "make coins - go fish.py")

# فایل‌های دیگر که باید قبل از اجرای فایل اصلی اجرا شوند
stop_scripts = [
    os.path.join(project_folder, "stop msi.py"),
    os.path.join(project_folder, "stop instances.py"),
    os.path.join(project_folder, "stop servers.py"),
    os.path.join(project_folder, "stop emulator.py")
]

pre_scripts = [
    os.path.join(project_folder, "stop msi.py"),
    os.path.join(project_folder, "stop instances.py"),
    os.path.join(project_folder, "stop servers.py"),
    os.path.join(project_folder, "stop emulator.py")
]

def kill_python_processes():
    """بستن تمام فرآیندهای پایتون به جز اسکریپت فعلی."""
    current_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'python.exe' and proc.info['pid'] != current_pid:
            try:
                proc.terminate()
                print(f"Terminated process: PID {proc.info['pid']}")
            except Exception as e:
                print(f"Failed to terminate process: {proc.info['pid']} - {e}")
    time.sleep(5)  # صبر 10 ثانیه‌ای بعد از بستن فرآیندها

def run_pre_scripts():
    """اجرای فایل‌های اولیه با تأخیر بین هر کدام."""
    for script in pre_scripts:
        if os.path.exists(script):
            print(f"Running script: {script}")
            try:
                subprocess.run(["python", script], check=True)
                time.sleep(5)  # صبر 10 ثانیه بین هر اسکریپت
            except subprocess.CalledProcessError as e:
                print(f"Error running script {script}: {e}")
        else:
            print(f"File not found: {script}")

def run_main_script():
    """اجرای فایل اصلی."""
    print("Starting the main process...")
    kill_python_processes()  # بستن فرآیندهای پایتون
    run_pre_scripts()  # اجرای فایل‌های اولیه با تأخیر
    # اجرای فایل اصلی
    if os.path.exists(main_script):
        print(f"Running main script: {main_script}")
        try:
            subprocess.run(["python", main_script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running main script: {e}")
    else:
        print(f"Main script not found: {main_script}")

# زمان‌بندی اجرای فایل اصلی
schedule.every().day.at("03:31").do(run_main_script)

print("Scheduled task is running. Waiting for the specified time. Press Ctrl+C to exit.")

# حلقه اصلی برای اجرا و نظارت
while True:
    schedule.run_pending()
    time.sleep(2)
