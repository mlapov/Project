

require('dotenv').config();
const { ethers } = require("hardhat"); 


async function main() {
  
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contract StateToken with the account:", deployer.address);
  
  const weiAmount = (await deployer.getBalance()).toString();
  console.log("Account balance:", (await ethers.utils.formatEther(weiAmount))); 
  const SingleTax = await ethers.getContractFactory("SingleTaxContract");
  const singleTaxContract = await SingleTax.deploy();

  await singleTaxContract.deployed();

  //console.log("===========================================");
 
  console.log(
    `SingleTaxContract address to ${singleTaxContract.address}`
  );
  
  
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

