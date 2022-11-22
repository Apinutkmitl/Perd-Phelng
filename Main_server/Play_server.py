import socket
import selectors
import traceback
import lib_for_sever
import lib_for_client
import vlc
import pafy 
import time
sel_system = selectors.DefaultSelector()
ready=False




    
def control(data,vlc_instance,player):
    # print(data)
    if data['command']=='play':
        global ready
        ready=True
        clip2=data['content']['url']
        try:
            video = pafy.new(clip2)
            videolink = video.getbestaudio()
            media = vlc_instance.media_new(videolink.url)
            player.set_media(media)
            player.play()
        except:
            time.sleep(1)
            video = pafy.new(clip2)
            videolink = video.getbestaudio()
            media = vlc_instance.media_new(videolink.url)
            player.set_media(media)
            player.play()
    
    if data['command']=='pause':
        player.pause()
    if data['command']=='stop':
        player.stop()




    

def send_data(host, port,request):
    addr = (host, port)
    sel = selectors.DefaultSelector()

    print(f"Starting connection to {addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
       
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    # print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = lib_for_sever.Message(sel_system, conn, addr)
    sel_system.register(conn, selectors.EVENT_READ, data=message)

host, port = "127.0.0.1", 2002
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel_system.register(lsock, selectors.EVENT_READ, data=None)
vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()

try:
    while True:
        
        events = sel_system.select(timeout=1)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    if mask & selectors.EVENT_READ:
                        message.command_read()
                        control(message.response,vlc_instance,player)
                        message.close()
                except Exception:
                    print(
                        f"Main: Error: Exception for {message.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    message.close()
        try:   
            if player.get_position()>0.990 and ready :
                player.stop()
                content=None
                action, user = "finish","system"
                data={"role": user,"command": action,"content": content}
                send_data('127.0.0.1',2000,data)
                ready=False
        except:
            pass
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel_system.close()
        
