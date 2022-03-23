import asyncio
from bleak import BleakScanner, BleakClient

MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"

async def main(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

        services = await client.get_services()
        for service in services:
            print(service)
            chars = service.characteristics
            for char in chars:
                print("char:")
                print(char)

async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == None:
            continue

        print("Found: " + d.name)

        if "Hue color" in d.name:
            await main(d.address)
            break

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
