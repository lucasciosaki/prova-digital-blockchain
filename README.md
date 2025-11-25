# Sistema de Provas Digitais com Blockchain (Hyperledger Besu)

Este projeto contém um smart contract, que pode ser visitado em "/contracts/Prova_Digital.sol" cuja finalidade é guardar hashes de provas digitais e seus metadados em uma blockchain permissionada, permitindo assim, a imutabilidade e verificação de integridade de quaisquer arquivos em uma base de dados off-chain. 

> **Disclaimer:** Este projeto tem fins puramente acadêmicos, portanto, as chaves privadas são explicitas e não deve ser usado em ambiente real.


## Instalação e Configuração

1. Em seu bash, clone o repositório e entre nele:
    ```
    git clone [https://github.com/lucasciosaki/prova-digital-blockchain.git](https://github.com/lucasciosaki/prova-digital-blockchain.git)
    cd prova-digital-blockchain
    ```
3. Instale o Hyperledger Besu seguindo o tutorial na página oficial: [Tutorial Besu ](https://besu.hyperledger.org/private-networks/get-started/install/binary-distribution)

4. Instalar o Node.js e npm:
   Pode ser instalado seguindo o tutorial em: [Tutorial Node.js](https://nodejs.org/en/download)

5. Certifique-se de ter o Python 3 instalado

4. Instale as dependencias citadas no package.json apenas com o seguinte comando:
   ```
   npm install
   ```
6. Instale as dependências do Python (dependendo do SO, precisa criar um ambiente virtual do Python antes)
   ```
   pip install -r requirements.txt
   ```
   
## Inicialização da rede IBFT 
(**Os comandos besu a seguir não são identicos, as portas são diferentes**)

1. Entre no diretório Node-1 e o inicialize
    ```
   cd ./Node-1
   besu --data-path=data --genesis-file=../genesis.json --rpc-http-enabled --rpc-http-api=ETH,NET,IBFT,WEB3 --host-allowlist="*" --rpc-http-cors-origins="all" --profile=ENTERPRISE
    ```
3. Após iniciar o Node-1, procure no log a linha que contém "enode://....". Copie esse endereço, você precisará dele para os outros nós.

4. Abra outro terminal no diretório Node-2 e o inicialize (No segundo comando, troque \<Node-1 Enode URL\> pelo Enode URL encontrado anteriormente
    ```
   besu --data-path=data --genesis-file=../genesis.json --bootnodes=<Node-1 Enode URL> --p2p-port=30304 --rpc-http-enabled --rpc-http-api=ETH,NET,IBFT,WEB3 --host-allowlist="*" --rpc-http-cors-origins="all" --rpc-http-port=8546 --profile=ENTERPRISE
    ```
5. Abra outro terminal no diretório Node-3 e o inicialize (Troque novamente o \<Node-1 Enode URL\> pelo mesmo Enode URL)
    ```
   besu --data-path=data --genesis-file=../genesis.json --bootnodes=<Node-1 Enode URL> --p2p-port=30305 --rpc-http-enabled --rpc-http-api=ETH,NET,IBFT,WEB3 --host-allowlist="*" --rpc-http-cors-origins="all" --rpc-http-port=8547 --profile=ENTERPRISE
    ```
6. Abra outro terminal no diretório Node-4 e o inicialize (Troque novamente o \<Node-1 Enode URL\> pelo mesmo Enode URL)
    ```
   besu --data-path=data --genesis-file=../genesis.json --bootnodes=<Node-1 Enode URL> --p2p-port=30306 --rpc-http-enabled --rpc-http-api=ETH,NET,IBFT,WEB3 --host-allowlist="*" --rpc-http-cors-origins="all" --rpc-http-port=8548 --profile=ENTERPRISE
    ```
## Compilação e configuração do Smart Contract (Prova_Digital.sol)

1. Em um novo terminal, entre no diretório base do repositório (prova-digital-blockchain/)

2. Compile o contrato e faça o deploy:
    ```
   npx hardhat compile
   npx hardhat run scripts/deploy.js --network besu
    ```
4. Copie o endereço do contrato mostrando no terminal (Ex: 0x123...)
5. Entre no arquivo "interface.py" e troque a variável CONTRACT_ADDRESS pelo novo endereço
6. Entre no arquivo "Prova_Digital.json" dentro de "artifacts/contracts/Prova_Digital.sol/", copie tudo dentro de abi.
7. Cole todo o abi gerado no lugar da variável CONTRACT_ABI em "interface.py"
8. Salve o arquivo .py

## Finalmente, vamos rodar a interface com o Smart Contract 
**(Deixei disponível um pdf e um json na pasta "/documents" para teste, com nome "exemplo1.pdf" e "exemplo1.json")**

1. Rode a interface
   ```
   python3 interface.py
   ```
3. Escolha a função 1 (Inserir Arquivo)
    ```
    1
   ./documents/exemplo1.pdf
    ```
5. Selecione (Y) temos um json de metadados de exemplo
    ```
   Y
   ./documents/exemplo1.json
    ```

7. Agora vamos testar buscar esse registro na blockchain
    ```
   python3 interface.py
    ```
8. Escolha a funçào 2 (Checar Registro)
    ```
   2
   ./documents/exemplo1.pdf
    ```
10. As informações guardadas na blockchain devem ser retornadas.
