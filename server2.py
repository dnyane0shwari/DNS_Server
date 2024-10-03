import socket
import dns.resolver

def start_dns_server():
    server_address = ('127.0.0.1', 12345)  # You can change this to another port if needed
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        server_socket.bind(server_address)
        print(f"DNS server listening on {server_address}")
    except Exception as e:
        print(f"Error binding server: {e}")
        return

    while True:
        print("Waiting for requests...")
        try:
            data, client_address = server_socket.recvfrom(1024)
            domain_name = data.decode()
            print(f"Received request for {domain_name} from {client_address}")

            try:
                answers = dns.resolver.resolve(domain_name, 'A')
                ip_addresses = [answer.address for answer in answers]
                print(f"Resolved {domain_name} to {', '.join(ip_addresses)}")
                server_socket.sendto(', '.join(ip_addresses).encode(), client_address)
            except dns.resolver.NXDOMAIN:
                print(f"Invalid domain provided: {domain_name} from {client_address}")
                server_socket.sendto(b"Invalid domain", client_address)
            except Exception as e:
                print(f"Error resolving domain: {e}")
                server_socket.sendto(b"Error resolving domain", client_address)

        except Exception as e:
            print(f"Error receiving data: {e}")

if __name__ == "__main__":
    print("Starting DNS server...")
    start_dns_server()
