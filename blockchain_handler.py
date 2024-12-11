from web3 import Web3
from web3.middleware import geth_poa_middleware  # This may be necessary for some networks
from eth_account import Account
from config import INFURA_URL, CONTRACT_ADDRESS, ABI
from web3.exceptions import TransactionNotFound

# Initialize Web3 connection
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Add PoA middleware if connecting to a network with Proof-of-Authority
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Check if the connection is successful
if not w3.isConnected():
    raise Exception("Web3 connection failed")

# Contract initialization
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# Hardcoded private key (DO NOT use this in production!)
PRIVATE_KEY = "0x919ee15b85947bb5a9976fb70999af0a97de69c357577fbdb2ad873d288a7071"  # Replace with your actual private key
account = Account.from_key(PRIVATE_KEY)

# Fetch dynamic gas price
def get_gas_price():
    try:
        gas_price = w3.eth.gas_price  # Fetch current gas price
        return gas_price
    except Exception as e:
        print(f"Error fetching gas price: {e}")
        return w3.toWei('20', 'gwei')  # Default gas price

# Check account balance
balance = w3.eth.get_balance(account.address)
print(f"Account balance: {w3.fromWei(balance, 'ether')} ETH")

# Check the gas price
gas_price = get_gas_price()
print(f"Current gas price: {w3.fromWei(gas_price, 'gwei')} Gwei")

# Function to wait for transaction receipt
def wait_for_transaction(tx_hash, timeout=120):
    try:
        print(f"Waiting for transaction {tx_hash} to be mined...")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
        if receipt.status == 1:
            print(f"Transaction {tx_hash} mined successfully.")
            return receipt
        else:
            print(f"Transaction {tx_hash} failed.")
            return None
    except TransactionNotFound:
        print(f"Transaction {tx_hash} not found!")
        return None

# Function to deposit funds
def deposit_funds(amount_in_ether):
    try:
        # Convert Ether to Wei (1 Ether = 10^18 Wei)
        amount_in_wei = Web3.toWei(amount_in_ether, 'ether')

        # Build transaction
        tx = contract.functions.deposit(amount_in_wei).buildTransaction({
            'chainId': 1,  # Mainnet
            'gas': 2000000,
            'gasPrice': get_gas_price(),
            'nonce': w3.eth.getTransactionCount(account.address),
            'value': amount_in_wei  # Sending Ether
        })

        # Sign the transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)

        # Send the transaction
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Wait for transaction to be mined
        receipt = wait_for_transaction(tx_hash)

        if receipt:
            return {"txHash": tx_hash.hex(), "status": "Success"}
        else:
            return {"error": "Transaction failed"}
    except Exception as e:
        print(f"Error in deposit: {e}")
        return {"error": str(e)}

# Function to release payment
def release_payment():
    try:
        # Build transaction for releasing payment
        tx = contract.functions.releasePayment().buildTransaction({
            'chainId': 1,  # Mainnet
            'gas': 2000000,
            'gasPrice': get_gas_price(),
            'nonce': w3.eth.getTransactionCount(account.address)
        })

        # Sign the transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)

        # Send the transaction
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Wait for transaction to be mined
        receipt = wait_for_transaction(tx_hash)

        if receipt:
            return {"txHash": tx_hash.hex(), "status": "Success"}
        else:
            return {"error": "Transaction failed"}
    except Exception as e:
        print(f"Error in release payment: {e}")
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    deposit_response = deposit_funds(0.1)  # Deposit 0.1 Ether
    print(deposit_response)

    # Example: Release Payment after deposit
    release_response = release_payment()
    print(release_response)
