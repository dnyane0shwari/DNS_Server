import tkinter as tk
from tkinter import ttk, StringVar, messagebox
import socket

class DNSClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("DNS Client")

        style = ttk.Style()
        style.configure("TFrame", background="#333")
        style.configure("TLabel", background="#333", foreground="#fff", font=("Arial", 16))
        style.configure("TButton", font=("Arial", 16, "bold"), foreground="#fff", relief="flat")

        self.frame = ttk.Frame(master, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.domain_label = ttk.Label(self.frame, text="Enter the domain name to resolve:")
        self.domain_label.grid(row=0, column=0, pady=20, padx=20, sticky=tk.W)

        self.domain_entry = ttk.Entry(self.frame, font=("Arial", 16))
        self.domain_entry.grid(row=1, column=0, pady=20, padx=20, sticky=(tk.W, tk.E))

        self.resolve_button = ttk.Button(self.frame, text="Resolve", command=self.resolve_domain)
        self.resolve_button.grid(row=2, column=0, pady=20, padx=20, sticky=tk.W + tk.E)

        self.result_var = StringVar()
        self.result_label = ttk.Label(self.frame, textvariable=self.result_var, font=("Arial", 16))
        self.result_label.grid(row=3, column=0, pady=20, padx=20, sticky=tk.W)

    def resolve_domain(self):
        try:
            # Get the domain name from the entry widget
            domain_name = self.domain_entry.get()
            print(f"Sending request for {domain_name}")  # Debugging line

            # Define the DNS server address and port
            server_address = ('127.0.0.1', 12345)

            # Create a UDP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Send the domain name to the DNS server
            client_socket.sendto(domain_name.encode(), server_address)

            # Receive the response from the DNS server
            response_data, _ = client_socket.recvfrom(1024)
            print(f"Received response: {response_data.decode()}")  # Debugging line

            # Display the resolved IP addresses
            self.result_var.set(f"Resolved IP addresses: {response_data.decode()}")

            # Close the socket
            client_socket.close()

        except Exception as e:
            # Display an error message if an exception occurs
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            print(f"Exception occurred: {str(e)}")  # Debugging line

if __name__ == "__main__":
    root = tk.Tk()
    app = DNSClientGUI(root)
    root.mainloop()
