

import { ethers } from 'ethers';
import SingleTaxContract from './artifacts/contracts/SingleTaxContract.sol/SingleTaxContract';
import NFTContract from './artifacts/contracts/NFTContract.sol/NFTContract';
import StateToken from './artifacts/contracts/StateToken.sol/StateToken';

import env from "react-dotenv"; 
 
export default async function init(addresses) {
  // необходимо проинициализировать NFT и ТАХ конракт
  //const provider = new ethers.providers.Web3Provider(window.ethereum);  
  const url = env.ALCHEMY_SEPOLIA_URL;
  console.log("url:", url); 
  const provider = new ethers.providers.JsonRpcProvider(url);  
  console.log("provider:", provider); 
  const signer = new ethers.Wallet(env.STATE_PRIVATE_KEY, provider); // provider.getSigner();
  console.log("signer.address:", await signer.getAddress()); 
  // connect State Contract 
  const instanceSingleTaxContract = new ethers.Contract(addresses.addressTaxContract, 
                      SingleTaxContract.abi,
                      signer );
  
  const singleTaxContract = instanceSingleTaxContract.connect(signer);
  console.log("singleTaxContract.address:", singleTaxContract.address); 
  
  // connect NFT 
  const instanceNFTContract = new ethers.Contract(addresses.addressNFT, 
                        NFTContract.abi, 
                        signer );
    
  const nftContract = instanceNFTContract.connect(signer);
  console.log("nftContract.address:", nftContract.address); 

  // connect Token 
  const instanceStateToken = new ethers.Contract(addresses.addressToken, 
    StateToken.abi, 
    signer );
    
  const stateToken = instanceStateToken.connect(signer);
  console.log("StateToken.address:", stateToken.address); 
  
  // In StateContract write address of NFT   
  console.log("11:", await singleTaxContract.owner());
  console.log("signer:", await singleTaxContract.setAddrNFT(nftContract.address));  
  //console.log("listTax:", await singleTaxContract.readListTax());   
  //console.log("balance signer:", ethers.utils.formatUnits(await stateToken.balanceOf(await signer.getAddress())));
  console.log("22");
  // Change owner of NFT -> newOwner = singleTaxContract
  const nftOwner = await nftContract.owner();
  console.log("owner NFT:", nftOwner);  
  if (nftOwner !== singleTaxContract.address) {
    await nftContract.transferOwnership(singleTaxContract.address);
    console.log("NEW owner NFT:", await nftContract.owner()); 
  }
   
  // Download list tax - addresses of budgets
  const ListTax = {
    
    "0xfE2a6ce64D1dda40Ec05A3b9fbeb61fAe92544f7" : "Income tax",
    "0x0bff5321b3C987754394b325D9e94bB3Fe2219Cb" : "Fire tax",
    "0x495b338b94cb2044f78ea216FD9BfC4bD90407Ed" : "Water tax",
    "0x93DF2DC3B7789A4fB777Ca439B1A4ad011D95041" : "Land tax",
    "0xD03D571A6E627060848498502b9F4A877eCefF73" : "Air tax"  
  }
  
  await singleTaxContract.uploadListTax(Object.keys(ListTax), Object.values(ListTax));
  //console.log("readListTax: ", await singleTaxContract.readListTax());

  // Download tax of businessman    
  const taxBusinessmans = {
    "0xf4eAA36948F5177D5b548Fbb20f672D3478CD8E0" : {
      "0xfE2a6ce64D1dda40Ec05A3b9fbeb61fAe92544f7" : ethers.utils.parseUnits("85.1"),
      "0x0bff5321b3C987754394b325D9e94bB3Fe2219Cb" : ethers.utils.parseUnits("15.3"),
      "0x495b338b94cb2044f78ea216FD9BfC4bD90407Ed" : ethers.utils.parseUnits("12"),
      "0x93DF2DC3B7789A4fB777Ca439B1A4ad011D95041" : ethers.utils.parseUnits("16"),
      "0xD03D571A6E627060848498502b9F4A877eCefF73" : ethers.utils.parseUnits("3.5")
    },
    "0xAc9E0Cd1f59cA37D9F6eE016Be1839086F1c4E9D" : {
      "0xfE2a6ce64D1dda40Ec05A3b9fbeb61fAe92544f7" : ethers.utils.parseUnits("45.1"),
      "0x0bff5321b3C987754394b325D9e94bB3Fe2219Cb" : ethers.utils.parseUnits("5.3"),
      "0x495b338b94cb2044f78ea216FD9BfC4bD90407Ed" : ethers.utils.parseUnits("6"),
      "0xD03D571A6E627060848498502b9F4A877eCefF73" : ethers.utils.parseUnits("0.91")
    },    
    "0xa5048352A3D9ad53E87AeF6EbF70c875ca3825eF" : {
      "0xfE2a6ce64D1dda40Ec05A3b9fbeb61fAe92544f7" : ethers.utils.parseUnits("4"),
      "0x0bff5321b3C987754394b325D9e94bB3Fe2219Cb" : ethers.utils.parseUnits("5"),
      "0x495b338b94cb2044f78ea216FD9BfC4bD90407Ed" : ethers.utils.parseUnits("6")
    }
  }
 
  const bankBusinessmans = {
    "0xf4eaa36948f5177d5b548fbb20f672d3478cd8e0" : 3000,
    "0xac9e0cd1f59ca37d9f6ee016be1839086f1c4e9d" : 2000,
    "0xa5048352a3d9ad53e87aef6ebf70c875ca3825ef" : 1000
  }
  console.log(Object.keys(taxBusinessmans));
  const arrTmp1 = [];
  const arrTmp2 = [];
  for (let i = 0; i < Object.keys(taxBusinessmans).length; i++) {
    arrTmp1.push(Object.keys(Object.values(taxBusinessmans)[i]));
    arrTmp2.push(Object.values(Object.values(taxBusinessmans)[i]));
  }
  //console.log(arrTmp1);
  //console.log(arrTmp2);
  await singleTaxContract.taxDataDownload (Object.keys(taxBusinessmans), arrTmp1, arrTmp2);
  // 
  const arrayTax = await singleTaxContract.readTaxes(
    Object.keys(taxBusinessmans), 
    Object.keys(ListTax));
  let result = [];
  for (let i = 0; i < arrayTax.length; i++){
    result.push(arrayTax[i].map((x) => {
      return (Number(ethers.utils.formatUnits(x)));
    }));
  }     
  console.log(result);
//console.log(arrayTax);
  return { provider, signer , singleTaxContract, stateToken, nftContract, ListTax, bankBusinessmans};
}

