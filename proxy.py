from twisted.internet import reactor
from quarry.net.proxy import DownstreamFactory, Bridge
import struct


class ProxyBridge(Bridge):
    orig_look = None
    orig_pos = None
    tele_id = None

    def packet_unhandled(self, buff, direction, name):
        if direction == "downstream":
            self.downstream.send_packet(name, buff.read())
        elif direction == "upstream":
            print(f"[{direction}] {name}")
            self.upstream.send_packet(name, buff.read())

    def packet_upstream_teleport_confirm(self, buff):
        buf = buff.read()
        print(f"teleport {buf.hex()}")
        self.tele_id = int(buf.hex(), 16)
        self.upstream.send_packet("teleport_confirm", buf)
        

    def packet_upstream_chat_message(self, buff):
        buff.save()

        chat_message = buff.unpack_string()
        
        if chat_message.startswith("tp"):
            try:
                _, dx, dy, dz = chat_message.split(" ")
                x, y, z = self.orig_pos
                x += float(dx)
                y += float(dy)
                z += float(dz)
                print(f" >> x: {x}, y: {y}, z: {z}")

                yaw, pitch, ground = self.orig_look
                flags = 0
                teleport = self.tele_id+1
                dismount = 0

                player_postion_buf = struct.pack('>dddffBBB', x, y, z, yaw, pitch, flags, teleport, dismount)
                self.downstream.send_packet('player_position_and_look', player_postion_buf)
            except Exception as e:
                print(f" >> error doing tp: {e}")

        buff.restore()
        self.upstream.send_packet("chat_message", buff.read())

    def packet_upstream_player_position(self, buff):
        buff.save()
        buf = buff.read()
        x, y, z, ground = struct.unpack('>dddB', buf)
        self.orig_pos = (x, y, z)
        print(f"player_position {x} / {y} / {z} | {ground}")
        buf = struct.pack('>dddB', x, y, z, ground)
        self.upstream.send_packet('player_position', buf)

    def packet_upstream_player_look(self, buff):
        buff.save()
        buf = buff.read()
        yaw, pitch, ground = struct.unpack('>ffB', buf)
        self.orig_look = (yaw, pitch, ground)
        buf = struct.pack('>ffB', yaw, pitch, ground)
        self.upstream.send_packet('player_look', buf)


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