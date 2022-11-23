from app import app

from flask import render_template, request, jsonify, json

@app.route('/', methods=["GET","POST"])
def index():
    return render_template('public/index.html')

@app.route('/songname', methods=["POST"])
def add():
    import re,urllib.request,urllib.parse, pafy,json

    def search(name): # หาลิ้ง youtube จากชื่อ
        query_string = urllib.parse.urlencode({"search_query": name})
        formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
        search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
        clip2 = "{}".format(search_results[0])
        return clip2

    def picture(link):
        video=pafy.new(link)
        picture_url=video.bigthumbhd #url รูป title ของ video
        path='app/static/img/thumbnails/'+link+'.jpg' # path ที่ต้องการจะ save + ชื่อไฟล์
        shortpath='static/img/thumbnails/'+link+'.jpg'
        urllib.request.urlretrieve(picture_url,path) #ดาวโหลด 
        return shortpath

    def name(link):
        video=pafy.new(link) 
        name_video=video.title # ชื่อวิดิโอ
        return name_video

    data = request.get_json()
    songInput = data.get('song')
    link = search(songInput)
    searchSong = name(link)
    imgPath = picture(link)
    jsonData = {'title': searchSong, "URL":imgPath}
    
    # with open("app/songname.json", "r") as f:
    #     file_data = json.load(f)
    # file_data.append(jsonData)
    # with open("app/songname.json",'w') as f:
    #     json.dump(file_data, f)
    
    return jsonify({"songname":searchSong,"imgPath": imgPath, "link":link})

@app.route('/sendsong', methods=["POST"])
def send_to_server():
    import re,urllib.request,urllib.parse, pafy, socket, selectors, traceback
    import lib_for_client

    def search(name): # หาลิ้ง youtube จากชื่อ
        query_string = urllib.parse.urlencode({"search_query": name})
        formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
        search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
        clip2 = "{}".format(search_results[0])
        return clip2

    def picture(link):
        video=pafy.new(link)
        picture_url=video.bigthumbhd #url รูป title ของ video
        path='app/static/img/thumbnails/'+link+'.jpg' # path ที่ต้องการจะ save + ชื่อไฟล์
        shortpath='static/img/thumbnails/'+link+'.jpg'
        urllib.request.urlretrieve(picture_url,path) #ดาวโหลด 
        return shortpath

    def name(link):
        video=pafy.new(link) 
        name_video=video.title # ชื่อวิดิโอ
        return name_video
    
    def send_data(host, port,request):
        addr = (host, port)
        sel = selectors.DefaultSelector()

        print(f"Starting connection to {addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_WRITE | selectors.EVENT_READ
        message = lib_for_client.Message(sel, sock, addr, request)
        sel.register(sock, events, data=message)

        try:
            while True:
                events = sel.select(timeout=1)
                for key, mask in events:
                    message = key.data
                    try:
                        if mask & selectors.EVENT_WRITE:
                            message.command_write()
                        if mask & selectors.EVENT_READ:
                            message.command_read()
                            print(message.response)
                            message.close()
                            return message.response
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

    content={"id": "admin","url":"youtube.com"}
    action, user = "addmusic","user"
    req={"role": user,"command": action,"content": content}
    
    data = request.get_json()
    songInput = data.get('song')
    link = search(songInput)
    searchSong = name(link)
    imgPath = picture(link)
    
    return jsonify({"songname":searchSong,"imgPath": imgPath, "link":link}),send_data("127.0.0.1",2000,{"role": user,"command": action,"content": {"id": "0","url":link}})