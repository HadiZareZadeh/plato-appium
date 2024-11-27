import psutil

def close_hd_player():
    """پیدا کردن و بستن فرآیند hd-Player.exe از Task Manager."""
    process_name = "HD-Player.exe"
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            try:
                proc.terminate()  # پایان دادن به فرآیند
                print(f"Process {process_name} (PID: {proc.info['pid']}) terminated.")
            except Exception as e:
                print(f"Failed to terminate {process_name} (PID: {proc.info['pid']}): {e}")
            return  # پایان دادن به جستجو بعد از پیدا کردن و بستن
    print(f"Process {process_name} not found.")

# اجرا
if __name__ == "__main__":
    close_hd_player()
