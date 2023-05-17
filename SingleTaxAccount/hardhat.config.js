require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.18",
    settings: {
      optimizer: {
        enabled: true,
        runs: 1000,
      },
    },
  },
  paths: {
    artifacts: "./app/src/artifacts",
  },
  allowUnlimitedContractSize: true,
  defaultNetwork: 'localhost',
  networks: {    
    sepolia: {
      url: process.env.ALCHEMY_SEPOLIA_URL,
      accounts: [process.env.TESTNET_PRIVATE_KEY]
    }
  }

};
