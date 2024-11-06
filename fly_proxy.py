from twisted.internet import reactor
from quarry.net.proxy import DownstreamFactory, Bridge
import struct, sys, time

class ProxyBridge(Bridge):    
    y_const = 0

    def packet_unhandled(self, buff, direction, name):
        if direction == "downstream":
            self.downstream.send_packet(name, buff.read())
        elif direction == "upstream":
            print(f"[{direction}] {name}")
            self.upstream.send_packet(name, buff.read())

    def packet_upstream_player_position_and_look(self, buff):
        buf = buff.read()
        x, y, z, yaw, pitch, ground = struct.unpack('>dddffB', buf)

        y += self.y_const

        print(f"[upstream] ppal: {x:.3f}, {y:.3f}, {z:.3f} | {yaw:.3f}, {pitch:.3f} | {ground}")

        buf = struct.pack('>dddffB', x, y, z, yaw, pitch, ground)
        self.upstream.send_packet('player_position_and_look', buf)

    def packet_upstream_player_position(self, buff):
        buf = buff.read()
        x, y, z, ground = struct.unpack('>dddB', buf)

        y += self.y_const

        print(f"[upstream] pp: {x:.3f}, {y:.3f}, {z:.3f} | {ground}")

        buf = struct.pack('>dddB', x, y, z, ground)
        self.upstream.send_packet('player_position', buf)

    def packet_upstream_chat_message(self, buff):
        buff.save()
        chat_message = buff.unpack_string()

        if chat_message.startswith(".fly"):
            self.y_const = 5
        
        if chat_message.startswith(".stopfly"):
            self.y_const = 0

        buff.restore()
        self.upstream.send_packet("chat_message", buff.read())

    # def packet_upstream_player_position_and_look(self, buff):
    #     buf = buff.read()
    #     x, y, z, yaw, pitch, ground = struct.unpack('>dddffB', buf)

    #     print(f"[upstream] ppal: {x:.3f}, {y:.3f}, {z:.3f} | {yaw:.3f}, {pitch:.3f} | {ground}")

    #     buf = struct.pack('>dddffB', x, y, z, yaw, pitch, ground)
    #     self.upstream.send_packet('player_position_and_look', buf)


    # def packet_downstream_player_position_and_look(self, buff):
    #     buf = buff.read()
    #     x, y, z, yaw, pitch, _, _, ground = struct.unpack('>dddffBBB', buf)

    # #     y += self.y_const

    #     print(f"[downstream] ppal:\t{x:.3f}, {y:.3f}, {z:.3f} | {yaw:.3f}, {pitch:.3f} | {ground}")

    #     buf = struct.pack('>dddffBBB', x, y, z, yaw, pitch, 0, 0, ground)
    #     self.downstream.send_packet('player_position_and_look', buf)

    

    # def packet_upstream_player_position(self, buff):
    #     buf = buff.read()
    #     x, y, z, ground = struct.unpack('>dddB', buf)

    #     print(f"[upstream] pp:\t{x:.3f}, {y:.3f}, {z:.3f} | {ground}")

    #     buf = struct.pack('>dddB', x, y, z, ground)
    #     self.upstream.send_packet('player_position', buf)


    # def packet_upstream_player_look(self, buff):
    #     buf = buff.read()
    #     yaw, pitch, ground = struct.unpack('>ffB', buf)

    #     print(f"[upstream] pl:\t{yaw:.3f}, {pitch:.3f} | {ground}")

    #     buf = struct.pack('>ffB', yaw, pitch, ground)
    #     self.upstream.send_packet('player_look', buf)


    # def packet_downstream_player_position_and_look(self, buff):
    #     buff.save()
    #     buf = buff.read()
    #     print(f"dppal:\t{buf.hex()}, {sys.getsizeof(buf)}")


    # def packet_upstream_player_position_and_look(self, buff):
    #     buf = buff.read()
    #     x, y, z, yaw, pitch, ground = struct.unpack('>dddffB', buf)

    #     y += self.y_const

    #     print(f"ppal: {x:2f}, {y:2f}, {z:2f} | {yaw:2f}, {pitch:2f} | {ground}")
    #     d_buf = struct.pack('>dddffBBB', x, y, z, yaw, pitch, 0, 0, ground)
    #     self.downstream.send_packet('player_position_and_look', d_buf)
    #     buf = struct.pack('>dddffB', x, y, z, yaw, pitch, ground)
    #     self.upstream.send_packet('player_position_and_look', buf)




    # def packet_upstream_player_position_and_look(self, buff):
    #     buff.save()
    #     buf = buff.read()
    #     x, y, z, yaw, pitch, ground = struct.unpack('>dddffB', buf)

    #     # if ground == 0:
    #     #     y += 1

    #     # print(f"ppal:\t{buf.hex()}, {sys.getsizeof(buf)}")

    #     # x, y, z, yaw, pitch, flags, teleport, dismount = struct.unpack('>dddffBBB', buf)

    #     print(f"ppal: {x}, {y}, {z} | {yaw}, {pitch} | {ground}")

    #     d_buf = struct.pack('>dddffBBB', x, y, z, yaw, pitch, 0, 0, 0)
    #     g_buf = struct.pack('>dddffB', x, y, z, yaw, pitch, ground)
    #     self.upstream.send_packet('player_position_and_look', g_buf)
    #     self.downstream.send_packet('player_position_and_look', d_buf)

    # def packet_upstream_player_position(self, buff):
    #     buff.save()
    #     buf = buff.read()
    #     print(f"pp:\t{buf.hex()}, {sys.getsizeof(buf)}")
    #     self.upstream.send_packet('player_position', buf)


    # def packet_upstream_player_look(self, buff):
    #     buff.save()
    #     buf = buff.read()
    #     print(f"pl:\t{buf.hex()}, {sys.getsizeof(buf)}")
    #     self.upstream.send_packet('player_look', buf)

    # def packet_upstream_player_position(self, buff):
    #     buf = buff.read()

    #     x, y, z, ground = struct.unpack('>dddB', buf)
    #     # y += 5

    #     print(f"player_position {x} / {y} / {z} | {ground}")

    #     yaw, pitch = self.orig_look
    #     flags = 0
    #     teleport = 0
    #     dismount = 0


    #     buf_pp = struct.pack('>dddB', x, y, z, ground)
    #     buf_ppal = struct.pack('>dddffBBB', x, y, z, yaw, pitch, flags, teleport, dismount)


    #     self.downstream.send_packet('player_position_and_look', buf_ppal)
    #     self.upstream.send_packet('player_position', buf_pp)


    # def packet_upstream_player_look(self, buff):
    #     buff.save()
    #     buf = buff.read()
    #     yaw, pitch, ground = struct.unpack('>ffB', buf)
    #     self.orig_look = (yaw, pitch, ground)
    #     buf = struct.pack('>ffB', yaw, pitch, ground)
    #     self.upstream.send_packet('player_look', buf)

    # def packet_upstream_player_position(self, buff):
    #     buff.save()
    #     buf = buff.read()
    #     x, y, z, ground = struct.unpack('>dddB', buf)



    #     print(f"player_position {x} / {y} / {z} | {ground}")

    #     print(self.orig_look)
    #     yaw, pitch, _ = self.orig_look

    #     flags = 0
    #     teleport = 0
    #     dismount = 0

    #     player_postion_buf = struct.pack('>dddffBBB', x, y, z, yaw, pitch, flags, teleport, dismount)
    #     buf = struct.pack('>dddB', x, y, z, ground)

    #     self.downstream.send_packet('player_position_and_look', player_postion_buf)
    #     self.upstream.send_packet('player_position', buf)

    # def packet_upstream_entity_action(self, buff):
    #     buf = buff.read()
    #     print(f"entity action: {buf.hex()}")
    #     crouch_start, crouch_end = 
    #     self.upstream.send_packet("entity_action", buf)

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