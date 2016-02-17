from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

class IphoneChat(Protocol):

    # Deals when a client is connected
    def connectionMade(self):
        # Add the client to a new list of clients
        self.factory.clients.append(self)
        print "Clients are ", self.factory.clients

    # Deals when a client disconnects
    def connectionLost(self, reason):
        # When a client leaves, remove him
        self.factory.clients.remove(self)

    # Deals with data sent
    def dataReceived(self, data):
        a = data.split(':')
        print a
        if len(a) > 1:
            command = a[0]
            content = a[1]

            msg = ""
            if command == "iam":
                self.name = content
                msg = self.name + " has joined"

            elif command == "msg":
                msg = self.name + ": " + content
                print msg

            for clients in self.factory.clients:
                clients.message(msg)

    # Deals with Messages
    def message(self, message):
        self.transport.write(message + '\n')

# Handles Incoming Connections
factory = Factory()
factory.clients = []
factory.protocol = IphoneChat

reactor.listenTCP(80, factory)
print "Iphone Chat server started"
reactor.run()
