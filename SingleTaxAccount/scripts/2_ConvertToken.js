
require('dotenv').config();
const { ethers } = require("hardhat"); 


async function main() {
  
    /*const url = process.env.ALCHEMY_SEPOLIA_URL;//sepolia
    const provider = new ethers.providers.JsonRpcProvider(url);//sepolia
    */
    const provider = new ethers.providers.JsonRpcProvider();  // on localhost
    const wallet = new ethers.Wallet(process.env.LOCAL_PRIVATE_KEY, provider); // on localhost
    /*const wallet = new ethers.Wallet(process.env.TESTNET_PRIVATE_KEY, provider);//sepolia
    const addrToken = "0x19F57852AfAD017CC6D886a3bE6D28B340cCad70"; //sepolia
    */
    // адрес токена
    const addrToken = "0x5FbDB2315678afecb367f032d93F642f64180aa3"; // on localhost
    
    const token = await ethers.getContractAt("StateToken", addrToken, wallet);

    console.log("token addr:", token.address);
    console.log("token signer:", token.signer.address);
    
    console.log("===========================");
    //console.log("wallet decimals:", token.provider);
    console.log(`balance Exchanger: ${ethers.utils.formatUnits(await token.balanceOf(token.signer.address))} ${await token.symbol()}` );

    const addrBusinessman = "0xf4eAA36948F5177D5b548Fbb20f672D3478CD8E0"; // счет бизнесмена
    const singleTaxPayment = "1.3"; // величина налога
    await wallet.sendTransaction({ // скинем бизнесмену немного ETH на комиссии
      to: addrBusinessman,
      value: ethers.utils.parseEther("1.0") });

    console.log(`balance STT of Businessman: ${ethers.utils.formatUnits(await token.balanceOf(addrBusinessman))} ${await token.symbol()}`);    
    
    console.log("======= convert ==========");

    tx = await token.transfer(addrBusinessman, ethers.utils.parseUnits(singleTaxPayment));
    await tx.wait();   

    console.log(`balance Exchanger: ${ethers.utils.formatUnits(await token.balanceOf(token.signer.address))} ${await token.symbol()}` );
    console.log(`balance STT of Businessman:", ${ethers.utils.formatUnits(await token.balanceOf(addrBusinessman))} ${await token.symbol()}`);    
     

    console.log("=========== разрешаем контракту тратить токены ") 
    const addrSingleTaxContract = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"; // счет контракта ЕНС
    
    const walletBusinessman = new ethers.Wallet(process.env.BISNESMAN_LOCAL_PRIVATE_KEY, provider); // кошелек бизнесмена on localhost
    const tokenBusinessman = await hre.ethers.getContractAt("StateToken", addrToken, walletBusinessman);
    console.log("tokenBusinessman addr:", tokenBusinessman.address);
    console.log("tokenBusinessman signer:", tokenBusinessman.signer.address);
    console.log(`balance of Businessman: ${ethers.utils.formatUnits(await tokenBusinessman.balanceOf(tokenBusinessman.signer.address))} ${await tokenBusinessman.symbol()}` );

    const success = await tokenBusinessman.approve(addrSingleTaxContract, ethers.utils.parseUnits(singleTaxPayment)) ;
    //console.log("success approve: ", success);    
    const amount = await tokenBusinessman.allowance(addrBusinessman, addrSingleTaxContract) ;
    console.log("amount allowance: ", ethers.utils.formatUnits(amount)); // вот столько разрешили тратить нашему контракту ЕНС




}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
