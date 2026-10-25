import os
import sys
import base64
import hashlib
from cryptography.fernet import Fernet
import subprocess
import csv

def decrypt():
    file_input = "credentials.csv"

    files = [f.strip() for f in file_input.split(',') if f.strip()]

    print(files)

    decryption_input = input("Enter the decryption key (paste key or passphrase): ").strip()

    try:
        decoded = base64.urlsafe_b64decode(decryption_input)
        if len(decoded) == 32:
            key = decryption_input.encode()
        else:
            raise ValueError("not 32 bytes")
    except Exception:
        key = base64.urlsafe_b64encode(hashlib.sha256(decryption_input.encode()).digest())

    try:
        for file in files:
            with open(file, "rb") as thefile:
                contents = thefile.read()
                contents_decrypted = Fernet(key).decrypt(contents)
            with open(file, "wb") as thefile:
                thefile.write(contents_decrypted)
                print("Your file(s) have been decrypted!")
    except Exception as e:
        print("Decryption failed:", e)

def encrypt():
    file_input = "credentials.csv"

    files = [f.strip() for f in file_input.split(',') if f.strip()]

    if not os.path.isfile(file_input):
        print(f"File(s) not found: {file_input}")
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit()

    print(files)

    key = input("Enter a password or type 'g' to generate one: ").strip()

    if key.lower() == "g":
        key = Fernet.generate_key()
        keyName = input("The name of the key: ")

        with open(keyName + ".txt", "wb") as decryption_key:
            decryption_key.write(key)

    else:
        try:
            decoded = base64.urlsafe_b64decode(key)
            if len(decoded) == 32:
                key = key.encode()
            else:
                raise ValueError("not 32 bytes")
        except Exception:
            key = base64.urlsafe_b64encode(hashlib.sha256(key.encode()).digest())
                
            for file in files:
                with open(file, "rb") as thefile:
                    contents = thefile.read()
                contents_encrypted = Fernet(key).encrypt(contents)
                with open(file, "wb") as thefile:
                    thefile.write(contents_encrypted)

            print("File(s) encrypted successfully!")
        else:
            print("Encryption canceled.")
        
if os.path.isfile("credentials.csv"):
    decrypt()

else:
    open('credentials.csv', 'x')
    a = 1

menu = '''#########################
1 - Add an entry.
2 - Show entries.
3 - Show and grep entry.
#########################
'''

print(menu)
option = int(input("Choose option: "))

if option == 1:
    user = input("Name: ")
    uname = input("Username: ")
    password = input("Password: ")
    url = input("URL: ")

    with open("credentials.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([user, uname, password, url])

    encrypt()
    
if option == 2:
    with open("credentials.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
    encrypt()
        
if option == 3:
    query = input("Search: ")

    with open("credentials.csv", "r") as f:
        reader = csv.reader(f)
        found = False
        for row in reader:
            if any(query.lower() in field.lower() for field in row):
                print(f"Name={row[0]}, Username={row[1]}, Password={row[2]}, URL={row[3]}")
                found = True
    
            if not found:
                print("No match found")
                
    encrypt()
    
