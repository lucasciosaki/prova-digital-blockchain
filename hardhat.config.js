require("@nomicfoundation/hardhat-toolbox");

const BESU_PRIVATE_KEY = "0x64eb53b02197e0ced9b91d3e2f8550893481891234ba459f7fd973c296bd003d"

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.10",
  networks: {
    besu: {
      url: "http://127.0.0.1:8545",

      chainID: 1337,

      accounts: [BESU_PRIVATE_KEY],

      gasPrice: 0
    }
  }
};
