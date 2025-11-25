import json
import hashlib
from web3 import Web3 # type: ignore
from eth_account import Account #type: ignore
from requests import Session
from datetime import datetime

#1. Configuração

# URL do seu nó Besu
# Quando abrimos o Node-1 no Besu, por padrão vem esse URL
BESU_NODE_URL = "http://127.0.0.1:8545"

# Endereço do contrato implantado (É retornado pelo deploy.js)
CONTRACT_ADDRESS = "0xC1C7F9a529324440833B1408396d0a9ebc89ACdC"

# Essa é a chave privada do Node-1
MY_PRIVATE_KEY = "0x64eb53b02197e0ced9b91d3e2f8550893481891234ba459f7fd973c296bd003d"
MY_ADDRESS = Account.from_key(MY_PRIVATE_KEY).address # Endereço da conta acima

# O ABI do contrato Prova_Digital (copiado do arquivo .../Prova_Digital.json)
CONTRACT_ABI = """
  [
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "bytes32",
          "name": "hash_arquivo",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "internalType": "string",
          "name": "nome_arquivo",
          "type": "string"
        },
        {
          "indexed": false,
          "internalType": "string",
          "name": "hash_metadados",
          "type": "string"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "registrar",
          "type": "address"
        }
      ],
      "name": "ArquivoRegistrado",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_hash_arquivo",
          "type": "bytes32"
        }
      ],
      "name": "checarRegistro",
      "outputs": [
        {
          "internalType": "string",
          "name": "_nome_arquivo",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_hash_metadados",
          "type": "string"
        },
        {
          "internalType": "address",
          "name": "dono",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_timestamp",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_hash_arquivo",
          "type": "bytes32"
        },
        {
          "internalType": "string",
          "name": "_nome_arquivo",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_hash_metadados",
          "type": "string"
        }
      ],
      "name": "registrarArquivo",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "name": "registros",
      "outputs": [
        {
          "internalType": "string",
          "name": "nome_arquivo",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "hash_metadados",
          "type": "string"
        },
        {
          "internalType": "address",
          "name": "registrar",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]
"""

def calcular_hash_arquivo(nome_arquivo):
    #Calcula o hash SHA-256 de um arquivo, lendo em blocos de 4KB

    sha256_hash = hashlib.sha256()
    try:
        with open(nome_arquivo, "rb") as f:
            # Lê o arquivo em blocos de 4KB
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        print(f"Arquivo '{nome_arquivo}' hasheado com sucesso.")
        # Retorna os bytes brutos do hash
        return sha256_hash.digest()
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{nome_arquivo}' não encontrado.")
        return None
    except Exception as e:
        print(f"ERRO ao hashear arquivo: {e}")
        return None


def registrar_arquivo(w3, contract):
  # Dados para registrar
  nome_arquivo = input("Qual arquivo deseja registrar?\n")
  
  # Calcula o hash do arquivo
  hash_arquivo = calcular_hash_arquivo(nome_arquivo)
  if hash_arquivo is None:
      return
    
  tem_metadados = input("Você deseja guardar a hash de um arquivo de metadados? (Y/N)\n")
  match tem_metadados:
      case "Y":
        nome_metadados = input("Qual o arquivo de metadados?\n")
        # Calcula o hash do arquivo e transforma em String         
        hash_metadados = calcular_hash_arquivo(nome_metadados)
        if hash_metadados is None:
            return
        hash_metadados = hash_metadados.hex()
      
      case "N":
        #Se não tem metadados, apenas guarda uma string vazia
        hash_metadados = ""
      
      case _:
          print("Entrada Inválida")
          return
  
  
  print(f"Hash SHA-256 do Arquivo: {hash_arquivo.hex()}")
  print(f"Hash SHA-256 dos Metadados: {hash_metadados}")
  # --- Chamando a Função do Contrato ---
  print("Iniciando transação para 'registrarArquivo'...")
  try:
      # 1. Preparar a transação

      nonce = w3.eth.get_transaction_count(MY_ADDRESS)
      tx_data = {
          'from': MY_ADDRESS,
          'nonce': nonce,
          'gas': 500000,       
          'gasPrice': w3.to_wei(0, 'gwei') 
      }
      # Constrói a transação que chama a função
      transaction = contract.functions.registrarArquivo(
          hash_arquivo,
          nome_arquivo,
          hash_metadados
      ).build_transaction(tx_data)
      # 2. Assinar a transação (necessário em rede permissionada)
      signed_tx = w3.eth.account.sign_transaction(transaction, MY_PRIVATE_KEY)
      # 3. Enviar a transação assinada
      tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
      print(f"Transação enviada! Hash: {tx_hash.hex()}")

      #4. Esperar a reposta de recibo
      try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt.status == 1:
            print(f"Arquivo registrado no bloco {receipt.blockNumber}.")
        else:
            print("A transação falhou e foi revertida pela blockchain.")
            print("Verifique se o arquivo já não estava registrado.")
            
      except Exception as e:
          print(f"Erro esperando recibo: {e}")

  except Exception as e:
      print(f"ERRO durante a transação: {e}")


def checar_registro(contract): 
  #Arquivo a ser checado
  nome_arquivo = input("Qual arquivo deseja checar?\n")
  
  # Calcula o hash do arquivo
  hash_arquivo = calcular_hash_arquivo(nome_arquivo)
  if hash_arquivo is None:
      return
  
  print(f"Hash SHA-256 do Arquivo: {hash_arquivo.hex()}")

  # --- Chamando a Função do Contrato ---
  print("Iniciando chamada para 'checarRegistro'...")
  try:
      resultado = contract.functions.checarRegistro(hash_arquivo).call()
      print("\n" + "-"*20)
      print("Registro Encontrado")
      print(f"Nome Original: {resultado[0]}")
      print(f"Hash Metadados: {resultado[1]}")
      print(f"Registrado por: {resultado[2]}")

      data = datetime.fromtimestamp(resultado[3])
      print(f"Data: {data}")


  except Exception as e:
      print(f"ERRO durante a chamada: {e}")



def main():
    #Conectando ao Besu
    session = Session()
    session.proxies = {"http": None, "https": None}
    provider = Web3.HTTPProvider(BESU_NODE_URL, session=session)
    w3 = Web3(provider)

    try:
        chain_id = w3.eth.chain_id
        print(f"Sucesso! Conectado ao nó Besu (Chain ID: {chain_id})")
    except Exception as e:
        print("FALHA AO CONECTAR AO NÓ BESU.")
        print("Ocorreu um erro ao tentar buscar o chain_id:")
        print(f"Erro: {e}")
        return


    # Carregando o Contrato
    # Transforma o texto do ABI em um objeto Python
    abi_object = json.loads(CONTRACT_ABI) 
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi_object)

    
    while(True):
      print("Escolha a função:")
      print("1 - Registrar Arquivo")
      print("2 - Checar Registro")
      print("3 - Sair")

      comando = int(input(""))

      match comando:
          case 1:
              registrar_arquivo(w3, contract)
          case 2:
              checar_registro(contract)
          case _:
              return
      
      print("-"*20)


if __name__ == "__main__":  
    main()