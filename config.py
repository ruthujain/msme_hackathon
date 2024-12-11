INFURA_URL = "https://mainnet.infura.io/v3/87c455be5a1b4920be109984d0ae7853"
CONTRACT_ADDRESS = "0xaF147Fd7455Af5c77a329Cd3F012558f22dd33bb"
ABI =[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "shipmentId",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "product",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "hsnCode",
				"type": "string"
			}
		],
		"name": "createShipment",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "deposit",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "shipmentId",
				"type": "uint256"
			}
		],
		"name": "markDelivered",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "shipmentId",
				"type": "uint256"
			}
		],
		"name": "releasePayment",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "shipmentId",
				"type": "uint256"
			}
		],
		"name": "PaymentReleased",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "shipmentId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "product",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "hsnCode",
				"type": "string"
			}
		],
		"name": "ShipmentCreated",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "shipments",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "product",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "hsnCode",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "delivered",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "paid",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
# Contract ABI (Application Binary Interface)
