import json
import random
import string

def generate_password(length=12):
    """Generate a random password of specified length"""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def add_user(username):
    """Add a new user with a generated password to data.json"""
    # Generate password
    password = generate_password()
    
    # Load existing data
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    # Add new user
    data[username] = password
    
    # Save updated data
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    return password

if __name__ == "__main__":
    # Example usage when run directly
    username = input("Enter username: ")
    password = add_user(username)
    print(f"User {username} added with password: {password}")