import hashlib
import time
class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.hash_current()
    def hash_current(self):
        current_data = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(current_data.encode()).hexdigest()
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")
    def get_latest_block(self):
        return self.chain[-1]
    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)
    def proof_of_work(self, block):
        block.nonce = 0
        target = '0' * self.difficulty
        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = block.hash_current()
        return block.hash
    def chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.hash_current():
                print(f"Block {current_block.index} has an invalid hash.")
                return False
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {current_block.index} has an incorrect previous hash.")
                return False
            if not current_block.hash.startswith('0' * self.difficulty):
                print(f"Block {current_block.index} does not satisfy proof-of-work.")
                return False
        return True
    def display_chain(self):
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {block.transactions}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print(f"Nonce: {block.nonce}")
            print("---------------")
def get_user_transactions():
    transactions = []
    while True:
        transaction = input("Enter a transaction (or 'done' to finish): ")
        if transaction == 'done':
            break
        transactions.append(transaction)
    return transactions
def mine_new_block(blockchain):
    transactions = get_user_transactions()
    new_block = Block(len(blockchain.chain), transactions, blockchain.get_latest_block().hash)
    blockchain.add_block(new_block)
    print("Block mined and added to the blockchain!")
def display_blockchain_state(blockchain):
    print("\nCurrent state of the blockchain:")
    blockchain.display_chain()
def main():
    blockchain_instance = Blockchain()
    while True:
        print("\n1. Add transactions and mine a new block")
        print("2. View blockchain")
        print("3. Verify blockchain integrity")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            mine_new_block(blockchain_instance)
        elif choice == '2':
            display_blockchain_state(blockchain_instance)
        elif choice == '3':
            if blockchain_instance.chain_valid():
                print("The blockchain is valid.")
            else:
                print("The blockchain is invalid.")
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")
if __name__ == "__main__":
    main()
