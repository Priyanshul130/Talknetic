import subprocess
import pyautogui as p
import time 

def call(no):
    subprocess.Popen(["cmd", "/C", "start whatsapp://call?phone=+91"+str(no)+"^"], shell=True)
def text(msg,no):
    a=f'whatsapp://send?phone=+91"+{str(no)}+"^&text={str(msg.replace(' ','%20'))}^'
    print(a)
    print(msg)
    #subprocess.Popen(["cmd", "/C", "start whatsapp://send?phone=+91"+str(no)+"^&text="+str(msg)], shell=True)
    subprocess.Popen([f"cmd", "/C", f"start {a}"] , shell=True)

while True:
    print('''
          1-call
          2-text
          3-exit''')
    ch=int(input("enter you choice:"))
    a=input("enter phone no")
    if ch==1:
        print("CALLING!!!",a)
        call(a)
    elif ch==2:
        b=input("enter your message:-")
        
        p.write(b)
        print("MESSAGING",a)
        text(b,a)
        p.press("Enter")
        
        
    elif ch==3:
        break
    else:
        print("CHOOSE FROM ABOVE MENU ONLY:-")
    time.sleep(2)


