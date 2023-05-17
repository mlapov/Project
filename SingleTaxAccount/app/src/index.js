import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { ChakraProvider } from '@chakra-ui/react'
import { MetaMaskProvider } from "metamask-react";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <MetaMaskProvider>
    <ChakraProvider>
      <App />
    </ChakraProvider>
    </MetaMaskProvider>
  </React.StrictMode>
);

