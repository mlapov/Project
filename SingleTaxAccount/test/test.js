const {
    time,
    loadFixture,
  } = require("@nomicfoundation/hardhat-network-helpers");
  const { anyValue } = require("@nomicfoundation/hardhat-chai-matchers/withArgs");
  const { expect } = require("chai");
  const { Alchemy } = require("alchemy-sdk");  

describe("Test SingleTaxAccount", function () {
    async function deployOneYearLockFixture() {
       
        const [owner, otherAccount] = await ethers.getSigners();
    
        const SingleTax = await ethers.getContractFactory("SingleTaxContract");
        const singleTaxContract = await SingleTax.deploy();
    
        
        return { singleTaxContract, owner, otherAccount };
    }
    // деплоим токен
    async function deployToken() {
       
      const [owner, otherAccount] = await ethers.getSigners();
  
      const StateToken = await ethers.getContractFactory("StateToken");
      const stateToken = await StateToken.deploy();
  
      
      return { stateToken };
    }

    // деплоим нфт
    async function deployNFT() {
       
      const [owner, otherAccount] = await ethers.getSigners();
  
      const NftContract = await ethers.getContractFactory("NFTContract");
      const nftContract = await NftContract.deploy();
        
      return { nftContract, owner };
    }


    describe("Проверка развертывания", function () {
      
      it("Проверка собственника", async function () {
          const { singleTaxContract, owner } = await loadFixture(deployOneYearLockFixture);
    
          expect(await singleTaxContract.owner()).to.equal(owner.address);
        });
      it("Проверка на несобственника", async function () {
        const { singleTaxContract, owner, otherAccount } = await loadFixture(deployOneYearLockFixture);
          
        expect(await singleTaxContract.owner()).to.not.equal(otherAccount.address);
      });
    });

    describe("Проверка записи и чтения базы 'Налоги'", function () {
      
      
      it("Проверка taxDataDownload и readTaxes", async function () {
          const { singleTaxContract, owner } = await loadFixture(deployOneYearLockFixture);
          
          
        await singleTaxContract.taxDataDownload(
            ["0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266","0x70997970C51812dc3A010C7d01b50e0d17dc79C8","0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"],
            [["0x90F79bf6EB2c4f870365E785982E1f101E93b906"/*,"0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65"*/,"0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc"],
              ["0x976EA74026E726554dB657fA54763abd0C3a0aa9","0x14dC79964da2C08b23698B3D3cc7Ca32193d9955","0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f"],
              [/*"0xa0Ee7A142d267C1f36714E4a8F75612F20a79720","0xBcd4042DE499D14e55001CcbB24a551F3b954096",*/"0x71bE63f3384f5fb98995898A86B02Fb2426c5788"]],
            [[11,22],[4,5,6],[7]]);                    
                
        const arrayTax = await singleTaxContract.readTaxes(
              ["0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266","0x70997970C51812dc3A010C7d01b50e0d17dc79C8","0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"], 
              ["0x976EA74026E726554dB657fA54763abd0C3a0aa9","0x14dC79964da2C08b23698B3D3cc7Ca32193d9955","0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f"])
        //console.log(arrayTax);
        
        let result = [];
        for (let i = 0; i < arrayTax.length; i++){
          result.push(arrayTax[i].map((x) => {
            return (Number(BigInt(x)));
          }));
        }         
        //console.log(result);
        expect(result).to.eql([[0, 0, 0], [4, 5, 6], [0, 0, 0],]);
        
        });

      
    });
    describe("Проверка загрузки и чтения Списка налогов", function () {
      
      it("Проверяем uploadListTax и readListTax", async function () {
        const { singleTaxContract, owner } = await loadFixture(deployOneYearLockFixture);
        
        const arrListTax = ["0x90F79bf6EB2c4f870365E785982E1f101E93b906",
        "0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65","0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc",
        "0x976EA74026E726554dB657fA54763abd0C3a0aa9","0x14dC79964da2C08b23698B3D3cc7Ca32193d9955",
        "0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f","0xa0Ee7A142d267C1f36714E4a8F75612F20a79720",
        "0xBcd4042DE499D14e55001CcbB24a551F3b954096","0x71bE63f3384f5fb98995898A86B02Fb2426c5788"] ;
        const arrListTaxName = ["Tax1","Tax2","Tax3","Tax4","Tax5","Tax6","Tax7","Tax8","Tax9",];

        await singleTaxContract.uploadListTax(arrListTax, arrListTaxName);

        const arrListTaxContract = await singleTaxContract.readListTax();
        expect(arrListTax).to.eql(arrListTaxContract);
        
      });
    });


    
    describe("Проверка создания токена и передача на адрес", function () {
      
      it("Проверяем StateToken", async function () {
        
        const { stateToken } = await loadFixture(deployToken);
        // console.log("stateToken.address:", stateToken.address);
        // console.log("stateToken.signer.address:", stateToken.signer.address);
        // console.log("stateToken balance Signer:", ethers.utils.formatUnits(await stateToken.balanceOf(stateToken.signer.address)));
        const addrBusinessman = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8";
        
        const amount = "1.3"
        tx = await stateToken.transfer(addrBusinessman, ethers.utils.parseUnits(amount));
        await tx.wait();   
        
        const balanceBusinessman = ethers.utils.formatUnits(await stateToken.balanceOf(addrBusinessman))
        //console.log("stateToken balance Businessman:",balanceBusinessman);
        expect(balanceBusinessman).to.equal(amount);
      });
    });
    
    describe("Проверка оплаты налогов", function () {
      
      it("Проверяем payTax", async function () {
        
        const { singleTaxContract, owner , otherAccount} = await loadFixture(deployOneYearLockFixture);
        console.log("singleTaxContract.address:", singleTaxContract.address);
        
        const { stateToken } = await loadFixture(deployToken);
        const { nftContract } = await loadFixture(deployNFT);

        // адрес нфт отсылать до работы основного контракта
        await singleTaxContract.setAddrNFT(nftContract.address);
        console.log("nftContract.address:", nftContract.address);  
        // меняем собственника нфт до работы основного контракта
        await nftContract.transferOwnership(singleTaxContract.address);

        console.log("stateToken.address:", stateToken.address);
        console.log("stateToken.signer.address:", stateToken.signer.address);
        console.log("stateToken balance Signer:", ethers.utils.formatUnits(await stateToken.balanceOf(stateToken.signer.address)));
        // передаем токены бизнесмену
        const addrBusinessman = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8";        
        const allTax = "15";
        let amount = "8";
        tx = await stateToken.transfer(addrBusinessman, ethers.utils.parseUnits(amount));
        await tx.wait();   
        const balanceBusinessman = ethers.utils.formatUnits(await stateToken.balanceOf(addrBusinessman));
        console.log("stateToken balance Businessman:",balanceBusinessman);
        /*await owner.sendTransaction({ // скинем бизнесмену немного ETH на комиссии
          to: addrBusinessman,
          value: ethers.utils.parseEther("1.0") });
        */
        console.log("ETH balance Businessman:", ethers.utils.formatUnits(await otherAccount.getBalance()));

        
        // загружаем список налогов
        const arrListTax = ["0x90F79bf6EB2c4f870365E785982E1f101E93b906",
        "0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65","0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc",
        "0x976EA74026E726554dB657fA54763abd0C3a0aa9","0x14dC79964da2C08b23698B3D3cc7Ca32193d9955",
        "0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f","0xa0Ee7A142d267C1f36714E4a8F75612F20a79720",
        "0xBcd4042DE499D14e55001CcbB24a551F3b954096","0x71bE63f3384f5fb98995898A86B02Fb2426c5788"] ;
        const arrListTaxName = ["Tax1","Tax2","Tax3","Tax4","Tax5","Tax6","Tax7","Tax8","Tax9",];

        await singleTaxContract.uploadListTax(arrListTax, arrListTaxName);

        // загружаем налоги в контрант ЕНС
        await singleTaxContract.taxDataDownload(
          ["0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266","0x70997970C51812dc3A010C7d01b50e0d17dc79C8","0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"],
          [["0x90F79bf6EB2c4f870365E785982E1f101E93b906"/*,"0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65"*/,"0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc"],
            ["0x976EA74026E726554dB657fA54763abd0C3a0aa9","0x14dC79964da2C08b23698B3D3cc7Ca32193d9955","0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f"],
            [/*"0xa0Ee7A142d267C1f36714E4a8F75612F20a79720","0xBcd4042DE499D14e55001CcbB24a551F3b954096",*/"0x71bE63f3384f5fb98995898A86B02Fb2426c5788"]],
          [[ethers.utils.parseUnits("11"),
            ethers.utils.parseUnits("22")],
           [ethers.utils.parseUnits("4"),
            ethers.utils.parseUnits("5"),
            ethers.utils.parseUnits("6")],
           [ethers.utils.parseUnits("7")]
            ]);            
        const arrayTax = await singleTaxContract.readTaxes(
                ["0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266","0x70997970C51812dc3A010C7d01b50e0d17dc79C8","0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"], 
                ["0x976EA74026E726554dB657fA54763abd0C3a0aa9","0x14dC79964da2C08b23698B3D3cc7Ca32193d9955","0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f"])
          //console.log(arrayTax);
          
        let result = [];
        for (let i = 0; i < arrayTax.length; i++){
          result.push(arrayTax[i].map((x) => {
            return (Number(BigInt(x)));
          }));
        }     
        console.log(result);
       

        // вызывать payTax будет уже бизнесмен
        stateTokenOther = stateToken.connect(otherAccount);
        singleTaxContractOther= singleTaxContract.connect(otherAccount);
        // разрешаем Контракту тратить токены бизнесмена
        await stateTokenOther.approve(singleTaxContractOther.address, ethers.utils.parseUnits("15"))
        //console.log(await stateTokenOther.approve(singleTaxContractOther.address, ethers.utils.parseUnits("15")));

        await singleTaxContractOther.payTax(addrBusinessman, stateToken.address);
        
        let sl1 = +ethers.utils.formatUnits(await stateToken.balanceOf("0x976EA74026E726554dB657fA54763abd0C3a0aa9"));
        console.log("budget1:", sl1);
        let sl2 = +ethers.utils.formatUnits(await stateToken.balanceOf("0x14dC79964da2C08b23698B3D3cc7Ca32193d9955"));
        console.log("budget2:", sl2);
        let sl3 = +ethers.utils.formatUnits(await stateToken.balanceOf("0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f"));
        console.log("budget3:", sl3);
        
        console.log("qwerty:", (+allTax) - (sl1+sl2+sl3));
        if (((+allTax) - (sl1+sl2+sl3)) > 0) {
          amount = ((+allTax) - (sl1+sl2+sl3)).toString();
          tx = await stateToken.transfer(addrBusinessman, ethers.utils.parseUnits(amount));
          await tx.wait();   
          const balanceBusinessman = ethers.utils.formatUnits(await stateToken.balanceOf(addrBusinessman));
          console.log("stateToken balance Businessman:",balanceBusinessman);
          await singleTaxContractOther.payTax(addrBusinessman, stateToken.address);
        
          sl1 = +ethers.utils.formatUnits(await stateToken.balanceOf("0x976EA74026E726554dB657fA54763abd0C3a0aa9"));
          console.log("budget1:", sl1);
          sl2 = +ethers.utils.formatUnits(await stateToken.balanceOf("0x14dC79964da2C08b23698B3D3cc7Ca32193d9955"));
          console.log("budget2:", sl2);
          sl3 = +ethers.utils.formatUnits(await stateToken.balanceOf("0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f"));
          console.log("budget3:", sl3);
          expect(sl1+sl2+sl3).to.equal(15);
          
          const arrNFT = await singleTaxContract.readNFTTaxpayer(addrBusinessman);
          console.log("owner NFT:", addrBusinessman);
          console.log("arrNFT id:", arrNFT);

          for (let i = 0; i < arrNFT.length; i++ ) {
            console.log("metadata №", ethers.utils.formatUnits(arrNFT[i],0), ": ", await nftContract.tokenURI(arrNFT[i]));
          }
        }        
      });
    });
});