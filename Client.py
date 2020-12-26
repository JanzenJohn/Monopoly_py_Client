import Network
import os

n = Network.Network()
while True:
    try:
        message, is_req = n.recv()
    except BrokenPipeError as e:
        print(e)
        exit()
    except EOFError as e:
        print("Server stopped responding")
        exit()
    if is_req and message != "OS":
        reply = input(str(message) + " : ")
        n.send("str", reply)
    elif is_req:
        n.send("str", str(os.name))
    elif message == "you won":
        print("You won")
        exit()
    elif message == "you loose":
        print("The game is over and you didn't win")
        exit()
    else:
        print(message)
