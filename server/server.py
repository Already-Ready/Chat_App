from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# global constants
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512

# global variables
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # set up server

def broadcast(msg, name):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return:
    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION]", e)


def client_communication(person):
    """
    Thread to handle all messages from client
    :param person: Person
    :return: None
    """
    client = person.client

    # 처음 입력받는것은 사람 이름이 되어야함
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    msg = bytes(f"{name} has joined the chat", "utf8")
    broadcast(msg, "")

    while True: # 이름을 받은 후 다른 메시지가 오는걸 대기
        try:
            msg = client.recv(BUFSIZ)

            if msg == bytes("{quit}", "utf8"): # quit 을 입력받으면 연결 끊기
                client.close()
                persons.remove(person)
                print(f"[DISCONNECTED] {name} disconnected")
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
                break
            else: # 다른 메시지를 입력받으면 클라에 전송
                broadcast(msg, name+": ")
                print(f"{name} : ", msg.decode("utf8"))
        except Exception as e:
            print("[EXCEPTION]", e)
            break


def wait_for_connection():
    """
    wait for connection from new clients, start new thread once connected
    :param SERVER: SOCKET
    :return: None
    """

    while True:
        try:
            client, addr = SERVER.accept() # 새로운 connection 대기
            person = Person(addr, client) # connection 에 따른 새로운 Person 객체 생성
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to the server {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break

    print("SERVER CRASHED")



if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) # open server to listen for connection
    print("waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()