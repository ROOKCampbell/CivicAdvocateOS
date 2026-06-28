import sys
import ctypes
from tree_sitter import Parser, Language

lib = ctypes.CDLL('/data/data/com.termux/files/home/tree-sitter-grammars/build/my-languages.so')

# Get the function pointer and cast its address to an integer
func_ptr = lib.tree_sitter_solidity
addr = ctypes.cast(func_ptr, ctypes.c_void_p).value

# Pass the integer address
SOL_LANG = Language(addr)
parser = Parser(SOL_LANG)

def perform_audit(file_path):
    with open(file_path, 'rb') as f:
        tree = parser.parse(f.read())
        
        # Diagnostic dump
        print(f"Root Type: {tree.root_node.type}")
        print(f"Child count: {len(tree.root_node.children)}")
        for child in tree.root_node.children:
            print(f"  Node: {child.type}")

if __name__ == "__main__":
    perform_audit(sys.argv[1])
