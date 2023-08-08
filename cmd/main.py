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