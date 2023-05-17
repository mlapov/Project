//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract StateToken is ERC20 {
    uint constant _initial_supply = 1500005 * (10**18);
    constructor() ERC20("StateToken", "STT") {
        _mint(msg.sender, _initial_supply);
    }
}