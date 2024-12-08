import socket
import traceback

def start_server(host='localhost', port=65432):
    """
    Start a socket server that listens for incoming connections
    and handles client messages.
    
    Args:
        host (str): Host IP address to bind the server. Defaults to localhost.
        port (int): Port number to listen on. Defaults to 65432.
    """
    try:
        # Create a socket object using IPv4 (AF_INET) and TCP (SOCK_STREAM)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Allow socket reuse to prevent "Address already in use" errors
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind the socket to a specific network interface and port
            server_socket.bind((host, port))
            
            # Listen for incoming connections (max 1 queued connection)
            server_socket.listen(1)
            
            print(f"Server listening on {host}:{port}")
            
            while True:
                # Wait for and accept a client connection
                client_socket, client_address = server_socket.accept()
                
                with client_socket:
                    print(f"Connection established with {client_address}")
                    
                    # Receive data from the client
                    data = client_socket.recv(1024).decode('utf-8')
                    
                    # Process and respond to the client
                    response = f"Server received: {data}"
                    client_socket.send(response.encode('utf-8'))
                    
                    print(f"Sent response to {client_address}")

    except socket.error as sock_err:
        print(f"Socket Error: {sock_err}")
        traceback.print_exc()
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    start_server()