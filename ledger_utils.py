import hashlib, ecdsa

class HashUtility:
    @staticmethod
    def calculate_hash(data):
        return hashlib.sha512(data.encode()).hexdigest()

def validate_single_block(block, prev_hash):
    # 1. Verify Hash Chain
    combined = prev_hash + block['data']
    if HashUtility.calculate_hash(combined) != block['expected_hash']:
        return False, block['id']
    
    # 2. Verify Digital Signature
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(block['pub_key']), curve=ecdsa.SECP256k1)
    try:
        vk.verify(bytes.fromhex(block['signature']), block['expected_hash'].encode())
        return True, block['id']
    except:
        return False, block['id']
