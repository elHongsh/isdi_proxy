class ClientRegistration {
    constructor(web3) {
        this.web3 = web3;
        this.abi = [
            {
                "constant": true,
                "inputs": [
                    {
                        "name": "",
                        "type": "bytes32"
                    }
                ],
                "name": "clientAddresses",
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
                "constant": true,
                "inputs": [
                    {
                        "name": "",
                        "type": "bytes32"
                    }
                ],
                "name": "clients",
                "outputs": [
                    {
                        "name": "name",
                        "type": "string"
                    },
                    {
                        "name": "clientId",
                        "type": "string"
                    },
                    {
                        "name": "pubKey",
                        "type": "string"
                    },
                    {
                        "name": "clientAddress",
                        "type": "address"
                    }
                ],
                "payable": false,
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "payable": false,
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "constant": false,
                "inputs": [
                    {
                        "name": "_clientName",
                        "type": "string"
                    },
                    {
                        "name": "_clientId",
                        "type": "string"
                    },
                    {
                        "name": "_pubKey",
                        "type": "string"
                    }
                ],
                "name": "registerClient",
                "outputs": [
                    {
                        "name": "",
                        "type": "bytes32"
                    }
                ],
                "payable": true,
                "stateMutability": "payable",
                "type": "function"
            },
            {
                "constant": false,
                "inputs": [
                    {
                        "name": "_clientId",
                        "type": "string"
                    }
                ],
                "name": "unregisterClient",
                "outputs": [
                    {
                        "name": "",
                        "type": "bool"
                    }
                ],
                "payable": true,
                "stateMutability": "payable",
                "type": "function"
            },
            {
                "constant": false,
                "inputs": [
                    {
                        "name": "_newPubKey",
                        "type": "string"
                    }
                ],
                "name": "changePubKey",
                "outputs": [
                    {
                        "name": "",
                        "type": "bool"
                    }
                ],
                "payable": true,
                "stateMutability": "payable",
                "type": "function"
            },
            {
                "constant": true,
                "inputs": [
                    {
                        "name": "clientId",
                        "type": "string"
                    }
                ],
                "name": "getClientSummary",
                "outputs": [
                    {
                        "name": "",
                        "type": "string"
                    },
                    {
                        "name": "",
                        "type": "string"
                    },
                    {
                        "name": "",
                        "type": "string"
                    },
                    {
                        "name": "",
                        "type": "address"
                    }
                ],
                "payable": false,
                "stateMutability": "view",
                "type": "function"
            }
        ];
        this.contractAddress = "0x43a933bc4686d0a671e5528f35227a6ff337fdf2";
    }

    register(payerAddress, clientName, clientId, clientPubKey) {
        let contract = this.web3.eth.Contract(this.abi, this.contractAddress);
        contract.methods.registerClient(clientName, clientId, clientPubKey).send({'from': payerAddress, 'gas': 1_500_000}, (error, txHash) =>{
            if (error) { return "0x0000000000000000000000000000000000000000000000000000000000000000"; }
            return txHash;
        });
    }
}

function web3Provider() {
    let w3 = new Web3();
    w3.setProvider(new Web3.providers.HttpProvider("http://localhost:7545"));
    alert('work!');
    return w3;
}

function clientRegistrationContract() {
    let web3 = web3Provider();
    new ClientRegistration(web3).register("0xE69e769b524B7cE3a85E4c363e41112EA2bd5633", "Yahoo", "yahoo-id", "yahoo-pubkey");
}