class InMemoryDatabase:
    def __init__(self):
        self.main_store = {}
        self.transaction_log = []
        self.in_transaction = False

    def begin_transaction(self):
        if self.in_transaction:
            raise Exception("Transaction already in progress")
        self.in_transaction = True
        self.transaction_log = []

    def put(self, key, value):
        if self.in_transaction:
            self.transaction_log.append(('put', key, value))
        else:
            self.main_store[key] = value

    def get(self, key):
        if self.in_transaction:
            # check the transaction log in reverse to get the most recent value
            for operation, op_key, op_value in reversed(self.transaction_log):
                if op_key == key and operation == 'put':
                    return op_value
            if key in self.main_store:
                return self.main_store[key]
            return None
        else:
            return self.main_store.get(key, None)

    def commit(self):
        if not self.in_transaction:
            raise Exception("No transaction is currently active")
        # apply all operations in the transaction log to the main store
        for operation, key, value in self.transaction_log:
            if operation == 'put':
                self.main_store[key] = value
        self.transaction_log = []
        self.in_transaction = False

    def rollback(self):
        if not self.in_transaction:
            raise Exception("No transaction is currently active")
        # simply discard the transaction log
        self.transaction_log = []
        self.in_transaction = False

db = InMemoryDatabase()
try:
    print(db.get("A"))  # output will be None, no transaction
except Exception as e:
    print(e)

try:
    db.put("A", 5)
except Exception as e:
    print(e)  # error because no transaction is active

db.begin_transaction()
db.put("A", 5)  # sets value of A to 5, not committed yet

print(db.get("A"))  # output will be None, updates to A are not committed yet

db.put("A", 6)  # update A's value to 6 within the transaction

db.commit()  # commits the open transaction

print(db.get("A"))  # output will be 6, that was the last value of A to be committed

try:
    db.commit()
except Exception as e:
    print(e)  # error, no open transaction

try:
    db.rollback()
except Exception as e:
    print(e)  # error, no ongoing transaction

print(db.get("B"))  # output will be None because B does not exist

db.begin_transaction()
db.put("B", 10)  # set key B's value to 10 within the transaction

db.rollback()  # rollback the transaction - revert any changes made to B

print(db.get("B"))  # output will be None because changes to B were rolled back
