import socket
import ipaddress
import concurrent.futures
from typing import List, Tuple, Optional

class PortScanner:
    def __init__(self, target: str, min_port: int = 1, max_port: int = 1024, timeout: float = 1.0):
        """
        Initialize the Port Scanner with target host and port range.
        
        Args:
            target (str): IP address or hostname to scan
            min_port (int): Minimum port number to scan (default: 1)
            max_port (int): Maximum port number to scan (default: 1024)
            timeout (float): Connection timeout in seconds (default: 1.0)
        """
        try:
            # Resolve hostname to IP address if needed
            self.target = socket.gethostbyname(target)
            self.min_port = max(1, min_port)
            self.max_port = min(max_port, 65535)
            self.timeout = timeout
        except socket.gaierror:
            raise ValueError(f"Invalid target: {target}")

    def scan_port(self, port: int) -> Optional[Tuple[int, str]]:
        """
        Attempt to connect to a specific port.
        
        Args:
            port (int): Port number to scan
        
        Returns:
            Tuple of (port, service name) if open, None otherwise
        """
        try:
            # Create a new socket for each connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Set socket timeout
                sock.settimeout(self.timeout)
                
                # Attempt to connect to the port
                result = sock.connect_ex((self.target, port))
                
                # Check if connection was successful
                if result == 0:
                    # Try to determine service name (best effort)
                    try:
                        service = socket.getservbyport(port)
                    except OSError:
                        service = "Unknown"
                    
                    return port, service
        
        except (socket.timeout, socket.error):
            # Silently handle connection errors
            pass
        
        return None

    def scan(self, max_workers: int = 100) -> List[Tuple[int, str]]:
        """
        Perform port scan using concurrent connections.
        
        Args:
            max_workers (int): Maximum number of concurrent threads
        
        Returns:
            List of open ports with their services
        """
        open_ports = []
        
        # Use ThreadPoolExecutor for concurrent scanning
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create futures for all ports in the specified range
            futures = {
                executor.submit(self.scan_port, port): port 
                for port in range(self.min_port, self.max_port + 1)
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
        
        # Sort open ports numerically
        return sorted(open_ports, key=lambda x: x[0])

def main():
    """
    Example usage of the PortScanner class.
    """
    try:
        # Example target and port range
        target = "scanme.nmap.org"
        
        # Create scanner instance
        scanner = PortScanner(
            target, 
            min_port=1, 
            max_port=1000, 
            timeout=1.0
        )
        
        # Perform scan
        print(f"Scanning {target} for open ports...")
        open_ports = scanner.scan()
        
        # Display results
        if open_ports:
            print("\nOpen Ports:")
            for port, service in open_ports:
                print(f"Port {port}: {service}")
        else:
            print("No open ports found.")
    
    except Exception as e:
        print(f"Scan failed: {e}")

if __name__ == "__main__":
    main()