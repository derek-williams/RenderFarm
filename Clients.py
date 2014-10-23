"""The Client class returns the answer back to the client that was
passed through connection from the server."""

class Client:
    def getAnswer( self, question ):
        return self.connection.getAnswer( question )
