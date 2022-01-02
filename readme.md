# isdi_proxy 
(new project name: VaultPoint Proxy)

---

## What proxy do?

VaultPoint proxy is a centralized system that mediate client's authentication/authorization request to right holders by firing remote push notification.  
To send a notification, proxy requires FCM secret key which is issued by FCM(what we call it `SERVER_KEY`).
All data except client's request are encrypted by client's public-key and these keys are stored in Ethereum blockchain.  


## How to run

### 1. Clone this project
```
git clone https://github.com/elHongsh/vaultpoint_proxy.git
```
VaultPoint-Proxy requires Python3 (≥ 3.7) and Microsoft Visual C++ Build Tools.  

### 2. Deploy the proxy

We tested this application on Windows 10.  
If you are trying to deploy it on Ubuntu or different version of Windows, unexpected issues can be occurred.
```
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver 0.0.0.0:8000
```

### 3. set up the Django database
Deploy client_management and notification contract.    
copy the deployed contract data and paste them into database.  
(you can easily insert them from django-admin page)


## Dependencies

* [django 3.0](https://pypi.org/project/Django/) - One of most well known web framework in python.
* [web3 4.9](https://pypi.org/project/web3/) - Web3 library for python environment.
* [requests 2.22](https://pypi.org/project/requests/) - Synchronous HTTP client library.
