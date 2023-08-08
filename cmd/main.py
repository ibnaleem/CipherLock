import os, sys
from rich.console import Console
from rich.table import Table
from rich.style import Style
from cryptography.fernet import Fernet

red_bold = Style(color="red", blink=True, bold=True)
ascii_art = '''

 ▄████▄   ██▓ ██▓███   ██░ ██ ▓█████  ██▀███   ██▓     ▒█████   ▄████▄   ██ ▄█▀
▒██▀ ▀█  ▓██▒▓██░  ██▒▓██░ ██▒▓█   ▀ ▓██ ▒ ██▒▓██▒    ▒██▒  ██▒▒██▀ ▀█   ██▄█▒ 
▒▓█    ▄ ▒██▒▓██░ ██▓▒▒██▀▀██░▒███   ▓██ ░▄█ ▒▒██░    ▒██░  ██▒▒▓█    ▄ ▓███▄░ 
▒▓▓▄ ▄██▒░██░▒██▄█▓▒ ▒░▓█ ░██ ▒▓█  ▄ ▒██▀▀█▄  ▒██░    ▒██   ██░▒▓▓▄ ▄██▒▓██ █▄ 
▒ ▓███▀ ░░██░▒██▒ ░  ░░▓█▒░██▓░▒████▒░██▓ ▒██▒░██████▒░ ████▓▒░▒ ▓███▀ ░▒██▒ █▄
░ ░▒ ▒  ░░▓  ▒▓▒░ ░  ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░▓  ░░ ▒░▒░▒░ ░ ░▒ ▒  ░▒ ▒▒ ▓▒
  ░  ▒    ▒ ░░▒ ░      ▒ ░▒░ ░ ░ ░  ░  ░▒ ░ ▒░░ ░ ▒  ░  ░ ▒ ▒░   ░  ▒   ░ ░▒ ▒░
░         ▒ ░░░        ░  ░░ ░   ░     ░░   ░   ░ ░   ░ ░ ░ ▒  ░        ░ ░░ ░ 
░ ░       ░            ░  ░  ░   ░  ░   ░         ░  ░    ░ ░  ░ ░      ░  ░   
░                                                              ░               
'''

key = Fernet.generate_key()
cipher_suite = Fernet(key)

encrypted_items = []

def encrypt_item(path):
  with open(path, "rb") as file:
    data = file.read()
    encrypted_data = cipher_suite.encrypt(data)
    
    encrypted_path = f"encrypted_{os.path.basename(path)}"
    with open(encrypted_path, "wb") as encrypted_file:
      encrypted_file.write(encrypted_data)
    
    encrypted_items.append(encrypted_path)
    return encrypted_path
  
def decrypt_item(encrypted_path):
  with open(encrypted_path, "rb") as encrypted_file:
    encrypted_data = encrypted_file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    
    decrypted_path = f"decrypted_{os.path.basename(encrypted_path)}"
    with open(decrypted_path, "wb") as decrypted_file:
      decrypted_file.write(decrypted_data)
    
    return decrypted_path
  
def main_menu():
  console = Console()

  while True:
    os.system("clear" if not os.name == 'nt' else "cls")
    console.print(ascii_art, justify="center", style="#D3869B bold")
    console.print("[cyan]:: Encrypt Your Files & Directories | Run with Admin Perms ::[cyan]\n", justify="center", end="")
    console.print("1. Encrypt Files      2. Show Encrypted Items     3. Decrypt Files     4. Exit", justify="center")
        
    choice = input("Enter your choice: ")

    if choice == "1":
      path = input("Enter the path of the file to encrypt: ")
      if os.path.exists(path):
        encrypted_path = encrypt_item(path)
        console.print(f"{path} encrypted and saved as {encrypted_path}", style="green")
        input("Press Enter to continue...")
      else:
        console.print("File not found.", style=red_bold)
        input("Press Enter to continue...")