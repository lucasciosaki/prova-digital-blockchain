// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;


contract Prova_Digital{

    // Define a estrutura da prova digital
    struct Prova {
        string nome_arquivo; //Nome original do Arquivo
        string hash_metadados; // Hash do JSON de metadados
        address registrar;        // Quem registrou
        uint256 timestamp;        // Quando foi registrado
    }

    // Mapeia o hash do arquivo para a prova
    mapping(bytes32 => Prova) public registros;

    // Evento para notificar o front-end
    event ArquivoRegistrado( 
        bytes32 indexed hash_arquivo,
        string nome_arquivo,
        string hash_metadados,
        address indexed registrar
    );

    //Modifier para requerir que o registro não exista na BC
    modifier registroNaoExiste(bytes32 _hash_arquivo) {
        require(registros[_hash_arquivo].timestamp == 0, "Este arquivo ja foi registrado.");
        _;
    }

    //Modifier para requerir que o registro exista na BC
    modifier registroExiste(bytes32 _hash_arquivo) {
        require(registros[_hash_arquivo].timestamp != 0, "Este arquivo nao foi registrado.");
        _;
    }

    // Função para registrar um arquivo
    function registrarArquivo(bytes32 _hash_arquivo, string memory _nome_arquivo, string memory _hash_metadados) public registroNaoExiste(_hash_arquivo){

        // Cria a prova
        registros[_hash_arquivo] = Prova({
            nome_arquivo: _nome_arquivo, 
            hash_metadados: _hash_metadados,
            registrar: msg.sender,
            timestamp: block.timestamp
        });

        // Emite o evento
        emit ArquivoRegistrado(_hash_arquivo, _nome_arquivo, _hash_metadados, msg.sender);
    }

    function checarRegistro(bytes32 _hash_arquivo) public view registroExiste(_hash_arquivo)
    returns(string memory _nome_arquivo, string memory _hash_metadados, address dono, uint256 _timestamp){
        Prova memory p = registros[_hash_arquivo];
        return(p.nome_arquivo, p.hash_metadados, p.registrar, p.timestamp);
    }
}