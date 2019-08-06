from web3.contract import Contract

from eth3.models import ContractLog
from eth3.web3_client import Web3Client


class ClientManagementContract:
    CONTRACT_ADDRESS = None

    def __init__(self, client: Web3Client):
        self.client = client
        contract_info: ContractLog = None
        try:
            contract_info = ContractLog.objects.get(contract_name='client_management')
        except ContractLog.DoesNotExist:
            pass
        self.instance: Contract = client.web3.eth.contract(address=contract_info.address, abi=contract_info.abi)

    def get_client_summary(self, client_id: str):
        data = self.instance.functions.getClientSummary(client_id).call(
            {'from': '', 'gas': 900_000})
        return ClientSummary(data)


class ClientSummary:
    def __init__(self, data):
        self.name = data[0]
        self.client_id = data[1]
        self.public_key = data[2]
        self.scopes = data[3]
        self.redirect_url = data[4]
        self.client_address = data[5]
