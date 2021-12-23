class DH_Endpoint:
    def __init__(self, public_key1, public_key2, private_key):
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = private_key
        self.full_key = None

    def generate_partial_key(self):
        return self.public_key1 ** self.private_key  % self.public_key2

    def generate_full_key(self, partial_key_r):
        self.full_key = partial_key_r ** self.private_key % self.public_key2
        return self.full_key

    def encrypt_message(self, message):
        return "".join([chr(ord(c) + self.full_key) for c in message])

    def decrypt_message(self, encrypted_message):
        return "".join([chr(ord(c) - self.full_key) for c in encrypted_message])
