
from dis import Bytecode
from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

with open("./Si mpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)


# Compile Our Solidity

compiled_sol = compile_standard(
    {
        "language": "solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": { "*" :["abi", "metadata", "evm,bytecode", "evm.sourceMap"]}
            }
        },
    },

    solc_version="0.6.0", 
)

with open("complied_code.json", "w") as files:
    json.dump(compiled_sol,file)

    #get bytecode
    abi = compiled_sol["contracts"]["Simplestorage.sol"]["SimpleStorage"]["evm"]
    ["bytecode"]["object"];

    #get abi
    abi = compiled_sol["contracts"]["Simplestorage.sol"]["Simplestorage"]["abi"]


    #to connect to HTTP/RPC provider / for connecting to ganache
    w3 = Web3(Web3(Web3.HTTPProvider("http://127.0.0.1:7545")))

    #chain ID
    chain_id =  5777
    my_address = "0xDa01e30BF8280a03a1257641257D95575b2984DA"
    private_key = "0xe096b32e4534c7aca84a58186e871d5a83cefdfca01a351223e25a4c95f180e1"
    


    #create the contract in python
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=Bytecode)
``
    #Get the latest transaction
    nonce = w3.eth.getTransactionCount(my_address)
    
    #1. Build a transaction
    #2. Sign a transaction
    #3. Send a transaction

    transaction = SimpleStorage.constructor().buildTransaction(
        {"chainId": chain_id, "from":my_address, "nonce":nonce}
    )

    signed_txn = w3.eth.account.sign_transaction(transaction,private_key=private_key)

    #set environment variables - which are variables set in the command line
    #export PRIVATE_KEY= "0xe096b32e4534c7aca84a58186e871d5a83cefdfca01a351223e25a4c95f180e1"
    #echo $PRIVATE_KEY

    #send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction) 
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


    #working with contract, you need:
    # contract ABI
    # Contract Address

    simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    #Call -> simulate making the call and getting a return value
    #Transact -> Actually make a state change

    #intial value of favorite number
    print(simple_storage.functions.retrieve().call())
    print("Updating contract...")
    #print(simple_storage.functions.store(15).call)
    #print(simple_storage.functions.retrieve(15).call)

    store_transaction = simple_storage.functions.store(15).buildTransaction(
        {
            "chainId": chain_id, "from": my_address,'nonce':nonce + 1,}
    )

    signed_store_txn = w3.eth.account.sign_transaction(
        store_transaction,private_key=private_key
    )

    send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
    print("Updated Contract...")
    print(simple_storage.functions.retrieve().call())