import os

def encrypt(shift1, shift2):
   
    try:
        with open("raw_text.txt", "r") as infile, open("encrypted_text.txt", "w") as outfile:
            raw_text = infile.read()
            
            for char in raw_text:
                encrypted_char, tag = encrypt_char(char, shift1, shift2)
                outfile.write(f"{encrypted_char},{tag}\n")

        print("Encryption complete. Output saved to 'encrypted_text.txt'.")

    except FileNotFoundError:
        print("Error: 'raw_text.txt' not found. Please create this file.")
        if not os.path.exists("raw_text.txt"):
            with open("raw_text.txt", "w") as f:
                f.write("This is a sample text file for testing purposes.")
            print("A sample 'raw_text.txt' has been created for you.")
            encrypt(shift1, shift2)

def encrypt_char(char, n, m):
    if char == '\n':
        return '[NL]', 'nl'
    elif 'a' <= char <= 'm':
        return chr((ord(char) - ord('a') + n * m) % 26 + ord('a')), 'lm'
    elif 'n' <= char <= 'z':
        return chr((ord(char) - ord('a') - (n + m)) % 26 + ord('a')), 'nz'
    elif 'A' <= char <= 'M':
        return chr((ord(char) - ord('A') - n) % 26 + ord('A')), 'AM'
    elif 'N' <= char <= 'Z':
        return chr((ord(char) - ord('A') + m**2) % 26 + ord('A')), 'NZ'
    else:
        return char, 'sp'

def decrypt(shift1, shift2):
    try:
        with open("encrypted_text.txt", "r") as infile, open("decrypted_text.txt", "w") as outfile:
            decrypted_chars = []
            for line in infile:
                line = line.rstrip('\n')
                if not line:
                    continue
                parts = line.rsplit(',', 1)
                encrypted_char = parts[0]
                tag = parts[1]
                
                decrypted_char = decrypt_char(encrypted_char, tag, shift1, shift2)
                decrypted_chars.append(decrypted_char)
            
            outfile.write("".join(decrypted_chars))

        print("Decryption complete. Output saved to 'decrypted_text.txt'.")

    except FileNotFoundError:
        print("Error: 'encrypted_text.txt' not found. Please run encryption first.")
    except IndexError:
        print("Error: 'encrypted_text.txt' appears to be corrupted or in the wrong format.")


def decrypt_char(char, tag, n, m):
    if tag == 'nl':
        return '\n'
    elif tag == 'lm':
        return chr((ord(char) - ord('a') - n * m) % 26 + ord('a'))
    elif tag == 'nz':
        return chr((ord(char) - ord('a') + (n + m)) % 26 + ord('a'))
    elif tag == 'AM':
        return chr((ord(char) - ord('A') + n) % 26 + ord('A'))
    elif tag == 'NZ':
        return chr((ord(char) - ord('A') - m**2) % 26 + ord('A'))
    else: # This will be 'sp'
        return char

def verify():
    try:
        with open("raw_text.txt", "r") as file1, open("decrypted_text.txt", "r") as file2:
            original_content = file1.read()
            decrypted_content = file2.read()
            
        if original_content == decrypted_content:
            print("\nVerification successful: The decrypted text perfectly matches the original.")
        else:
            print("\nVerification FAILED: The decrypted text does not match the original.")
            
    except FileNotFoundError:
        print("Error: Could not find 'raw_text.txt' or 'decrypted_text.txt' for verification.")

def main():
    print("--- File Encryption/Decryption Program (No JSON) ---")
    try:
        shift1 = int(input("Enter the first shift value (integer): "))
        shift2 = int(input("Enter the second shift value (integer): "))
    except ValueError:
        print("Invalid input. Please enter integers for shift values.")
        return

    encrypt(shift1, shift2)
    decrypt(shift1, shift2)
    verify()

if __name__ == "__main__":
    main()

