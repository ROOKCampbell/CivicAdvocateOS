import hashlib

class HashUtility:
    """Handles SHA-512 operations efficiently."""
    @staticmethod
    def calculate_hash(block_data):
        return hashlib.sha512(block_data.encode()).hexdigest()

def validate_single_block(block):
    """Worker function for parallel processing."""
    expected = block.get('expected_hash')
    actual = HashUtility.calculate_hash(block['data'])
    
    if actual != expected:
        print(f"DEBUG: Block {block['id']} Mismatch!")
        print(f"  Data: {repr(block['data'])}")
        print(f"  Expected: {expected}")
        print(f"  Actual:   {actual}")
        
    return actual == expected, block['id']
