## Challenge Description
In this challenge we are given a staking manager which lets us stake some tokena and provides us LP tokens in return. We also get rewards based on the time after which we withdraw and also on the total supply of LP token available as of now.

## Initial Observation
The setup contract has initially staked `100000` tokens and thus increased the total supply of the LP tokens. To win we will need to return 10 ETH back to the setup contract where we initially withdrew 1 ETH from it. Now how do we increase 1 ETH to 10 ETH because the reward per token per second [see here](./contracts/StakingManager.sol#L36) after the setup contract has provided liquidity is too low. We will have to wait longer than the session for it to pass.

## Vulnerability
After inspection i was convinced that there was no flaw in the manager contract so where could it then be. It turns out the LP token contract allows anyone to burn off the tokens [here](./contracts/LpToken.sol#L18) and thus reduce totalsupply and manipulate rewards in the manager contract.

After this we need to just script the [solution](./new.py) with some help from GPT4.o . 