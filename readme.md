#A simulation of Betin's spin and win wheel, 
![Betin's Spin and win fontend ](https://github.com/p-netm/Bsaw/blob/plotting/figures/snp.png)


## objective
The aim is to see if there is a possible combination of bets and arbitraged stakes that might be best in reducing the overall risk and thus, atleast maintain a winning average round of waging.

### implementation
creates a permutation of all possible bet combinations and uses basic statistics to caclulate an arbitrage such that for a certain choosen combination of staking, if the result is a part of the combination then you are guaranteed a win. eg. if we take the combination x2,x4,x20,  then arbitrage makes sure that if the outcome is any of the above you will still make enough money more than your initial stake.

the choosen combination is then simulated over an arbitrary number of  simulations with an arbitrary initial starting capital.

the simulator plots the changes in the waging stake through the simulations and plots it only if the end result is greater than the initial capital which is to say that there was profit made

## a few Results plots

![plot image of 100 simulations ](https://github.com/p-netm/Bsaw/blob/plotting/figures/Figure_3.png)
![plot image of 100 simulations ](https://github.com/p-netm/Bsaw/blob/plotting/figures/Figure_4.png)

For a large number of simualtions/ iterations i.e. wage iterations such as greater than 150, the bookie is guaranteed to win all your money
![plot image of 1000 simulations ](https://github.com/p-netm/Bsaw/blob/plotting/figures/Figure_5.png)
