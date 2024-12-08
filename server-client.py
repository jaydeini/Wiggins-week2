import socket
import traceback

def start_client(host='localhost', port=135, message='Hello, Server!'):
    """
    Create a socket client that connects to a server and sends a message.
    
    Args:
        host (str): Server host IP address. Defaults to localhost.
        port (int): Server port number. Defaults to 65432.
        message (str): Message to send to the server.
    """
    try:
        # Create a socket object using IPv4 (AF_INET) and TCP (SOCK_STREAM)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Set a timeout to prevent indefinite waiting
            client_socket.settimeout(10)
            
            # Attempt to connect to the server
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")
            
            # Send message to the server
            client_socket.send(message.encode('utf-8'))
            print(f"Sent message: {message}")
            
            # Receive response from the server
            response = client_socket.recv(135).decode('utf-8')
            print(f"Server response: {response}")

    except socket.timeout:
        print("Connection timed out. The server might be unavailable.")
    except ConnectionRefusedError:
        print("Connection was refused. Ensure the server is running.")
    except socket.error as sock_err:
        print(f"Socket Error: {sock_err}")
        traceback.print_exc()
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    start_client()