from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3


class Web3Client:
    provider: str = "http://192.168.0.161:8545"
    private_key: str = "bbd7e23c9e3cb8a2665d71bed580351d74ef92b3adbb37f0add5f6a28779e0fd"

    def __init__(self):
        self.account: LocalAccount = Account.privateKeyToAccount(Web3Client.private_key)
        self.web3 = Web3(Web3.HTTPProvider(Web3Client.provider))
