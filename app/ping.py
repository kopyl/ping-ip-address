import socket

def ping(host, port, timeout=3):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            return True
        else:
            return False
    except socket.gaierror:
        print(f"Could not resolve hostname: {host}")
        return False
    except socket.error as e:
        print(f"Connection to {host} port {port} [tcp] failed: {e}")
        return False