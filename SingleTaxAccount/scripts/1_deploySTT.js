

const { ethers } = require("hardhat"); 
require('dotenv').config();


async function main() {
  
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contract StateToken with the account:", deployer.address);
  
  const weiAmount = (await deployer.getBalance()).toString();
  console.log("Account balance:", (await ethers.utils.formatEther(weiAmount))); 
  const Token = await ethers.getContractFactory("StateToken");
  const token = await Token.deploy();

  await token.deployed();

  //console.log("===========================================");
 
  console.log(
    `token address to ${token.address}`
  );
  console.log(
    `balance token of State: ${ethers.utils.formatUnits(await token.balanceOf(deployer.address),18)}`
  );

  
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});


