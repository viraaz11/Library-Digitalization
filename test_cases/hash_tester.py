from hash_table import *

# Test parameters for each collision method
params_chain = (33, 5)          # (z, table_size) for chaining
params_linear = (33, 5)         # (z, table_size) for linear probing
params_double = (33, 29, 5, 5)  # (z1, z2, c2, table_size) for double hashing

# Function to perform tests on a HashSet or HashMap
def test_hash_structure(hash_structure, name):
    print(f"\nTesting {name}")
    
    # Insert elements
    hash_structure.insert("Stack" if name.endswith("HashSet") else ("Stack", 1))
    hash_structure.insert("AVL" if name.endswith("HashSet") else ("AVL", 2))
    hash_structure.insert("Heap" if name.endswith("HashSet") else ("Heap", 3))
    hash_structure.insert("Hash" if name.endswith("HashSet") else ("Hash", 4))
    
    # Display table
    print("\nAfter insertions:")
    print(hash_structure)

    # Find elements
    print("\nFinding 'AVL':", hash_structure.find("AVL"))
    print("Finding 'Binary' (should be None):", hash_structure.find("Binary"))

    # # Delete element
    # hash_structure.delete("AVL")
    # print("\nAfter deleting 'AVL':")
    # print(hash_structure)

    # Get slot of an element
    print("\nSlot of 'Heap':", hash_structure.get_slot("Heap"))

    # Get load factor
    print("\nLoad factor:", hash_structure.get_load())


# Chaining HashSet and HashMap
chain_hash_set = HashSet("Chain", params_chain)
chain_hash_map = HashMap("Chain", params_chain)
test_hash_structure(chain_hash_set, "Chaining HashSet")
test_hash_structure(chain_hash_map, "Chaining HashMap")


# Linear Probing HashSet and HashMap
linear_hash_set = HashSet("Linear", params_linear)
linear_hash_map = HashMap("Linear", params_linear)
test_hash_structure(linear_hash_set, "Linear Probing HashSet")
test_hash_structure(linear_hash_map, "Linear Probing HashMap")


# Double Hashing HashSet and HashMap
double_hash_set = HashSet("Double", params_double)
double_hash_map = HashMap("Double", params_double)
test_hash_structure(double_hash_set, "Double Hashing HashSet")
test_hash_structure(double_hash_map, "Double Hashing HashMap")