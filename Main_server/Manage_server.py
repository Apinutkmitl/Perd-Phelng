import socket
import selectors
import traceback
import lib_for_client
import lib_for_sever
import Full_list
import json

sel_sys = selectors.DefaultSelector()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 4000
s.connect((host, port))

global mode
mode=False
admin_list=list()
user_list=list()
global state
state=True

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = lib_for_sever.Message(sel_sys, conn, addr)
    sel_sys.register(conn, selectors.EVENT_READ, data=message)

def send_data(host, port,request,Mode):
    addr = (host, port)
    sel = selectors.DefaultSelector()
    print(f"Starting connection to {addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_WRITE | selectors.EVENT_READ
    message = lib_for_client.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)
    response=None
    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                try:
                    if mask & selectors.EVENT_WRITE:
                        message.command_write()
                        if Mode:
                            message.close()
                    if mask & selectors.EVENT_READ:
                        message.command_read()
                        response=message.response
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
    return response

def send_admin(data):
    
    s.send(json.dumps(data, ensure_ascii=False).encode("utf-8"))

def control(data,message):
    global state,admin_list,user_list,user_list,mode
    if data['role']=='admin':
        if data['command']=='addmusic':
            system.addmusic_admin(**data['content'])
            temp=system.get_adminlist()
            action, user = "update","admin"
            request={"role": user,"command": action,"content": temp}
            send_admin(request)
        
        if data['command']=='selcet':
            content={'id':data['content']['id'],'url':data['content']['url']}
            action, user = "play","system"
            request={"role": user,"command": action,"content": content}
            send_admin(request)
            system.removemusicall_admin(content['url'])
            send_data("127.0.0.1",2002,request,True)
            content=system.get_adminlist()
            action, user = "update","admin"
            request={"role": user,"command": action,"content": content}
            send_admin(request)
            
        if data['command']=='remove':
            system.removemusic_admin(data['content']['url'])
            temp=system.get_adminlist()
            action, user = "update","admin"
            request={"role": user,"command": action,"content": temp}
            send_admin(request)
            
            
    if data['role']=='user':
        if data['command']=='addmusic':
            system.addmusic(**data['content'])
            content=system.get_list()
            action, user = "update","user"
            request={"role": user,"command": action,"content": content}
            send_admin(request)
        if data['command']=='selcet':

            content={'id':data['content']['id'],'url':data['content']['url']}
            action, user = "play","system"
            request={"role": user,"command": action,"content": content}
            send_admin(request)
            send_data("127.0.0.1",2002,request,True)
            content=system.get_list()
            action, user = "update","user"
            request={"role": user,"command": action,"content": content}
            send_admin(request)
            
            
        if data['command']=='remove':
            system.remove_id(data['content']['id'],data['content']['url'])
            target=data['content']
            for i in range(len(user_list)):
                if target['id']==user_list[i]['id'] and target['url']==user_list[i]['url']:
                    user_list.pop(i)
            content=system.get_list()
            action, user = "update","user"
            request={"role": user,"command": action,"content": content}
            send_admin(request)
            
    if data['role']=='system':

        if data['command']=='finish'or data['command']=='skip':
            state=True

        if data['command']=='mode':
            if mode:
                mode=False
            else:
                mode=True
        # ===================================================
        

        

host, port = "127.0.0.1", 2000
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel_sys.register(lsock, selectors.EVENT_READ, data=None)

system=Full_list.fulllist()

try:
    while True:
        events = sel_sys.select(timeout=1)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    if mask & selectors.EVENT_READ:
                        message.command_read()
                        control(message.response,message)
                        message.close()
                    
                except Exception:
                    print(
                        f"Main: Error: Exception for {message.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    message.close()
        #start
        if state:
            if mode:
                
                if len(admin_list)==0:
                    admin_list+=system.getmusic_admin()
                    
                if len(admin_list)!=0:
                    content=admin_list[0]
                    admin_list.pop(0)
                    action, user = "play","system"
                    request={"role": user,"command": action,"content": content}
                    send_admin(request)
                    system.removemusicall_admin(content['url'])
                    send_data("127.0.0.1",2002,request,True)
                    content=system.get_adminlist()
                    action, user = "update","admin"
                    request={"role": user,"command": action,"content": content}
                    send_admin(request)
                    state=False
            else:
                
                if len(user_list)==0:
                    user_list+=system.get_sublist()
                if len(user_list)!=0:
                    content=user_list[0]
                    user_list.pop(0)
                    action, user = "play","system"
                    request={"role": user,"command": action,"content": content}
                    send_admin(request)
                    #function_mysql.delet_allitem(content['url'],"user")
                    send_data("127.0.0.1",2002,request,True)
                    content=system.get_list()
                    action, user = "update","user"
                    request={"role": user,"command": action,"content": content}
                    send_admin(request)
                    state=False
                    
                    

except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel_sys.close()