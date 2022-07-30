import json
import os
from solcx import compile_standard
from web3 import Web3
from dotenv import load_dotenv

# solcx.install_solc("0.6.0")
load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


# Compile on Solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Need bytecode and ABI to deploy to blockchain

# Get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get ABI
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# First deploying to something similar to the Javascript VM on Remix: will use Ganache which lets us spin up our own blockchain

# Get http port, network ID, address and private key from Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# Should never hard code your private key (use environment variables)
# Can use export VARIABLE=VALUE (but this only be available for the time the shell is live)
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Build transaction to deploy to blockchain

# Get latest transaction to grab nonce
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,  # https://stackoverflow.com/questions/70051896/python-web3-and-ganache-error-method-eth-maxpriorityfeepergas-not-supported
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)  # Every contract has an implied constructor (not defined explicitly)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("Deploying contract...")

# Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# This will have our code stop and wait until this transaction goes through before executing rest of the code
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Deployed!")

# Working with a contract: need contract address and ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Can either Call or Interact with contract functions
# Call: simply simulate making a call and getting a return value (mainly used for only 'view' functions)
# Transact: Actually make a state change (need to build and send the transaction)

# Initial value of favoriteNumber
print(simple_storage.functions.retrieve().call())

# Will get empty return value as store function has no returns argument (but this function call did update the favoriteNumber for this run only i.e. simulation)
# print(simple_storage.functions.store(15).call())

print("Updating contract...")

# Build, sign and send transaction to actually store a value
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,  # Already used nonce earlier so now need to add 1
    }
)

store_signed_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
store_tx_hash = w3.eth.send_raw_transaction(store_signed_txn.rawTransaction)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)

print("Updated!")

# Retrieve updated value
print(simple_storage.functions.retrieve().call())
