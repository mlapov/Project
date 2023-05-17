//const hre = require("hardhat");
import { ethers } from 'ethers';
import SingleTaxContract from './artifacts/contracts/SingleTaxContract.sol/SingleTaxContract';

//require('dotenv').config();
//const fs = require('fs');
//const env = require('react-dotenv');
import env from "react-dotenv"; 
import addressContracts from './address-contracts.js';
 
export default async function assigntx(event) {
    //alert(numberTax);
    //console.log(event);
    const url = env.ALCHEMY_SEPOLIA_URL;
    const provider = new ethers.providers.JsonRpcProvider(url);  
    const signer = new ethers.Wallet(env.STATE_PRIVATE_KEY, provider); // provider.getSigner();
    console.log("AT: signer.address:", await signer.getAddress()); 
    // connect State Contract 
    const instanceSingleTaxContract = new ethers.Contract(addressContracts.addressTaxContract, 
                        SingleTaxContract.abi,
                        signer );
    
    const singleTaxContract = instanceSingleTaxContract.connect(signer);
    console.log("AT: singleTaxContract.address:", singleTaxContract.address); 

    console.log("AT: button:", event.target.value);
    let variant = event.target.value;
    let taxBusinessmans = {};
    if (variant == 1) {
        taxBusinessmans = {
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
    }
    else if (variant == 2) {
      taxBusinessmans = {
        "0xf4eAA36948F5177D5b548Fbb20f672D3478CD8E0" : {
          "0xfE2a6ce64D1dda40Ec05A3b9fbeb61fAe92544f7" : ethers.utils.parseUnits("0.9"),
          "0x0bff5321b3C987754394b325D9e94bB3Fe2219Cb" : ethers.utils.parseUnits("0.8"),
          "0x495b338b94cb2044f78ea216FD9BfC4bD90407Ed" : ethers.utils.parseUnits("0.7"),
          "0x93DF2DC3B7789A4fB777Ca439B1A4ad011D95041" : ethers.utils.parseUnits("0.62"),
          "0xD03D571A6E627060848498502b9F4A877eCefF73" : ethers.utils.parseUnits("0.51")
        },
        "0xAc9E0Cd1f59cA37D9F6eE016Be1839086F1c4E9D" : {
          "0xfE2a6ce64D1dda40Ec05A3b9fbeb61fAe92544f7" : ethers.utils.parseUnits("0.5"),
          "0x0bff5321b3C987754394b325D9e94bB3Fe2219Cb" : ethers.utils.parseUnits("0.4"),
          "0x495b338b94cb2044f78ea216FD9BfC4bD90407Ed" : ethers.utils.parseUnits("0.3"),
          "0xD03D571A6E627060848498502b9F4A877eCefF73" : ethers.utils.parseUnits("0.25")
        },    
        "0xa5048352A3D9ad53E87AeF6EbF70c875ca3825eF" : {
          "0xfE2a6ce64D1dda40Ec05A3b9fbeb61fAe92544f7" : ethers.utils.parseUnits("0.3"),
          "0x0bff5321b3C987754394b325D9e94bB3Fe2219Cb" : ethers.utils.parseUnits("0.2"),
          "0x495b338b94cb2044f78ea216FD9BfC4bD90407Ed" : ethers.utils.parseUnits("0.19")
        }
      }
    }
    else {
      taxBusinessmans = {
        "0xf4eAA36948F5177D5b548Fbb20f672D3478CD8E0" : {
          "0xfE2a6ce64D1dda40Ec05A3b9fbeb61fAe92544f7" : ethers.utils.parseUnits("31.1"),
          "0x0bff5321b3C987754394b325D9e94bB3Fe2219Cb" : ethers.utils.parseUnits("32.3"),
          "0x495b338b94cb2044f78ea216FD9BfC4bD90407Ed" : ethers.utils.parseUnits("33"),
          "0x93DF2DC3B7789A4fB777Ca439B1A4ad011D95041" : ethers.utils.parseUnits("34"),
          "0xD03D571A6E627060848498502b9F4A877eCefF73" : ethers.utils.parseUnits("35")
        },
        "0xAc9E0Cd1f59cA37D9F6eE016Be1839086F1c4E9D" : {
          "0xfE2a6ce64D1dda40Ec05A3b9fbeb61fAe92544f7" : ethers.utils.parseUnits("35.1"),
          "0x0bff5321b3C987754394b325D9e94bB3Fe2219Cb" : ethers.utils.parseUnits("36.3"),
          "0x495b338b94cb2044f78ea216FD9BfC4bD90407Ed" : ethers.utils.parseUnits("37"),
          "0xD03D571A6E627060848498502b9F4A877eCefF73" : ethers.utils.parseUnits("38.91")
        },    
        "0xa5048352A3D9ad53E87AeF6EbF70c875ca3825eF" : {
          "0xfE2a6ce64D1dda40Ec05A3b9fbeb61fAe92544f7" : ethers.utils.parseUnits("34.46"),
          "0x0bff5321b3C987754394b325D9e94bB3Fe2219Cb" : ethers.utils.parseUnits("35.98"),
          "0x495b338b94cb2044f78ea216FD9BfC4bD90407Ed" : ethers.utils.parseUnits("36.56")
        }
      }
    } 

    const ListTax = {
        /*"Income tax"  : "0xfE2a6ce64D1dda40Ec05A3b9fbeb61fAe92544f7",
        "Fire tax"  : "0x0bff5321b3C987754394b325D9e94bB3Fe2219Cb",
        "Water tax"  : "0x495b338b94cb2044f78ea216FD9BfC4bD90407Ed",
        "Land tax"  : "0x93DF2DC3B7789A4fB777Ca439B1A4ad011D95041",
        "Air tax"  : "0xD03D571A6E627060848498502b9F4A877eCefF73",*/
    
        "0xfE2a6ce64D1dda40Ec05A3b9fbeb61fAe92544f7" : "Income tax",
        "0x0bff5321b3C987754394b325D9e94bB3Fe2219Cb" : "Fire tax",
        "0x495b338b94cb2044f78ea216FD9BfC4bD90407Ed" : "Water tax",
        "0x93DF2DC3B7789A4fB777Ca439B1A4ad011D95041" : "Land tax",
        "0xD03D571A6E627060848498502b9F4A877eCefF73" : "Air tax"  
      }
      
      console.log(Object.keys(taxBusinessmans));
      const arrTmp1 = [];
      const arrTmp2 = [];
      for (let i = 0; i < Object.keys(taxBusinessmans).length; i++) {
        arrTmp1.push(Object.keys(Object.values(taxBusinessmans)[i]));
        arrTmp2.push(Object.values(Object.values(taxBusinessmans)[i]));
      }
      console.log(arrTmp1);
      console.log(arrTmp2);
      const tx = await singleTaxContract.taxDataDownload (Object.keys(taxBusinessmans), arrTmp1, arrTmp2);
      await tx.wait(); 
      const arrayTax = await singleTaxContract.readTaxes(
        Object.keys(taxBusinessmans), 
        Object.keys(ListTax));
      let result = [];
      for (let i = 0; i < arrayTax.length; i++){
        result.push(arrayTax[i].map((x) => {
          return (Number(ethers.utils.formatUnits(x)));
        }));
      }     
      console.log("AT: readTaxes:", result);
}