from tkinter import *
from PIL import ImageTk
from socket import *
import _thread
from urllib.request import urlopen
import re,urllib.request,urllib.parse
import pafy
import io
import json
import selectors
import traceback

import lib_for_client


def initialize_server():
    # initialize socket
    s = socket(AF_INET, SOCK_STREAM)
    # config details of server
    host = "127.0.0.1"  ## to use between devices in the same network eg.192.168.1.5
    port = 4000
    # initialize server
    s.bind((host, port))
    # set no. of clients
    s.listen()
    # accept the connection from client
    conn, addr = s.accept()

    return conn

def receive():

    while 1:
        try:
            data = conn.recv(1024)
            msg = data.decode('ascii')
            tiow = io.TextIOWrapper(
            io.BytesIO(data), encoding="utf-8", newline=""
            )
            msg = json.load(tiow)
            tiow.close()
            if msg != "":
                control(msg)
        except:
            pass

def control(msg):
    print(msg)
    
    if msg['role']=='system':
        if msg['command']=='play':
            img(msg['content']['url'])
    
    if msg['role']=='admin':
        if msg['command']=='update':
            update_listbox1(msg['content'])
    
    if msg['role']=='user':
        if msg['command']=='update':
            update_listbox2(msg['content'])

def send_data(host, port,request):
    addr = (host, port)
    sel = selectors.DefaultSelector()

    print(f"Starting connection to {addr}")
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_WRITE
    message = lib_for_client.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)

    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                print(mask)
                try:
                    message.command_write()
                    message.close()
                except Exception:
                    print(
                        f"Main: Error: Exception for {message.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    message.close()
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()
    
def search(name): # หาลิ้ง youtube จากชื่อ
    query_string = urllib.parse.urlencode({"search_query": name})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    clip2 =  "{}".format(search_results[0])
    return clip2

def picture(link):
    video=pafy.new(link)
    picture_url=video.bigthumbhd #url รูป title ของ video
    path='/Users/Onlyjune/Desktop/untitled folder 3/save/'+link+'.jpg' # path ที่ต้องการจะ save + ชื่อไฟล์
    urllib.request.urlretrieve(picture_url,path) #ดาวโหลด 
    print(path)
    return (path)

def name(link):
    video=pafy.new(link)
    name_video=video.title # ชื่อวิดิโอ
    return name_video

def imagelink(url):
    urls = "https://img.youtube.com/vi/" + url + "/0.jpg"
    print(urls)
    return urls
    
# Create Frame
def des():
    global t
    global label
    t.destroy
    label.destroy

def add():
    global entry_variable
    global t
    global label
    global button_add
    global a
    content={"id": "admin","url":a}
    action, user = "addmusic","admin"
    request={"role": user,"command": action,"content": content}
    send_data("127.0.0.1",2000,request)
    label.destroy
    t.destroy

def img(li):
    imageUrl = imagelink(li)
    u = urlopen(imageUrl)
    raw_data = u.read()
    u.close()
    photo = ImageTk.PhotoImage(data=raw_data)
    pho = Label(image=photo, height=450, width=450)
    pho.image = photo
    pho.place(relx=0.43, rely=0.3, anchor=CENTER)

def print_input():
    global entry_variable
    global t
    global label
    global button_add
    global a
    t = Label(text=" ")
    entry = entry_variable.get("0.0", END)
    
    a = search(entry)
    name_son = name(a)

    imageUrl = imagelink(a)
    u = urlopen(imageUrl)
    raw_data = u.read()
    u.close()

    photo = ImageTk.PhotoImage(data=raw_data)
    label = Label(image=photo, height=300, width=300)
    label.image = photo
    label.place(relx=0.85, rely=0.56, anchor=CENTER)
    t = Label(text=name_son)
    t.place(relx=0.85, rely=0.8, anchor=CENTER)

    button_add = Button(text="Add", command=add).place(relx=0.85, rely=0.84, anchor=CENTER)

def selected_admin():
    global listbox1
    for i in listbox1.curselection():
        url=search(listbox1.get(i))
        listbox1.delete(i)

    content={"id": "0","url":url}
    action, user = "select","admin"
    request={"role": user,"command": action,"content": content}
    send_data("127.0.0.1", 2000,request)

def selected_user():
    global listbox2

    for i in listbox2.curselection():
        url=search(listbox2.get(i))
        listbox2.delete(i)

    content={"id": "0","url":url}
    action, user = "select","user"
    request={"role": user,"command": action,"content": content}
    send_data("127.0.0.1", 2000,request)

def skip_bt():
    content={"id": "0","url":"kTHcaTCM4rs"}
    action, user = "skip","system"
    request={"role": user,"command": action,"content": content}
    send_data("127.0.0.1", 2000,request)

def pause_bt():
    content={"id": "0","url":"kTHcaTCM4rs"}
    action, user = "pause","system"
    request={"role": user,"command": action,"content": content}
    send_data("127.0.0.1", 2002,request)

def mode_bt():
    content=None
    action, user = "mode","system"
    request={"role": user,"command": action,"content": content}
    send_data("127.0.0.1", 2000,request)

def update_listbox1(update):
    global listbox1
    listbox1.delete(0,END)
    for i in range(len(update)):
        listbox1.insert(i, name(update[i]['url']))

def update_listbox2(update):
    global listbox2
    listbox2.delete(0,END)
    for i in range(len(update)):
        listbox2.insert(i, name(update[i]['url']))
        
def main():
    global entry_variable
    global button_submit
    global listbox1
    global listbox2
    root = Tk()
    root.title("Admin")
    root.geometry("1280x800")
    frame1 = Frame(root, background="light green", highlightthickness=1,width=400, height=600, bd= 0)
    frame1.pack( side = RIGHT )

    # Create widgets
    input_variable = StringVar()
    entry_variable = Text(root, bg='white', height=1, width=30)
    entry_variable.place(relx=0.85, rely=0.25, anchor=CENTER)
    button_submit = Button(root, text="Submit",command=print_input).place(relx=0.85, rely=0.3, anchor=CENTER)

    name1="gdZLi9oWNZg"
    name2="WMweEpGlu_U"

    listbox1=Listbox(root, width=30)
    listbox1.place(relx=0.17, rely=0.8, anchor=CENTER)

    listbox2=Listbox(root, width=30)
    listbox2.place(relx=0.54, rely=0.8, anchor=CENTER)

    btn = Button(root, text='select_admin',command=selected_admin).place(relx=0.17, rely=0.94, anchor=CENTER)
    btn = Button(root, text='select_user',command=selected_user).place(relx=0.51, rely=0.94, anchor=CENTER)

    pause = Button(root, text="pause", height=2,command=pause_bt).place(relx=0.32, rely=0.6, anchor=CENTER)
    skip = Button(root, text="skip", height=2,command=skip_bt).place(relx=0.42, rely=0.6, anchor=CENTER)
    mode = Button(root, text="mode", height=2,command=mode_bt).place(relx=0.52, rely=0.6, anchor=CENTER)

    _thread.start_new_thread(receive, ())

    root.mainloop()

if __name__ == '__main__':
    button_submit = None
    a=None
    conn = initialize_server()
    main()