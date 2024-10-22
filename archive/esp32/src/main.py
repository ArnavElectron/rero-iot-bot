# This code runs on the ESP32

import network
import socket

# from reroBot import *

# Get server host IP and replace here
# Or set HOST = '' and PORT = None
HOST: str = ""
PORT: int = 65432

# Replace with SSID and PASSWORD
# Or set SSID = '' and PASSWORD = ''
SSID: str = ""
PASS: str = ""


def scanForNetworks(wlan: network.WLAN) -> list:
    """
    Scans for available Wi-Fi networks and returns a list of SSIDs.
    """
    networks = wlan.scan()
    ssid_list = []
    for net in networks:
        if net[0]:
            ssid_list.append(net[0].decode("utf-8"))
    return ssid_list


def connectToNetwork(wlan: network.WLAN, ssid: str, password: str) -> str:
    """
    Connects to a Wi-Fi network with the specified SSID and password.
    Returns the IP address of ESP32.
    """
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
        return list(wlan.ifconfig())[0]


def executeCode(conn: socket.socket) -> None:
    """
    Continuously receives and executes Python code from the server connection.
    """
    while True:
        data = conn.recv(1024)
        data = data.decode("utf-8")
        if data:
            print(f"\nCode Received : {data}")
            print("Executing...")
            try:
                exec(data)
            except Exception as e:
                print(f"{type(e).__name__} : {e}")


def main() -> None:

    global SSID, PASS, HOST, PORT

    print("\nWelcome to ReRo Bot :)")

    print("\nQuit the client anytime using CTRL-C")

    try:

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        print("\nScanning for networks...")
        networks = scanForNetworks(wlan)

        print("\nFound networks:")
        for ssid in networks:
            print(f"\t{ssid}")

        if SSID == "" or PASS == "":
            SSID = input("\nWiFi: ")
            PASS = input("Password : ")

        print(f"\nConnecting to {SSID}...")
        IP = connectToNetwork(wlan, SSID, PASS)

        if IP:
            print(f"\nConnected to {SSID}!")
            print(f"\nIP Address : {IP}")

        if HOST == "" or PORT is None:
            HOST = input("\nServer Host: ")
            PASS = input("Server Port : ")

        print(f"\nSetting up TCP connection to {HOST}:{PORT}...")
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST, PORT))

        print(f"\nConnected to {HOST}:{PORT}...")
        executeCode(conn)

    except KeyboardInterrupt:
        print("\nExiting...")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

    finally:
        try:
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
