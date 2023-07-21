# Welcome to PyShine

# This code is for the server
# Lets import the libraries
import socket, cv2, pickle, struct, imutils, threading
import cv
import movement_controller

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '192.168.0.55'  # server ip address here
print('HOST IP:', host_ip)
port = 6969
socket_address = (host_ip, port)
payload_size = struct.calcsize("Q")

def deepcopy(arr, newArr):
    for i in range(len(arr)):
        arr[i] = newArr[i]

def stream_video(conn, addr):
    print(f"[NEW CONNECTION] {addr} CONNECTED")
    
    vid = cv2.VideoCapture(0)
    
    facePos = []
    
    movement_thread = threading.Thread(target=movement_controller, args=(facePos))
    movement_thread.start()
    
    while (vid.isOpened()):
        img, frame = vid.read()
        
        frame, pos = cv.parseFrame(frame)
        
        #deepcopy(facePos, pos)
        
        movement_controller.move(facePos)
        
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        conn.sendall(message)
    
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            conn.close()
    conn.close()

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)

# Socket Accept
while True:
    conn, addr = server_socket.accept()
    video_send_thread = threading.Thread(target=stream_video, args=(conn, addr))
    video_send_thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
