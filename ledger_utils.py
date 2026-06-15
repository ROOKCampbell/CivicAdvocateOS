import hashlib

class HashUtility:
    @staticmethod
    def calculate_hash(block_data):
        return hashlib.sha512(block_data.encode()).hexdigest()

def validate_single_block(block, prev_hash):
    # Verification combines prev_hash + current data
    combined = prev_hash + block['data']
    actual = HashUtility.calculate_hash(combined)
    return actual == block['expected_hash'], block['id']
