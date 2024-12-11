const Web3 = require('web3');
const fs = require('fs');
const path = require('path');

// Step 1: Connect to the Ethereum network
const web3 = new Web3(new Web3.providers.HttpProvider("https://mainnet.infura.io/v3/87c455be5a1b4920be109984d0ae7853"));

// Step 2: Load compiled contract
const contractPath = path.resolve(__dirname, 'build', 'YourContract.json'); // Adjust path if needed
const contractJson = JSON.parse(fs.readFileSync(contractPath, 'utf8'));

// Step 3: Define contract details
const bytecode = contractJson.evm.bytecode.object;
const abi = contractJson.abi;

const deploy = async () => {
    const accounts = await web3.eth.getAccounts(); // Optionally use private key for signing
    console.log("Deploying contract from:", accounts[0]);

    // Create contract instance
    const contract = new web3.eth.Contract(abi);

    // Deploy
    const contractInstance = await contract.deploy({ data: bytecode })
        .send({ from: accounts[0], gas: '5000000' });

    console.log("Contract deployed at:", contractInstance.options.address);
};

deploy().catch(console.error);
