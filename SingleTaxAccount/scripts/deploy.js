
const { ethers } = require("hardhat"); 
require('dotenv').config();
const fs = require('fs');

async function main() {

  const [signer] = await ethers.getSigners();
  // скинем немного ETH на комиссии
  /*const addrState = "0x7D63D9Ddf2b9B3B0F1cb95eFb0a7ae1cADF35e12";
  const addrBusinessman1 = "0xf4eAA36948F5177D5b548Fbb20f672D3478CD8E0";
  const addrBusinessman2 = "0xAc9E0Cd1f59cA37D9F6eE016Be1839086F1c4E9D";
  const addrBusinessman3 = "0xa5048352A3D9ad53E87AeF6EbF70c875ca3825eF";
  await signer.sendTransaction({ // скинем бизнесмену немного ETH на комиссии
          to: addrState,
          value: ethers.utils.parseEther("100.0") });
  await signer.sendTransaction({ // скинем бизнесмену немного ETH на комиссии
          to: addrBusinessman1,
          value: ethers.utils.parseEther("41.0") });          
  await signer.sendTransaction({ // скинем бизнесмену немного ETH на комиссии
          to: addrBusinessman2,
          value: ethers.utils.parseEther("23.0") });      
  await signer.sendTransaction({ // скинем бизнесмену немного ETH на комиссии
          to: addrBusinessman3,
          value: ethers.utils.parseEther("10.0") });
  */
  const url = process.env.ALCHEMY_SEPOLIA_URL;
  const provider = new ethers.providers.JsonRpcProvider(url);  
  const deployer = new ethers.Wallet(process.env.STATE_PRIVATE_KEY, provider); // provider.getSigner();
         


  console.log("============ Deploy Token =============");
  //const [deployer] = await ethers.getSigners();
  console.log("Deploying contract StateToken with the account:", deployer.address);
  
  const weiAmount = (await deployer.getBalance()).toString();
  console.log("Account balance:", (await ethers.utils.formatEther(weiAmount))); 
  const Token = await ethers.getContractFactory("StateToken", deployer);
  const token = await Token.deploy();

  await token.deployed();
 
  console.log(
    `token address to ${token.address}`
  );
  console.log(
    `balance token of State: ${ethers.utils.formatUnits(await token.balanceOf(deployer.address),18)}`
  );
  console.log("============ Deploy Tax Contract =============");

  //const [deployer] = await ethers.getSigners();
  console.log("Deploying contract SingleTaxContract with the account:", deployer.address);
    
  const SingleTax = await ethers.getContractFactory("SingleTaxContract", deployer);
  const singleTaxContract = await SingleTax.deploy();

  await singleTaxContract.deployed();
  
  console.log(
    `SingleTaxContract address to ${singleTaxContract.address}`
  );

  console.log("============ Deploy NFT =============");
  console.log("Deploying NFT with the account:", deployer.address);
  const NftContract = await ethers.getContractFactory("NFTContract", deployer);
  const nftContract = await NftContract.deploy();
  await nftContract.deployed();

  console.log(
    `NFT address to ${nftContract.address}`
  );
  console.log("owner NFT:", await nftContract.owner());  
  //await nftContract.changeOwner(singleTaxContract.address);
  console.log("NEW owner NFT:", await nftContract.owner()); 

  const addrContracts = `const addressContracts = { \
    "adressOwner": "${deployer.address}", \
    "addressToken" : "${token.address}", \
    "addressTaxContract" : "${singleTaxContract.address}", \
    "addressNFT" : "${nftContract.address}" \
  }; \
  \nexport default addressContracts;`;

  
  fs.writeFile('./app/src/address-contracts.js', addrContracts, function (error) {
      if (error) throw error; // если возникла ошибка
      console.log(
          '\nАсинхронная запись файла завершена. Содержимое файла:'
      );
      let data = fs.readFileSync('./app/src/address-contracts.js', 'utf8');
      console.log(data); // выводим считанные данные
  });



}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

  