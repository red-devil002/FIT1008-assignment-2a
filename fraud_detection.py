from processing_line import Transaction
from data_structures import ArrayR
from data_structures import  HashTableSeparateChaining

class FraudDetection:
    def __init__(self, transactions):
        self.transactions = transactions  # ArrayR or Python list is fine

    # helper fun for converting str to int.
    def converter(self, s: str) -> int:
        val = 0
        for ch in s:
            if '0' <= ch <= '9':
                d = ord(ch) - ord('0')
            else:
                d = ord(ch) - ord('a') + 10
            val = val * 36 + d
        return val

    def detect_by_blocks(self):
        """
        mySw_mix = signature length
        N = number of transactions
        Time Complexity:
            Best: O(N * mySw_mix)
            Worst: O(N * mySw_mix^2)

        Reason:
            This is the best case because it assumes the hash table performs well.
            This is the worst case because it assumes the hash table performs poorly.
        """
        if len(self.transactions) == 0:
            return (1, 0)

        mySw_mix = len(self.transactions[0].signature)
        best_S = 1
        best_score = 0

        # Hashing help humbers
        P1 = 1_000_000_037 
        P2 = 1_000_000_123 
        P3 = 1_000_000_319 
        mySw_key = 987_654_361

        sum1 = 0
        sum2 = 0
        prod = 1
        cnt  = 0

        for val in range(1, mySw_mix + 1):
            mySw_patches = HashTableSeparateChaining()

            for trx in self.transactions:
                sig = trx.signature

                mySw_rowL = mySw_mix % val
                if mySw_rowL == 0:
                    rem = "" 
                else: 
                    sig[mySw_mix - mySw_rowL : mySw_mix]

                i = 0
                while i + val <= mySw_mix:
                    block = sig[i : i + val]
                    Q1 = self.converter(block)
                    sum1 = (sum1 + Q1) % P1
                    sum2 = (sum2 + Q1 * Q1) % P2
                    prod = (prod * (Q1 + mySw_key)) % P3
                    cnt += 1
                    i += val

                # Code of hashing tables
                key_str = f"{len(rem)}:{rem}|{sum1}|{sum2}|{prod}|{cnt}"
                try:
                    mySw_patches[key_str] = mySw_patches[key_str] + 1
                except KeyError:
                    mySw_patches[key_str] = 1

            # Searching into hashing tables for fraud
            mySw_result = 1
            for i in range(len(mySw_patches.items())):
                mySw_result *= mySw_patches.items()[i][1]

            # Final Answer
            if mySw_result > best_score:
                best_S = val
                best_score = mySw_result

        return best_S, best_score

    def rectify(self, functions: ArrayR):
        if len(functions) == 0:
            return (None, 0)

        mySw_len = len(self.transactions)
        mySw_func = functions[0]
        mySw_map = 10**18

        for _ in range(len(functions)):
            mySw_inFu = functions[_]

            mySw_maxxx = -1

            for ti in range(mySw_len):
                v1 = mySw_inFu(self.transactions[ti])
                if v1 > mySw_maxxx:
                    mySw_maxxx = v1

            # check
            if mySw_maxxx >= 0:
                mySw_Tranz = mySw_maxxx + 1 
            else: 
                mySw_Tranz = 0

            #implement
            if mySw_Tranz == 0:
                mySw_rec = 0
            else:
                counts = ArrayR(mySw_Tranz)
                for i in range(mySw_Tranz):
                    counts[i] = 0
                for ti in range(mySw_len):
                    v2 = mySw_inFu(self.transactions[ti])
                    counts[v2] = counts[v2] + 1

                mySw_rec = 0
                for i in range(mySw_Tranz):
                    c = counts[i]
                    if c > 0:
                        probe_len = c - 1
                        if probe_len > mySw_rec:
                            mySw_rec = probe_len

            if mySw_rec < mySw_map:
                mySw_map = mySw_rec
                mySw_func = mySw_inFu

        return mySw_func, mySw_map



if __name__ == "__main__":
    # Write tests for your code here...
    # We are not grading your tests, but we will grade your code with our own tests!
    # So writing tests is a good idea to ensure your code works as expected.
    
    def to_array(lst):
        """
        Helper function to create an ArrayR from a list.
        """
        lst = [to_array(item) if isinstance(item, list) else item for item in lst]
        return ArrayR.from_list(lst)

    # Here is something to get you started with testing detect_by_blocks
    print("<------- Testing detect_by_blocks! ------->")
    # Let's create 2 transactions and set their signatures
    tr1 = Transaction(1, "Alice", "Bob")
    tr2 = Transaction(2, "Alice", "Bob")

    # I will intentionally give the signatures that would put them in the same groups
    # if the block size was 1 or 2.
    tr1.signature = "aabbcc"
    tr2.signature = "ccbbaa"

    # Let's create an instance of FraudDetection with these transactions
    fd = FraudDetection([tr1, tr2])

    # Let's test the detect_by_blocks method
    block_size, suspicion_score = fd.detect_by_blocks()

    # We print the result, hopefully we should see either 1 or 2 for block size, and 2 for suspicion score.
    print(f"Block size: {block_size}, Suspicion score: {suspicion_score}")

    # I'm putting this line here so you can find where the testing ends in the terminal, but testing is by no means
    # complete. There are many more scenarios you'll need to test. Follow what we did above.
    print("<--- Testing detect_by_blocks finished! --->\n")

    # ----------------------------------------------------------

    # Here is something to get you started with testing rectify
    print("<------- Testing rectify! ------->")
    # I'm creating 4 simple transactions...
    transactions = [
        Transaction(1, "Alice", "Bob"),
        Transaction(2, "Alice", "Bob"),
        Transaction(3, "Alice", "Bob"),
        Transaction(4, "Alice", "Bob"),
    ]

    # Then I create two functions and to make testing easier, I use the timestamps I
    # gave to transactions to return the value I want for each transaction.
    def function1(transaction):
        return [2, 1, 1, 50][transaction.timestamp - 1]

    def function2(transaction):
        return [1, 2, 3, 4][transaction.timestamp - 1]

    # Now I create an instance of FraudDetection with these transactions
    fd = FraudDetection(to_array(transactions))

    # And I call rectify with the two functions
    result = fd.rectify(to_array([function1, function2]))

    # The expected result is (function2, 0) because function2 will give us a max probe chain of 0.
    # This is the same example given in the specs
    print(result)
    
    # I'll also use an assert statement to make sure the returned function is indeed the correct one.
    # This will be harder to verify by printing, but can be verified easily with an `assert`:
    assert result == (function2, 0), f"Expected (function2, 0), but got {result}"

    print("<--- Testing rectify finished! --->")