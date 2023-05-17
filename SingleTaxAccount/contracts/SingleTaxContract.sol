//SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;


import "hardhat/console.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "./NFTContract.sol";

contract SingleTaxContract {
    enum statusTaxpayer {ACTIV, INACTIVE}
    struct taxpayerID {        
        mapping(address => uint) taxes;     // на входе адрес бюджета - на выходе величина налога
        mapping(address => uint) taxPaid;   // на входе адрес бюджета - на выходе уплаченный налог
        mapping(address => uint) debt;      // на входе адрес бюджета - на выходе остаток по налогу - на дату начисления следующего налога - по сути на это начисляется пеня
        address[] listTax;                   // хранение чисто налогов налогоплательщика
        uint taxBalance;                    // остаток по налогам
        uint amountTax;                     // величина налога
        bool status;                        // ставится один раз при назначении налога - значит бизнесмен действующий
        bool taxPaidNoDebt;                 // налог оплачен - долгов нет
    }
    // businessman's taxes: 
    // address(1) - businessman's address
    // address(2) - budget institution's address
    // uint - amount of tax to a budgetary institution
    mapping(address => taxpayerID) public taxpayers;
    
    // 
    mapping(address => uint[]) arrIdNFT; // на входе адрес бизнесмена - на выходе адрес его NFT

    address public owner;
    address[] public listTax;
    mapping (address => string) listTaxNames;
    IERC20 public token; 
    address addrNFT;
    uint internal periodTax;

    constructor() { 
        // Set the transaction sender as the owner of the contract.
        owner = msg.sender; 
        periodTax = 0;         
    }

    
    // The taxDataDownload() function is responsible for loading tax data 
    // for each businessman into the contract
    // array address[] addrBisnesman - array of businessmen's addresses
    // array address[] addrBudgetInstitution - array of addresses of budgetary institutions
    // uint[] tax - array of taxes to budgetary institutions
    function taxDataDownload(
        address[] calldata addrBisnesman, 
        address[][] calldata addrBudgetInstitution, 
        uint[][] calldata tax 
        ) external onlyOwner{
            
            for(uint i = 0; i < addrBisnesman.length; i++) {

                taxpayers[addrBisnesman[i]].listTax = new address[](0); // обнулим массив адресов налогов налогоплательщика
                taxpayers[addrBisnesman[i]].taxBalance = 0;
                //console.log("addrBudgetInstitution[i].length: ", addrBudgetInstitution[i].length);//, taxes);
                for(uint j = 0; j < addrBudgetInstitution[i].length; j++) {
                    //console.log("tax[i][j]: ", tax[i][j]);
                    // сохраняем остаток по налогу на дату начисления нового налога -  
                    // это должно начилсяться пеня, штраф
                    taxpayers[addrBisnesman[i]].debt[addrBudgetInstitution[i][j]] = 
                        (taxpayers[addrBisnesman[i]].taxes[addrBudgetInstitution[i][j]] - 
                        taxpayers[addrBisnesman[i]].taxPaid[addrBudgetInstitution[i][j]]);
                                        
                    taxpayers[addrBisnesman[i]].taxes[addrBudgetInstitution[i][j]] = tax[i][j]; // ввод нового налога
                    taxpayers[addrBisnesman[i]].listTax.push(addrBudgetInstitution[i][j]);      // сохраняем налог в массиве
                    taxpayers[addrBisnesman[i]].taxPaid[addrBudgetInstitution[i][j]] = 0; // остаток обнуляется
                    taxpayers[addrBisnesman[i]].taxBalance += tax[i][j];                    
                    taxpayers[addrBisnesman[i]].status = true; //statusTaxpayer.ACTIV;
                    taxpayers[addrBisnesman[i]].taxPaidNoDebt = false; // 
                    //console.log("taxes[addrBisnesman[i]][addrBudgetInstitution[i][j]]: ", taxes[addrBisnesman[i]][addrBudgetInstitution[i][j]]);
                    //console.log("taxes[addrBisnesman[i]]: ", taxpayers[addrBisnesman[i]].status);
                }
                taxpayers[addrBisnesman[i]].amountTax = taxpayers[addrBisnesman[i]].taxBalance; //statusTaxpayer.ACTIV;
            }
            periodTax += 1; 
            //console.log("!!!!!!!!!!taxDataDownload2: ");//, taxes);

        }

    // Function readTaxes() provides data from the mapping() taxes; 
    // address[] addrBisnesman - array of businessmen's addresses
    function readTaxes(address[] calldata _addrBisnesman, address[] calldata _addrBudgetInstitution) 
        view 
        external 
        returns (uint[][] memory) 
    {        
        uint[][] memory _taxes = new uint[][] (_addrBisnesman.length);
        /*console.log("!!!!!!!!!!readTaxes !!!!!!!!!!");//, taxes);
        console.log("_addrBisnesman: ", _addrBisnesman[0]);//, taxes);
        console.log("!!!!!!!!!!_addrBudgetInstitution: ", _addrBudgetInstitution[1]);//, taxes);*/
        //console.log("taxes: ", taxes[_addrBisnesman[0]][_addrBudgetInstitution[2]]);
        for(uint i = 0; i < _addrBisnesman.length; i++) {
            
            //console.log(_addrBisnesman.length);     

            uint[] memory _taxesTmp = new uint[] (_addrBudgetInstitution.length);
            for(uint j = 0; j < _addrBudgetInstitution.length; j++) {
                    //console.log("taxes[_addrBisnesman[i]][_addrBudgetInstitution[j]]: ", taxes[_addrBisnesman[i]][_addrBudgetInstitution[j]]);     
                    _taxesTmp[j] = taxpayers[_addrBisnesman[i]].taxes[_addrBudgetInstitution[j]];
                    //console.log("_taxesTmp: ", _taxesTmp[j]);     
                }
            _taxes[i] = _taxesTmp;              
        }        
        return _taxes;
    }

    function readTaxPaid(address[] calldata _addrBisnesman, address[] calldata _addrBudgetInstitution) 
        view 
        external 
        returns (uint[][] memory) 
    {        
        uint[][] memory _taxesPaid = new uint[][] (_addrBisnesman.length);
        /*console.log("!!!!!!!!!!readTaxes !!!!!!!!!!");//, taxes);
        console.log("_addrBisnesman: ", _addrBisnesman[0]);//, taxes);
        console.log("!!!!!!!!!!_addrBudgetInstitution: ", _addrBudgetInstitution[1]);//, taxes);*/
        //console.log("taxes: ", taxes[_addrBisnesman[0]][_addrBudgetInstitution[2]]);
        for(uint i = 0; i < _addrBisnesman.length; i++) {
            
            //console.log(_addrBisnesman.length);     

            uint[] memory _taxesPaidTmp = new uint[] (_addrBudgetInstitution.length);
            for(uint j = 0; j < _addrBudgetInstitution.length; j++) {
                    //console.log("taxes[_addrBisnesman[i]][_addrBudgetInstitution[j]]: ", taxes[_addrBisnesman[i]][_addrBudgetInstitution[j]]);     
                    _taxesPaidTmp[j] = taxpayers[_addrBisnesman[i]].taxPaid[_addrBudgetInstitution[j]];
                    //console.log("_taxesTmp: ", _taxesTmp[j]);     
                }
            _taxesPaid[i] = _taxesPaidTmp;              
        }        
        return _taxesPaid;
    }

    // функция по загрузке списка налогов и их названий
    function uploadListTax(address[] calldata _listTax, string[] calldata _listTaxNames) external onlyOwner{
        listTax = _listTax;
        for (uint i = 0; i < _listTaxNames.length; i++) {
            listTaxNames[_listTax[i]] = _listTaxNames[i];
        }
    }
    function readListTax() external view onlyOwner returns (address[] memory ) {
        return listTax;
    }

    // функция по оплате налогов
    function payTax(address _addrBisnesman, address _token) public {
        uint realBalanceTaxpayer;
        uint koef; // 2<<18
        uint tax;
        // проверка наличия плательщика в базе 
        console.log("status:",taxpayers[_addrBisnesman].status);

        require(taxpayers[_addrBisnesman].status, "TaxPayer not found");

        // проверяем - хватает ли у нас токенов для полной оплаты
        // смотрим сколько у нас баланса токенов у налогоплательщика
        token = IERC20(_token);
        console.log("_token address:", _token);
   
        realBalanceTaxpayer = token.balanceOf(msg.sender); 
        console.log("realBalanceTaxpayer:", realBalanceTaxpayer);
        require(realBalanceTaxpayer > 0, "No Tokens"); // если токены есть - продолжаем
       
        console.log("taxpayers[_addrBisnesman].taxBalance: ", taxpayers[msg.sender].taxBalance);
        console.log("address(this):", address(this));
               
        // допустим платим налоги пропорционально
        // увеличиваем систему счисления в 2^18
        koef = (realBalanceTaxpayer << 18) / taxpayers[_addrBisnesman].taxBalance;
        console.log("koef1:", koef);
        if (koef > (1<<18)) {
            koef = (1<<18);
        }
        console.log("koef2:", koef);
        console.log("msg.sender:", msg.sender);
        console.log("address(this):", address(this));
        uint allmoney = token.allowance(msg.sender, address(this));
        console.log("allmoney:", allmoney);

        for (uint8 i = 0; i < listTax.length; i++) {
            //console.log("listTax:", listTax[i]);
            if (taxpayers[_addrBisnesman].taxes[listTax[i]] > 0) {
                console.log("Budget:", listTax[i]);
                tax = (((
                    (taxpayers[_addrBisnesman].taxes[listTax[i]] - taxpayers[_addrBisnesman].taxPaid[listTax[i]])
                    * koef) 
                    >> 18) / 10**16)*(10**16); // вычисляем налог для оплаты                
                console.log("tax:", tax);
                bool sent = token.transferFrom(_addrBisnesman, listTax[i], tax);    // посылаем в соответствующий бюджет
                require(sent, "Token transfer failed");
                taxpayers[_addrBisnesman].taxBalance -= tax;             // уменьшаем задолженность
                taxpayers[_addrBisnesman].taxPaid[listTax[i]] += tax;
                console.log("taxBalance:", taxpayers[_addrBisnesman].taxBalance);
                console.log("taxPaid:", taxpayers[_addrBisnesman].taxPaid[listTax[i]]);
                allmoney = token.allowance(msg.sender, address(this));
                console.log("allmoney:", allmoney);

                // если налог оплачен - ставим флаг об оплате налога
                if (taxpayers[_addrBisnesman].taxBalance == 0) {
                    taxpayers[_addrBisnesman].taxPaidNoDebt = true;
                    console.log("nftContract.address: ", addrNFT);
                    mintNFT(addrNFT);                          
                }
            } 
        }   

    }


    function mintNFT(address _addrNFT) internal {
        NFTContract nftContract = NFTContract(_addrNFT);
        string memory tmpTaxName = ""; 

        for (uint i = 0; i < taxpayers[msg.sender].listTax.length; i++) {     
            //console.log("mintNFT tax:", i, " : ", taxpayers[msg.sender].listTax[i]);    
            //console.log("mintNFT listTax:", i, " : ", listTax[i]); 
            //console.log("mintNFT amount:", i, " : ", taxpayers[msg.sender].taxPaid[taxpayers[msg.sender].listTax[i]]);   
            
            tmpTaxName = string.concat(tmpTaxName, 
                '{"tax_name":"',
                listTaxNames[taxpayers[msg.sender].listTax[i]], 
                '",',
                '"value":"', 
                Strings.toString(taxpayers[msg.sender].taxPaid[taxpayers[msg.sender].listTax[i]]),
                '"}',(i < (taxpayers[msg.sender].listTax.length-1))?",":"");
        }
        

        string memory json = string.concat('{"name":"TAX NFT",\
        "description":"Proof of payment of taxes - #',Strings.toString(periodTax),'",\
        "atribute":[{"trait_type":"Date of payment","value":"',Strings.toString(block.timestamp),'"},\
        {"trait_type":"Amount of Tax","value":"',Strings.toString(taxpayers[msg.sender].amountTax),'"},\
        {"trait_type":"List of Tax","value":[',tmpTaxName,']}]}');
        console.log("1-");
        uint256 tokenid = nftContract.safeMint(msg.sender, json);
        console.log("2-");
        arrIdNFT[msg.sender].push(tokenid);
        console.log("3-");
        
    }

    function readNFTTaxpayer(address _taxpayer) public view returns(uint[] memory) {
        return arrIdNFT[_taxpayer];
    }
    
    // загрузка адреса NFT
    function setAddrNFT(address _addrNFT) public onlyOwner {
        addrNFT = _addrNFT;
    }
    // Modifier to check that the caller is the owner of
    // the contract.
    modifier onlyOwner() {
        console.log("owner: ", msg.sender);
        require(msg.sender == owner, "Not owner");
        // Underscore is a special character only used inside
        // a function modifier and it tells Solidity to
        // execute the rest of the code.
        _;
    }

}