# Dictionary to store usernames and passwords
user_credentials = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3'
}

def login():
    # Get username and password from the user
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Check if the entered username exists in the dictionary
    if username in user_credentials:
        # Check if the entered password matches the stored password
        if user_credentials[username] == password:
            print("Login successful!")
        else:
            print("Incorrect password. Please try again.")
    else:
        print("Username not found. Please try again.")

# Main program loop
while True:
    print("Welcome to the Simple Login System")
    print("1. Login")
    print("2. Exit")
    
    choice = input("Enter your choice (1/2): ")
    
    if choice == '1':
        login()
    elif choice == '2':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please choose 1 or 2.")
