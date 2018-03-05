import zmq
import time
# ZeroMQ Context


context = zmq.Context()

# Define the socket using the "Context"

sock_rec = context.socket(zmq.PULL)
#sock_rec.setsockopt(zmq.SUBSCRIBE,b'')
sock_rec.bind("tcp://127.0.0.1:5677")



sock = context.socket(zmq.PUB)
sock.bind("tcp://127.0.0.1:5678")
#message = sock_rec.recv()

dic = {}
while True:
    try:
        message = sock_rec.recv()
        message = message.decode('utf-8')
        print(message)
        try:
            key, value = message.split(">")
            
        except ValueError:
            msg = "\nUser [" + str(message) + "] Connected to the chat server."
        else:
            msg = "\n" + key + ":" + value       
        msg = msg.encode('utf-8')
        sock.send(msg)
    except zmq.ZMQError:
        pass
    time.sleep(0.5)
    