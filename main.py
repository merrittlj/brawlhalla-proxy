if __name__ == "__main__":
    import asyncio
    from filters import Filters, DIR_C2S, DIR_S2C
    from proxy import Proxy

    Filters.register(DIR_C2S, b'.*', Filters.Mode.REGEX, lambda d: print(f"[C2S] {d.hex()}"))
    Filters.register(DIR_S2C, b'.*', Filters.Mode.REGEX, lambda d: print(f"[S2C] {d.hex()}"))

    proxy = Proxy("127.0.0.1", 13377, "server.ip", 23001)
    asyncio.run(proxy.start())
