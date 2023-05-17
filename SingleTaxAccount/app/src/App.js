
import './App.css';

import { Card, CardHeader, CardBody, CardFooter } from '@chakra-ui/react'
import {
  Box,
  Button,
  Center,
  Flex,
  Heading,
  Image,
  Input,
  SimpleGrid,
  Text,
  CircularProgress,
  Progress,
  Divider,
  StackDivider,
  Link,
} from '@chakra-ui/react';

import {
  Table,
  Thead,
  Tbody,
  Tfoot,
  Tr,
  Th,
  Td,
  TableCaption,
  TableContainer,
} from '@chakra-ui/react'
import {
  List,
  ListItem,
  ListIcon,
  OrderedList,
  UnorderedList,
} from '@chakra-ui/react'
import { Stack, HStack, VStack } from '@chakra-ui/react'
import { Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react'

import { useEffect, useState } from 'react'; 

import init from './init.js'; 
import assigntax from './assigntax.js'; 
import addressContracts from './address-contracts.js';

import { ethers } from 'ethers';
import { useMetaMask, MetaMaskProvider } from "metamask-react";
import { Alchemy, Network, Utils } from 'alchemy-sdk';


 
function App() { 
  const [bankAccount, setBankAccount] = useState({}); // банковский аккаунт
  const [tokenAccount, setTokenAccount] = useState(0);  // аккаунт в токенах
  const [provider, setProvider] = useState();               // провайдер
  const [signer, setSigner] = useState();               // подписант
  const [singleTaxContract, setSingleTaxContract] = useState();  // TaxContract
  const [stateToken, setStateToken] = useState();               // StateToken
  const [nftContract, setNftContract] = useState();               // NFT
  const [listTax, setListTax] = useState();               // list tax
  const [arrayTaxBusnessman, setTaxBusnessman] = useState([]);               // list tax
  const [arrayTaxPaidBisnessman, setArrayTaxPaidBisnessman] = useState([]);  // сколько оплачено
  const [initTrue, setInitTrue] = useState(false);               // инициализация завершена
  const [convertToken, setConvertToken] = useState("");  
  const [payToken, setPayToken] = useState("");  
  const [debt, setDebt] = useState(0);
  const [flagTaxPaidAll, setFlagTaxPaidAll] = useState(false);
  const [nftTaxPaid, setNftTaxPaid] = useState([]);
  
  const { status, connect, account, chainId, ethereum } = useMetaMask();
  
  // хук метамаска - меняем в метамаске аккаунт - меняется всё это хозяйство 
  
  console.log("status:", status); 
  if (status === "connected") { 
    //setCurrentAccount(account); 
    console.log("Current account in metamask:", account);     
  }

  // получение списка размера налогов налогоплательщика 
  useEffect(() => { 
    
    async function getTaxBusnessman() {
          
      const arrayTaxPaidBisnessmanTmp = await singleTaxContract.readTaxPaid(
        [account],  
        Object.keys(listTax));

        const arrayTaxPaidBusnessman = arrayTaxPaidBisnessmanTmp[0].map((x) => {
          return (Number(ethers.utils.formatUnits(x)))});

      // сохраним значения оплат по налогам
      console.log("arrayTaxPaidBusnessman:", arrayTaxPaidBusnessman);
      setArrayTaxPaidBisnessman(arrayTaxPaidBusnessman);  

      const arrayTaxBusnessmanTmp = await singleTaxContract.readTaxes(
        [account],  
        Object.keys(listTax));

        const arrayTaxBusnessman = arrayTaxBusnessmanTmp[0].map((x) => {
        return (Number(ethers.utils.formatUnits(x)))});

      // сохраним налоги
      console.log("arrayTaxBusnessman:" , arrayTaxBusnessman);      
      setTaxBusnessman(arrayTaxBusnessman); // получение списка размера налогов налогоплательщика
      

      // считываем кол-во токенов 
      const tokenAcc = ethers.utils.formatUnits(await stateToken.balanceOf(account));      
      setTokenAccount(tokenAcc);  

    
    } 
    getTaxBusnessman();  
  }, [account, initTrue]); // запускаться будет только один  раз
  
  useEffect(() => { 
    // !!! деплоим наши контракты в localhost - при тестнесе этоно не надо
    async function getContract () {
        const { provider, signer , singleTaxContract, stateToken, nftContract, ListTax, bankBusinessmans} = await init(addressContracts);  
        setProvider(provider);
        setSigner(signer);
        setSingleTaxContract(singleTaxContract);
        setStateToken(stateToken);
        setNftContract(nftContract);
        setListTax(ListTax);
        setInitTrue(true);
        setBankAccount(bankBusinessmans);
        console.log("signerState1:", signer.address);   
        console.log("singleTaxContract1:", singleTaxContract.address);  
        console.log("stateToken1:", stateToken.address);  
        console.log("bankBusinessmans1:", bankBusinessmans);  
      
    }      
    getContract();    
    
  }, []); // запускаться будет только один  раз

  useEffect(() => {
    async function getDebt() {
      const debtTmp = (arrayTaxBusnessman.reduce((total, item) => total + item).toFixed(2) - 
                    arrayTaxPaidBisnessman.reduce((total, item) => total + item).toFixed(2)).toFixed(2);
      setDebt(debtTmp);
    }
    getDebt();
  },[arrayTaxBusnessman, arrayTaxPaidBisnessman]);
  
  // читаем выпущенные на налогоплательщика NFT
  useEffect(() => {
    async function getNFT() {

      let arrNftTaxPaidTmp = [];
      
        setFlagTaxPaidAll(false);
        console.log("debt:", debt);
      
          const arrNFT = await singleTaxContract.readNFTTaxpayer(account);
          console.log("mint NFT on:", account);
          console.log("arrNFT id:", arrNFT);

          for (let i = 0; i < arrNFT.length; i++ ) {            
            let uriTmp = await nftContract.tokenURI(arrNFT[i]);    
            console.log("uriTmp:", uriTmp);
            arrNftTaxPaidTmp[i] = JSON.parse(uriTmp);
            console.log("metadata №", ethers.utils.formatUnits(arrNFT[i],0), ": ", arrNftTaxPaidTmp[i]);
          }
          console.log("arrNftTaxPaidTmp:", arrNftTaxPaidTmp);
          setNftTaxPaid(arrNftTaxPaidTmp);
                
    }
    getNFT();
  },[flagTaxPaidAll, account]);
 
  
  // конвертирует $ в STT
  async function depositToken() {
      // считываем из поля ввода
      // если не ноль - банковский счет уменьшаем на сумму
      // а на налогоплательщику переводим STT
      if (convertToken > 0) {
        console.log("convertToken:", String(convertToken));

        console.log("account:", account);
        console.log("bankAccount:", bankAccount[account]);
        if ((bankAccount[account]-convertToken) >= 0)
        {
            const bankAccountTmp = bankAccount;
            let remainder = bankAccountTmp[account]-convertToken;
            bankAccountTmp[account] = remainder.toFixed(2);
            console.log("bankAccountTmp:", bankAccountTmp); 
            setBankAccount(bankAccountTmp);
           
            console.log(`balance STT of Businessman: ${ethers.utils.formatUnits(await stateToken.balanceOf(account))} ${await stateToken.symbol()}`);    
    
            console.log("======= convert ==========");
        
            const tx = await stateToken.transfer(account, ethers.utils.parseUnits(convertToken));
            await tx.wait();   
        
            const tokenAcc = ethers.utils.formatUnits(await stateToken.balanceOf(account));
            console.log(`balance Exchanger: ${ethers.utils.formatUnits(await stateToken.balanceOf(stateToken.signer.address))} ${await stateToken.symbol()}` );
            console.log(`balance STT of Businessman:", ${tokenAcc} ${await stateToken.symbol()}`);    
            setTokenAccount(tokenAcc);            
        } 
        else
        {
          alert("There are not enough funds in your bank account!");
        }  
      }
      setConvertToken("");
  }

  // обработка кнопки Pay - платим в бюджеты
  async function PayTokenToBudget() {
    // устанавливаем подписанта  - текущий аккаунт
    const providerMM = new ethers.providers.Web3Provider(window.ethereum); 
    await providerMM.send("eth_requestAccounts", []);
    const payer = providerMM.getSigner();
    
    // вызывать payTax будет уже бизнесмен
    const stateTokenPayer = stateToken.connect(payer);
    const singleTaxContractPayer = singleTaxContract.connect(payer);    
    const payerAddr = await payer.getAddress();
    console.log("payer:", payerAddr);
    console.log("stateTokenPayer:", stateTokenPayer.address);
    console.log("singleTaxContractPayer:", singleTaxContractPayer.address);

    let arrayTaxPaidBisnessmanTmp = await singleTaxContract.readTaxPaid(
      [account],  
      Object.keys(listTax));

    let arrayTaxPaidBisnessman = arrayTaxPaidBisnessmanTmp[0].map((x) => {
      return (Number(ethers.utils.formatUnits(x)))});
    console.log("Оплачено налогов arrayTaxPaidBusnessman:", arrayTaxPaidBisnessman); 
    setArrayTaxPaidBisnessman(arrayTaxPaidBisnessman); 
    
    console.log("STT у налогоплательщика", ethers.utils.formatUnits(await stateToken.balanceOf(account)));
  
    const remainder = 
      arrayTaxBusnessman.reduce((total, item) => total + item) - 
      arrayTaxPaidBisnessman.reduce((total, item) => total + item);
    console.log("Остаток по налогам remainder:", remainder); 
     
    // разрешаем Контракту тратить токены бизнесмена
    if (remainder <= 0) {
      alert("No tax debt!"); // Задолженность по налогам отсутствует      
    }
    else if (remainder < payToken) {
      alert("You entered more than required!"); // Ввели больше чем надо
    }
    else {
      
      console.log("payToken:", payToken);
      await stateTokenPayer.approve(singleTaxContractPayer.address, ethers.utils.parseUnits(String(remainder)));

      console.log("1:");
      const tx = await singleTaxContractPayer.payTax(account, stateTokenPayer.address);
      console.log("2:");
      await tx.wait();
      console.log("3:");
      arrayTaxPaidBisnessmanTmp = await singleTaxContract.readTaxPaid(
        [account],  
        Object.keys(listTax));
      console.log("4:");
        arrayTaxPaidBisnessman = arrayTaxPaidBisnessmanTmp[0].map((x) => {
            return (Number(ethers.utils.formatUnits(x)))});
      
      setArrayTaxPaidBisnessman(arrayTaxPaidBisnessman);  
      console.log("arrayTaxPaidBisnessmanTmp:", arrayTaxPaidBisnessman); 

      for (let i = 0; i < Object.keys(listTax).length; i++) {
        console.log("budget:", i, " = ", ethers.utils.formatUnits(await stateTokenPayer.balanceOf(Object.keys(listTax)[i])));
      }
      const debtTmp = (arrayTaxBusnessman.reduce((total, item) => total + item).toFixed(2) - 
                    arrayTaxPaidBisnessman.reduce((total, item) => total + item).toFixed(2)).toFixed(2);
      if (debtTmp == 0) setFlagTaxPaidAll(true);                   
    }
    
    setPayToken(""); 
    // считываем кол-во токенов 
    const tokenAcc = ethers.utils.formatUnits(await stateToken.balanceOf(account));      
    setTokenAccount(tokenAcc);  
  }

  // обновим состояния нового налога
  async function getNewAssignTax(event) {
    await assigntax(event);
    setInitTrue(!initTrue);
  }

  return (
    <div className="App">
      
      
      <Tabs variant='enclosed' align="center">
        <TabList>
          <Tab>Сurrent Tax</Tab>
          <Tab>Payment History</Tab>
          <Tab>Addresses</Tab>
          <Tab>Test</Tab>
        </TabList>
        <TabPanels >
          <Flex align="center" justify="center">    
            <TabPanel id='currentTax'  >
              <HStack spacing='124px'>
                <VStack                  
                  spacing={4}
                  align='stretch'>
                  <Card>
                    <CardHeader>
                      <Heading size='lg'>Account</Heading>
                    </CardHeader>
                    <Divider orientation='horizontal' />
                    <CardBody>
                      <Text fontSize='md'>{account}</Text>                    
                    </CardBody>        
                  </Card>
                  <Card>                  
                    <CardHeader>
                      <Heading size='lg'>Tax Notice
                      </Heading>                 
                    </CardHeader>
                    <Divider orientation='horizontal' />
                    <CardBody>
                      <TableContainer>
                        <Table size='sm'>
                          <Thead>
                            <Tr>
                              <Th>Tax</Th>                  
                              <Th isNumeric>Amount of tax</Th>
                            </Tr>
                          </Thead> 
                          
                          <Tbody>
                            { arrayTaxBusnessman.length ? 
                              (
                                arrayTaxBusnessman.map((e, i) => {
                                  if (e > 0) {
                                    return (
                                        <Tr key={e.id}>
                                          <Td>{Object.values(listTax)[i]}</Td>                  
                                          <Td isNumeric>{arrayTaxBusnessman[i].toFixed(2)}</Td>
                                        </Tr>                                 
                                    );}   
                                  } ) 
                              ) : ('') 
                            }                          
                          </Tbody>
                          <Divider orientation='horizontal' />
                          <Tfoot>
                            <Tr>
                              <Th>Total</Th>
                              <Th isNumeric>{
                                arrayTaxBusnessman.length ? 
                                (arrayTaxBusnessman.reduce((total, item) => total + item).toFixed(2)) : ("")                               
                              }</Th>
                            </Tr>
                          </Tfoot>
                        </Table>
                      </TableContainer>
                    </CardBody>        
                  </Card>
                  
                  <Card>
                    <CardHeader>
                      <Heading size='lg'>Bank`s Account</Heading>
                    </CardHeader>
                    <Divider orientation='horizontal' />
                    <CardBody>
                    {
                      bankAccount[account] >= 0 ?
                      (<Text>$ {Number(bankAccount[account]).toFixed(2)}</Text>) :
                      ("")
                    }
                    </CardBody>        
                  </Card>

                  <Card>
                    <CardHeader>
                      <Heading size='lg'>StateToken's Account</Heading>
                    </CardHeader>
                    <Divider orientation='horizontal' />
                    <CardBody> 
                      {
                        bankAccount[account] >= 0 ?
                        (<Text>{Number(tokenAccount).toFixed(2)} STT</Text>) :
                        ("")
                      }                    
                    </CardBody>        
                  </Card>
                  
                  <Card>
                    <CardHeader>
                      <Heading size='lg'>Convert $ to tokens</Heading>
                    </CardHeader>
                    <Divider orientation='horizontal' />
                    <CardBody>
                      <Input 
                        id="inputToken"
                        placeholder='$ 1 = 1 STT' 
                        onChange={(e) => setConvertToken(e.target.value)}
                        type='number' 
                        value={convertToken}                      
                      />
                      
                      <Button 
                      colorScheme='blue'                    
                      onClick={depositToken}
                      >                    
                        Convert
                      </Button>
                    </CardBody>        
                  </Card>
                </VStack>
                <VStack spacing={4}
                  align='stretch'> 
                  <Card>
                      <CardHeader>
                        {                       
                        debt > 0 ?
                        (<Heading size='lg'><Text>It is possible to pay the tax in full or in part</Text>                        
                          <Text>You have {Number(tokenAccount).toFixed(2)} of the {arrayTaxBusnessman.length > 0 ? 
                          debt : ("")} STT</Text>
                          </Heading>) : 
                          (<Heading size='lg'><Text>No tax arrears</Text>
                          </Heading>) 
                        }
                        
                      </CardHeader>
                      <Divider orientation='horizontal' />
                      <CardBody>                      
                        <Button colorScheme='blue'
                          onClick={PayTokenToBudget}>
                          Pay
                        </Button>
                      </CardBody>        
                  </Card>

                  {!true ? "": 
                    <VStack spacing={4}
                    align='stretch'>  
                      <Card>
                        <CardHeader>
                        <Heading size='lg'>You paid taxes</Heading> 
                          
                        </CardHeader>
                        <Divider orientation='horizontal' />
                        <CardBody>
                          <TableContainer>
                          <Table size='sm'>
                            <Thead>
                              <Tr>
                                <Th>Tax</Th>                  
                                <Th isNumeric>Amount of tax</Th>
                              </Tr>
                            </Thead>

                            <Tbody>
                              { arrayTaxBusnessman.length ? 
                                (
                                  arrayTaxBusnessman.map((e, i) => {
                                    if (e > 0) {
                                      return (
                                          <Tr key={e.id}>
                                            <Td>{Object.values(listTax)[i]}</Td>                  
                                            <Td isNumeric>{arrayTaxPaidBisnessman[i].toFixed(2)}</Td>
                                          </Tr>                                 
                                      );}   
                                    } ) 
                                ) : ('') 
                              }                          
                            </Tbody>
                          <Divider orientation='horizontal' />
                            <Tfoot>
                              <Tr>
                                <Th>Total</Th>
                                <Th isNumeric>{
                                arrayTaxPaidBisnessman.length ? 
                                (arrayTaxPaidBisnessman.reduce((total, item) => total + item).toFixed(2)) : ("")                               
                                }</Th> 
                              </Tr>
                              <Tr> 
                                <Th>Debt</Th>
                                <Th isNumeric>{
                                arrayTaxBusnessman.length > 0 ? (debt) : ("")                               
                                }</Th>
                              </Tr>
                            </Tfoot>
                          </Table>
                        </TableContainer>
                        </CardBody>        
                      </Card>
                      <Card>         
                        <CardBody>
                          <CardHeader>
                            <Heading size='md'>NFT is issued to your account as proof of tax payment</Heading> 
                            <Heading size='md'>You can see all the NFTs credited to your account</Heading> 
                            <Heading size='md'>on the "Payment history" tab</Heading>                           
                          </CardHeader>                        
                        </CardBody>        
                      </Card>  
                    </VStack>      
                  }                
                </VStack>
              </HStack>  

            </TabPanel>            
          </Flex>
          <Flex align="center" justify="center">
            <TabPanel id='/paymentHistory'>
              <VStack spacing={4}
                  align='stretch'>               
                {
                  nftTaxPaid.map((e, i) => {
                    return(
                      <Card>
                      <CardHeader>
                            <Heading size='lg'>
                              <Text>{nftTaxPaid[i].name}</Text>
                              <Text>{nftTaxPaid[i].description}</Text>      
                            </Heading>
                      </CardHeader>
                          <Divider orientation='horizontal' />
                      <CardBody>
                                          
                          <Text>{nftTaxPaid[i].atribute[0].trait_type} : {(String(new Date(nftTaxPaid[i].atribute[0].value*1000)).slice(0, (String(new Date(nftTaxPaid[i].atribute[0].value*100)).indexOf("(")-1)))}</Text>
                          <Text>{nftTaxPaid[i].atribute[1].trait_type} : {Number(ethers.utils.formatUnits(nftTaxPaid[i].atribute[1].value,18)).toFixed(2)} STT</Text>
                          <Text>{nftTaxPaid[i].atribute[2].trait_type} :</Text>
                          <Box textAlign='left' display='inline-block'>
                          <UnorderedList  >{
                              nftTaxPaid[i].atribute[2].value.length ? 
                              (
                                nftTaxPaid[i].atribute[2].value.map((e, j) => {
                                   
                                    return (
                                      
                                      <ListItem > 
                                        {nftTaxPaid[i].atribute[2].value[j].tax_name} : {Number(ethers.utils.formatUnits(nftTaxPaid[i].atribute[2].value[j].value, 18)).toFixed(2)} STT
                                      </ListItem>   
                                                             
                                    );   
                                  } ) 
                              ) : ('') 
                          }</UnorderedList>
                          </Box>
                      </CardBody>        
                    </Card> 
                    );
                  })
                }              
              </VStack>
            </TabPanel>
          </Flex>
          <Flex align="center" justify="center">
            <TabPanel>
              <VStack spacing={4}
                  align='stretch'>      
                      <Card>                        
                        <CardHeader>
                              <Heading size='lg'>
                                Addresses Smart-Contracts and Accounts     
                              </Heading>
                        </CardHeader>
                            <Divider orientation='horizontal' />
                        <CardBody>                          
                          <Stack direction='column'>
                            <Text>Current taxpayer: </Text>                            
                            <Text>{account}</Text>                               
                            <Divider orientation='horizontal' />
                            <Text>Owner TAX Smart Contract - State: </Text>
                            <Text>
                                {addressContracts.adressOwner}
                            </Text>
                            <Divider orientation='horizontal' />
                            <Text>TAX Smart Contract: </Text>
                            <Text>
                                {addressContracts.addressTaxContract}
                            </Text>
                            <Divider orientation='horizontal' />
                            <Text>STT Token: </Text>
                            <Text>
                                {addressContracts.addressToken}
                            </Text>
                            <Divider orientation='horizontal' />
                            <Text>TAX NFT: </Text>
                            <Text>
                                {addressContracts.addressNFT}
                            </Text>   
                            <Divider orientation='horizontal' />
                            
                              { arrayTaxBusnessman.length ? 
                                (
                                  Object.keys(listTax).map((e, i) => {
                                    
                                      return (
                                        <Box>
                                          <Text>{Object.values(listTax)[i]}:</Text>
                                          <Text>
                                              {Object.keys(listTax)[i]}
                                          </Text>   
                                          <Divider orientation='horizontal' />                              
                                        </Box>
                                      );  
                                    } ) 
                                ) : ('') 
                              }  
                            
                            
                          </Stack>
                        </CardBody>        
                    </Card> 
              </VStack>
            </TabPanel>
          </Flex>
          <Flex align="center" justify="center">
            <TabPanel>
              <VStack spacing={4}
                  align='stretch'>      
                      <Card>                        
                      <CardHeader>
                            <Heading size='lg'>
                              Assign taxes     
                            </Heading>
                      </CardHeader>
                          <Divider orientation='horizontal' />
                      <CardBody>
                        You can assign taxes as a check
                        <Stack direction='column'>
                          <Button colorScheme='red' value={"1"} onClick={getNewAssignTax}>Assign a tax</Button>
                          <Button colorScheme='yellow' value={"2"} onClick={getNewAssignTax}>Assign another tax</Button>
                          <Button colorScheme='green' value={"3"} onClick={getNewAssignTax}>Assign a third tax</Button>  
                        </Stack>
                      </CardBody>        
                    </Card> 
              </VStack>
            </TabPanel>
          </Flex>
        </TabPanels>
      </Tabs>
      
      
    </div>
  );
}

export default App;
