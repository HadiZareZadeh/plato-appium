import subprocess
from time import sleep

def get_emulator_list():
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    emulators = [line.split()[0] for line in lines if line.startswith("emulator")]
    return emulators


def get_offline_devices():
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    offline_devices = []
    for line in lines[1:]:
        if 'offline' in line:
            device_id = line.split()[0]
            offline_devices.append(device_id)
    return offline_devices


def terminate_emulator(emulator):
    subprocess.run(["adb", "-s", emulator, "emu", "kill"], capture_output=True, text=True)

def terminate_all_emulators():
    emulators = get_emulator_list()
    if not emulators:
        print("No emulators are currently running.")
    else:
        print("Terminating the following emulators:")
        for emulator in emulators:
            print(f"Terminating {emulator}...")
            terminate_emulator(emulator)
        print("All emulators terminated.")

if __name__ == "__main__":
    terminate_all_emulators()
    sleep(3)
