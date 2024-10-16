import subprocess

def get_device_info(serial):
    """
    Fetches the device name and model using adb shell commands.
    """
    try:
        # Get device model
        model = subprocess.run(['adb', '-s', serial, 'shell', 'getprop', 'ro.product.model'], capture_output=True, text=True)
        # Get device name
        name = subprocess.run(['adb', '-s', serial, 'shell', 'getprop', 'ro.product.name'], capture_output=True, text=True)
        
        model = model.stdout.strip()
        name = name.stdout.strip()
        
        return model, name
    except Exception as e:
        return "Unknown", "Unknown"

def get_connected_devices():
    """
    Runs the 'adb devices' command and parses the list of connected devices.
    Returns a list of tuples, each containing device serial number, model, and name.
    """
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')[1:]  # Skip the first line 'List of devices attached'
    
    devices = []
    for line in lines:
        if line.strip():  # Ensure the line is not empty
            device_info = line.split()
            if len(device_info) == 2 and device_info[1] == 'device':
                serial = device_info[0]
                model, name = get_device_info(serial)
                devices.append((serial, model, name))  # Tuple of (serial, model, name)
    
    return devices

def choose_device(devices):
    """
    Lets the user choose a device from the list of connected devices.
    """
    if not devices:
        print("No devices connected.")
        return None
    
    print("Connected devices:")
    for i, (serial, model, name) in enumerate(devices):
        print(f"{i + 1}. Serial: {serial} | Model: {model} | Name: {name}")
    
    choice = input("Choose a device by number: ")
    
    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(devices):
            return devices[choice_index][0]  # Return the serial number
        else:
            print("Invalid choice.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def main():
    devices = get_connected_devices()
    
    if devices:
        chosen_device = choose_device(devices)
        if chosen_device:
            print(f"You selected device with Serial: {chosen_device}")
            # Use this device with Appium
            # For example, you can pass it to Appium capabilities like this:
            # capabilities['deviceName'] = chosen_device
        else:
            print("No valid device selected.")
    else:
        print("No devices connected.")

if __name__ == '__main__':
    main()
