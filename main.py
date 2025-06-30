def intercept_profile_picture(data):
    print(f"[Profile Picture] {data.hex()}")
    return data

if __name__ == "__main__":
    import asyncio
    from filters import Filters, DIR_C2S, DIR_S2C
    from proxy import Proxy

    Filters.register(DIR_C2S, b'.*', Filters.Mode.REGEX, lambda d: print(f"[C2S] {d.hex(); return d}"))
    Filters.register(DIR_S2C, b'.*', Filters.Mode.REGEX, lambda d: print(f"[S2C] {d.hex(); return d}"))

    Filters.register(DIR_C2S, b'\xTODO', Filters.Mode.BYTES, intercept_profile_picture)

    proxy = Proxy("127.0.0.1", 13377, "TODO", 23001)
    asyncio.run(proxy.start())
