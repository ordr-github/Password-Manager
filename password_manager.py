from cryptography.fernet import Fernet   #Crpytography module to encrypt the passwords present in the text file
import os.path  #Provides functions for paths

#Generates Key
def write_key():
    key = Fernet.generate_key()
    with open("key.key","wb") as key_file: 
        key_file.write(key)
        
        
#Loads the Key        
def load_key():
    with open("key.key", "rb") as key_file: 
        key = key_file.read()
    return key

# Function to view Passwords Stored
def view(fer):
    try:
        with open("passwords.txt", "r") as f:
            for line in f.readlines():
                data = line.rstrip()  # Strips new line '\n' escape character
                user, passw = data.split("|")
                try:
                    decrypted_pass = fer.decrypt(passw.encode()).decode() #Decrpytion of passwords
                    print("User:", user, "| Password:", decrypted_pass)
                except Exception as e:
                    if isinstance(e, (ValueError, TypeError)):
                        print(f"Error decrypting password for user {user}: Incorrect key or password")
    except Exception as e:
        print("Error reading passwords file:", e)


# Function to add Passwords
def add(fer):
    try:
        name = input("Account Name: ")
        pwd = input("Password: ")
        encrypted_pwd = fer.encrypt(pwd.encode()).decode() #Encryption of passwords
        with open('passwords.txt', 'a') as f:
            f.write(name + "|" + encrypted_pwd + "\n")
    except Exception as e:
        print("Error adding password:", e)




# Main Function
def main():
    try:
        if not os.path.exists("key.key"):
            write_key()
            print("Key generated successfully.")

        key = load_key()
        master_pwd = input("What is the master password? ")
        key_with_pwd = key + master_pwd.encode() #Combines key and encode master password to generate a key with passwords
        fer = Fernet(key_with_pwd)

        while True:
            mode = input("Would you like to add a new password or view existing ones (view, add), press q to quit?\n").lower()
            if mode == "q":
                break
            elif mode == "view":
                view(fer)
            elif mode == "add":
                add(fer)
            else:
                print("Invalid mode.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":     
    main()
