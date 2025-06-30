import asyncio
from filters import Filters, DIR_C2S, DIR_S2C

class Proxy:
    def __init__(self, local_host, local_port, remote_host, remote_port):
        self.local_host = local_host
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port

    async def start(self):
        server = await asyncio.start_server(
            self.handle_connection, self.local_host, self.local_port
        )
        print(f"[+] Proxy listening on port {self.local_port}")
        async with server:
            await server.serve_forever()

    async def pipe(src_reader, dst_writer, direction):
        try:
            while not src_reader.at_eof():
                data = await src_reader.read(4096)
                if not data:
                    break
                data = Filters.apply(direction, data)
                dst_writer.write(data)
                await dst_writer.drain()
        except Exception as e:
            print(f"Pipe error [{direction}]:", e)
        finally:
            dst_writer.close()
            await dst_writer.wait_closed()

    async def handle_connection(self, reader_c2p, writer_c2p):
        try:
            reader_p2s, writer_p2s = await asyncio.open_connection(self.remote_host, self.remote_port)
            await asyncio.gather(
                pipe(reader_c2p, writer_p2s, DIR_C2S),
                pipe(reader_p2s, writer_c2p, DIR_S2C)
            )
        except Exception as e:
            print("Connection error:", e)
            writer.close()

