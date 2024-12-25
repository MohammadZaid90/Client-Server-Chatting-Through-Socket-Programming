# import require modules
import socket
import threading

#from server import send_message_to_client

HOST = '192.168.0.100'
PORT = 1234     # 0 to 65535 
LISTENER_LIMIT = 5
active_clients = [] # list of currently connected clients


# function to listen for upcoming messages from a client
def listen_for_messages(client ,username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else:
            print(f"The message sent from client {username} is empty")


# function to send a message to single client
def send_message_to_client(client, message):
    client.sendall(message.encode())


# function to send any new message to all the clients that are connected to server
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)


# function to handle client
def client_handler(client):
    # server will listen for client message that contains username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "Server~" + f"{username} added to the chat" 
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()


# main function
def main():
    # creatubg the socket class object
    # AF_INET means we use IPv4 addresses
    # SOCK_STREAM means we use TCP Protocol packet for communicate
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running server on {HOST}, {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")
    
    # set server limit
    server.listen(LISTENER_LIMIT)

    # this while loop will keep listening to client connection
    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]}, {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()
