from twisted.internet import reactor
from quarry.net.proxy import DownstreamFactory, Bridge


class ProxyBridge(Bridge):
    def packet_unhandled(self, buff, direction, name):
        print(f"[{direction}] {name}")
        if direction == "downstream":
            self.downstream.send_packet(name, buff.read())
        elif direction == "upstream":
            self.upstream.send_packet(name, buff.read())


def main(argv):
    factory = DownstreamFactory()
    factory.bridge_class = ProxyBridge
    factory.connect_host = "127.0.0.1"
    factory.connect_port = 12345
    factory.listen("127.0.0.1", 25565)
    reactor.run()

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])