import cv2
import socket
import platform
import requests
import datetime
import os

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

if __name__ == "__main__":
    print("Logging failed login attempt...")
    capture_image()
    log_system_info()
    print("Logging complete")