from data_structures import LinkedQueue
from data_structures import LinkedStack

class Transaction:
    def __init__(self, timestamp, from_user, to_user):
        self.timestamp = timestamp
        self.from_user = from_user
        self.to_user = to_user
        self.signature = None
    
    def sign(self):
        """
        Analyse your time complexity of this method.
        """
        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"

        # Adding transaction details into str
        str_bytes_notes = str(self.timestamp) + "|" + self.from_user + "|" + self.to_user

        swe_trns_seed = 0x1f123bb5a7c94d3f # Random seed
        for ch in str_bytes_notes:
            swe_trns_seed = (swe_trns_seed * 131) ^ ord(ch)
            swe_trns_seed = swe_trns_seed + 17

        # Char to int
        pin_raw = ""
        while swe_trns_seed > 0:
            ans = swe_trns_seed % 36
            pin = ALPHABET[ans]
            swe_trns_seed = swe_trns_seed // 36
            pin_raw = pin + pin_raw

        # 4. Fix length to 37
        while len(pin_raw) < 37:
            pin_raw = "0" + pin_raw
        if len(pin_raw) > 37:
            pin_raw = pin_raw[-37:]  

        self.signature = pin_raw
        # print(f"Transaction signed: {self.signature}") # For debugging


class ProcessingLine:
    def __init__(self, critical_transaction):
        """
        Analyse your time complexity of this method.
        """

        # Variables for the ProcessingLine task.
        self.critical_transaction = critical_transaction
        self.Queue_for_left = LinkedQueue()
        self.Stack_for_right = LinkedStack()
        self._fixed_pointer = False

    def add_transaction(self, transaction):
        """
        Analyse your time complexity of this method.
        """
        if transaction.timestamp <= self.critical_transaction.timestamp:
            self.Queue_for_left.append(transaction)
        elif transaction.timestamp > self.critical_transaction.timestamp:
            self.Stack_for_right.push(transaction)
        else:
            return RuntimeError("Cannot add more transactions.")

    def __iter__(self):
        if self._fixed_pointer:
            raise RuntimeError("Iterator already in use.")
        self._fixed_pointer = True
        return LineIterator(self)

class LineIterator:
    def __init__(self, pointer1):
        self.pointer1 = pointer1
        self.side = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.side == 0:
            if not self.pointer1.Queue_for_left.is_empty():
                tx = self.pointer1.Queue_for_left.serve()
                tx.sign()
                return tx
            else:
                self.side = 1
        
        if self.side == 1:
            self.side = 2
            tx = self.pointer1.critical_transaction
            tx.sign()
            return tx

        if self.side == 2:
            if not self.pointer1.Stack_for_right.is_empty():
                tx = self.pointer1.Stack_for_right.pop()
                tx.sign()
                return tx
            else:
                self.side = 3


        raise StopIteration


if __name__ == "__main__":
    # Write tests for your code here...
    # We are not grading your tests, but we will grade your code with our own tests!
    # So writing tests is a good idea to ensure your code works as expected.
    
    # Here's something to get you started...
    transaction1 = Transaction(50, "alice", "bob")
    transaction2 = Transaction(100, "bob", "dave")
    transaction3 = Transaction(120, "dave", "frank")

    line = ProcessingLine(transaction2)
    line.add_transaction(transaction3)
    line.add_transaction(transaction1)

    print("Let's print the transactions... Make sure the signatures aren't empty!")
    line_iterator = iter(line)
    while True:
        try:
            transaction = next(line_iterator)
            print(f"Processed transaction: {transaction.from_user} -> {transaction.to_user}, "
                  f"Time: {transaction.timestamp}\nSignature: {transaction.signature}")
        except StopIteration:
            break

    # Task 1.1: Signature checks Testing for myself.
    # t1 = Transaction(123, "alice", "bob")
    # t1.sign()
    # assert len(t1.signature) == 37

    # t2 = Transaction(123, "alice", "bob")
    # t2.sign()
    # assert t1.signature == t2.signature   # deterministic

    # t3 = Transaction(124, "alice", "bob")
    # t3.sign()
    # assert t1.signature != t3.signature   # sensitivity

    # print("Task 1.1 signature checks passed ✅")
