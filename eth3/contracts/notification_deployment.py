from web3.contract import Contract

from eth3.models import ContractLog
from eth3.web3_client import Web3Client


class NotificationContract:
    CONTRACT_ADDRESS = None

    def __init__(self, client: Web3Client):
        self.client = client
        contract_info: ContractLog = None
        try:
            contract_info = ContractLog.objects.get(contract_name='notification')
        except ContractLog.DoesNotExist:
            pass
        self.instance: Contract = client.web3.eth.contract(address=contract_info.address, abi=contract_info.abi)

    def get_device_token(self, email: str):
        data = self.instance.functions.getToken(email).call()
        return data
