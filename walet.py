from eth_account import Account

# Generate a new account
new_account = Account.create()

# Get the address and private key
print(f"Address: {new_account.address}")
print(f"Private Key: {new_account.key.hex()}")
# Example: Loading ABI from a JSON file (assuming ABI is stored in 'contract_abi.json')


