from twisted.internet import reactor
from quarry.net.proxy import DownstreamFactory, Bridge

class ProxyBridge(Bridge):    
    # def packet_unhandled(self, buff, direction, name):
    #     if direction == "downstream":
    #         self.downstream.send_packet(name, buff.read())
    #     elif direction == "upstream":
    #         print(f"[{direction}] {name}")
    #         self.upstream.send_packet(name, buff.read())
    
    def packet_upstream_chat_message(self, buff):
        buff.save()
        chat_message = buff.unpack_string()


        if chat_message.startswith(".sign"):
            sign_location = b'\x00'*8
            x = 1
            z = 2
            y = 3

            sign_location = sign_location | x.to_bytes(4, byteorder='little')
            sign_location = sign_location | z.to_bytes(4, byteorder='little') << 26
            sign_location = sign_location | y.to_bytes(4, byteorder='little') << 52

            print(f"sign_location", sign_location.hex())

            # self.downstream.send_packet("")

        buff.restore()
        self.upstream.send_packet("chat_message", buff.read())

    def packet_downstream_open_sign_editor(self, buff):
        buf = buff.read()
        print(f"open_sign_editor: ", bin)
        self.downstream.send_packet("open_sign_editor", buf)

    def packet_upstream_update_sign(self, buff):
        buf = buff.read()
        print(f"update_sign: ", buf.hex())
        self.upstream.send_packet("update_sign", buf)


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