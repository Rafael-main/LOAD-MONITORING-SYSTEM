import bcrypt


class Secreto:

    def to_process(self, password):
        self.process_input = (str(password) * 10).encode()
        return self.process_input

    def to_hash(self, password):
        self.password_to_hashed = self.to_process(password)
        self.hashed = bcrypt.hashpw(self.password_to_hashed, bcrypt.gensalt())
        return self.hashed

    def check_hash(self, password, hashed):
        if bcrypt.checkpw(password, hashed):
            return True
        return False


if __name__ == "__main__":
    Secreto()
