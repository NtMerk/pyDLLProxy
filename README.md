# pyDllProxy
<img width="360" alt="2024-03-13 13_36_30-ChatGPT y 4 páginas más - Trabajo_ Microsoft​ Edge" src="https://github.com/NtMerk/pyDLLProxy/assets/19492870/5ca7fa09-d82c-4d40-a9e0-2ee542cb4488">

pyDLLProxy is a Python tool that intends to aid the development of DLL Proxying attacks. It creates the C/C++ directives necessary for a DLL to proxy the exports to the original DLL. This way, an attacker can craft a malicious DLL that proxies function calls to the original, while executing any desired malicious code.

## Installation
Clone repository
```sh
git clone https://github.com/ntmerk/pyDLLProxy.git
```
Go to pyDLLProxy folder
```sh
cd pyDLLProxy
```
Install requirements
```sh
python3 -m pip install -r requirements.txt
```

## Usage
```sh
⮞  python3 .\pyDLLProxy.py -h
usage: pyDLLProxy.py [-h] [-O OUTPUT] [-T {c,cpp}] dll_path dll_new_name

pyDLLProxy will generate the necessary C/C++ directives in order to aid in the development of DLL Proxying techniques.

positional arguments:
  dll_path              Full path to the DLL to Proxy.
  dll_new_name          New name for the DLL to proxy to.

options:
  -h, --help            show this help message and exit
  -O OUTPUT, --output OUTPUT
                        Output file for the exports.
  -T {c,cpp}, --template {c,cpp}
                        Generate a DLL template with the exports.
```
