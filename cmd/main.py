import os, sys, hashlib
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from rich.console import Console
from rich.table import Table
from rich.style import Style

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


def encrypt_item(path, password):
  with open(path, "wb") as file:
    
    # Read data
    data = file.read()
    
    # Generate a random salt
    salt = get_random_bytes(AES.block_size)

    # Use Scrypt KDF to create a private key from the password
    private_key = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # Create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # Encrypt data
    encrypted_data, tag = cipher_config.encrypt_and_digest(bytes(data, 'utf-8'))

    with open(path, "wb") as encrypted_file:  # Open the original file for writing
        encrypted_file.write(salt + tag + encrypted_data)

  
def decrypt_item(path, password):
  with open(path, "rb") as encrypted_file:

    # Read data
    encrypted_data = encrypted_file.read()

    salt = encrypted_data[:AES.block_size] # Obtain salt
    tag = encrypted_data[AES.block_size:AES.block_size+16] # Obtain tag
    ciphertext = encrypted_data[AES.block_size+16] # Obtain ciphertext

    # Use Scrypt KDF to obtain a private key from the password
    private_key = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

  
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

    elif choice == "2":
      os.system("clear" if not os.name == 'nt' else "cls")
      console.print(ascii_art, justify="center", style="#D3869B bold")
      console.print("[cyan]:: Encrypted Items ::[cyan]\n", justify="center", end="")
      terminal_width = console.width

      table = Table(show_header=True, header_style="bold magenta")
      table.add_column("File", style="dim", width=int(terminal_width * 0.5), justify="center")
      table.add_column("Status", style="dim", width=int(terminal_width * 0.5), justify="center")
      for item in encrypted_items:
        table.add_row(item, "Encrypted", style="green")
      console.print(table)
      input("\nPress Enter to continue...")

    if choice == "3":
      os.system("clear" if not os.name == 'nt' else "cls")
      console.print(ascii_art, justify="center", style="#D3869B bold")
      console.print("[cyan]:: Decrypt Items ::[cyan]\n", justify="center", end="")
    
      for idx, item in enumerate(encrypted_items):
        console.print(f"{idx + 1}. {item}")
    
      decrypt_choice = input("Enter the number of the item to decrypt: ")
    
      if decrypt_choice.isdigit() and int(decrypt_choice) >= 1 and int(decrypt_choice) <= len(encrypted_items):
        item_index = int(decrypt_choice) - 1
        decrypted_path = decrypt_item(encrypted_items[item_index])
        console.print(f"{encrypted_items[item_index]} decrypted and saved as {decrypted_path}", style="green")
        input("Press Enter to continue...")

    elif choice == "4":
      sys.exit(0)
    else:
      console.print("Invalid choice. Please choose a valid option.", style=red_bold)
      input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()