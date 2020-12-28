pragma solidity ^0.5.0;
import 'zeppelin-solidity/contracts/token/ERC20/ABCD.sol';

contract AshyPay is StandardToken, Ownable { 

  string public name          = 'AshyPay';
  string public symbol        = 'ASH';
  uint8 public decimals       = 18;
  uint public INITIAL_SUPPLY  = 1000;



  constructor(){
    totalSupply_ = INITIAL_SUPPLY * (10**uint(decimals));
    balances[msg.sender] = totalSupply_;
  }

  function setOwner(string _n) public onlyOwner returns (bool)
  {
    Owner = _n;
    return true;
  }

  function getOwner() public view returns (string) {
    return Owner;
  }


}
