from data_structures import ArrayR
from processing_line import Transaction


class ProcessingBook:
    LEGAL_CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789"

    def __init__(self, level=0, root=None):
        self.pages = ArrayR(len(ProcessingBook.LEGAL_CHARACTERS))
        self._size = 0 # 2.3 Task
        self.error_count = 0
        self.level = level
        if root is None:
            self._root = self
        else:
            self._root = root
    
    def page_index(self, character):
        """
        You may find this method helpful. It takes a character and returns the index of the relevant page.
        Time complexity of this method is O(1), because it always only checks 36 characters.
        """
        return ProcessingBook.LEGAL_CHARACTERS.index(character)
    
    def get_error_count(self):
        """
        Returns the number of errors encountered while storing transactions.
        """
        return self._root.error_count
    
    # Task 2.1 Methods.
    def __setitem__(self, transactions: Transaction, amount: int) -> None:
        mySw_sig = transactions.signature
        self._insert(mySw_sig, transactions, amount, self.level)

    def _insert(self, mySw_sig, transactions: Transaction, amount: int, i: int) -> None:
        mySw_indexs_check = self.page_index(mySw_sig[i])
        mySw_acc_slot = self.pages[mySw_indexs_check]
        
        if isinstance(mySw_acc_slot, tuple) and mySw_acc_slot[0] == "L":
            _, old_tx, old_amt, old_sig = mySw_acc_slot
            if old_sig == mySw_sig:
                # print("Debug 1")
                if old_amt == amount:
                    # print("Debug 2")
                    return
                self._root.error_count += 1
                raise ValueError("Updating existing transaction amount is forbidden")
            # Recursion case
            twist = ProcessingBook(level=i + 1, root=self._root)
            self.pages[mySw_indexs_check] = twist
            twist._insert(old_sig, old_tx, old_amt, i + 1)
            twist._insert(mySw_sig, transactions, amount, i + 1)
            return
        
        if mySw_acc_slot is None:
            self.pages[mySw_indexs_check] = ("L", transactions, amount, mySw_sig)
            self._size += 1
            return
        
        gmae = mySw_acc_slot
        gmae._insert(mySw_sig, transactions, amount, i + 1)
        self._size += 1

    def __getitem__(self, transactions: Transaction) -> int:
        mySw_sign = transactions.signature
        return self._find(mySw_sign, self.level)

    def _find(self, mySw_sig, i: int) -> int:
        mySw_indexs_check = self.page_index(mySw_sig[i])
        mySw_acc_slot = self.pages[mySw_indexs_check]

        if mySw_acc_slot is None:
            raise KeyError("Transaction not found")
        
        # print("Check 1")
        if isinstance(mySw_acc_slot, tuple) and mySw_acc_slot[0] == "L":
            # print("Check 2")
            if mySw_acc_slot[3] == mySw_sig:
                # print("Check 3")
                return mySw_acc_slot[2] 
            raise KeyError("Transaction not found")

        return mySw_acc_slot._find(mySw_sig, i + 1)
    
    def __len__(self):
        return self._size
    
    def sample(self, required_size):
        """
        1054 Only - 1008/2085 welcome to attempt if you're up for a challenge, but no marks are allocated.
        Analyse your time complexity of this method.
        """
        pass


if __name__ == "__main__":
    # Write tests for your code here...
    # We are not grading your tests, but we will grade your code with our own tests!
    # So writing tests is a good idea to ensure your code works as expected.

    # Let's create a few transactions
    tr1 = Transaction(123, "sender", "receiver")
    tr1.signature = "abc123"

    tr2 = Transaction(124, "sender", "receiver")
    tr2.signature = "0bbzzz"

    tr3 = Transaction(125, "sender", "receiver")
    tr3.signature = "abcxyz"

    # Let's create a new book to store these transactions
    book = ProcessingBook()

    book[tr1] = 10
    print(book[tr1])  # Prints 10

    book[tr2] = 20
    print(book[tr2])  # Prints 20

    book[tr3] = 30    # Ends up creating 3 other nested books
    print(book[tr3])  # Prints 30
    print(book[tr2])  # Prints 20

    book[tr2] = 40
    print(book[tr2])  # Prints 20 (because it shouldn't update the amount)

    del book[tr1]     # Delete the first transaction. This also means the nested books will be collapsed. We'll test that in a bit.
    try:
        print(book[tr1])  # Raises KeyError
    except KeyError as e:
        print("Raised KeyError as expected:", e)

    print(book[tr2])  # Prints 20
    print(book[tr3])  # Prints 30

    # We deleted T1 a few lines above, which collapsed the nested books.
    # Let's make sure that actually happened. We should be able to find tr3 sitting
    # in Page A of the book:
    print(book.pages[book.page_index('a')])  # This should print whatever details we stored of T3 and only T3