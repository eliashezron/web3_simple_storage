from solcx import compile_standard, install_solc
import json
from web3 import Web3

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

print("Installing...")
install_solc("0.6.0")
# compile our solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

# print(compiled_sol)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode and abi
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to local testrpc
# w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/379d2d85420a445cb0f197f6c7b01977"))
# chain_id = 1337
chain_id = 4
# my_address = "0x280De3f967A3c010AEf7ff0D2036D5199AD2B279"
my_address = "0xdB01d94217308046a792D864b16A35837aa52B86"
# private_key = 
private_key = "{privatekey}"

# deploying python contart
simpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(simpleStorage)
# get lastest transaction
nounce = w3.eth.getTransactionCount(my_address)
# submit the transaction that deploys the contract
transanction = simpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "gas": 1000000,
        "gasPrice": w3.toWei(10, "gwei"),
        "nonce": nounce,
    }
)
# sign the transaction
signed_transaction = w3.eth.account.signTransaction(transanction, private_key)
# send the transaction
tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

# to interact with transaction
simple_Storage_Transaction = w3.eth.contract(
    address=tx_receipt.contractAddress, abi=abi
)
# call means to read
# transact means to write
# print(simple_Storage_Transaction)
print("initial value:", simple_Storage_Transaction.functions.retrieve().call())
simple_Storage_Transaction.functions.store(5).transact({"from": my_address})
print("final value:", simple_Storage_Transaction.functions.retrieve().call())
