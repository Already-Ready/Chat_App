from client import Client
import time
from threading import Thread

c1 = Client("Tim")
c2 = Client("Joe")


def update_messages():
    """
    update the local list of messages
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)
        new_messages = c1.get_messages() # get any new messages from client
        msgs.extend(new_messages) # add to local list of messages
        for msg in new_messages: # display new messages
            print(msg)
            if msg == "{quit}":
                run = False
                break

Thread(target=update_messages).start()

c1.send_messages("hello")
time.sleep(1)
c2.send_messages("whats up")
time.sleep(1)
c1.send_messages("nothing much, bro")
time.sleep(1)
c2.send_messages("boring...")
time.sleep(5)

c1.disconnect()
time.sleep(2)
c2.disconnect()
