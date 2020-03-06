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
        client = persons.client
        client.send(bytes(name + ": ", "utf8") + msg)


def client_communication(person):
    """
    Thread to handle all messages from client
    :param person: Person
    :return: None
    """
    client = person.client
    addr = person.addr

    # get persons name
    name = client.recv(BUFSIZ).decode("utf8")
    msg = f"{name} has joined the chat"
    broadcast(msg)

    while True:
        msg = client.recv(BUFSIZ)
        if msg == bytes("{quit}", "utf8"):
            broadcast(f"{name} has left the chat...", "")
            client.send(bytes("{quit}", "utf8"))
            client.close()
            persons.remove(person)
        else:
            client.send(msg, name)


def wait_for_connection():
    """
    wait for connection from new clients, start new thread once connected
    :param SERVER: SOCKET
    :return: None
    """
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)
            print(f"[COONECTION] {addr} connected to the server {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[FAILURE]",e)
            run = False

    print("SERVER CRASHED")



if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)
    print("waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()