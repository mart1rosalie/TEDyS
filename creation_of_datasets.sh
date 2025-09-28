#!/bin/bash

#init, seed, phi, alpha_h, b_h, d_h, b_t, d_t, p_a, init_te

init=( 1 2 3 )
init_te=( 1 5 10 )
phi_tab=( 1.75e-4 1.80e-4 1.85e-4 1.90e-4 1.95e-4 2e-4 )
alpha_h=( 2e-5 )
p_a=( 0.1 0.3 )

b_h=0.06
d_h=0.04
b_t=0.001
d_t=1e-4

number_of_simulations=2

file=initialization_of_simulations.csv

if [ -e $file ]
then
    rm $file
fi

touch $file
echo "init, seed, phi, alpha_h, b_h, d_h, b_t, d_t, p_a, init_te" >> $file

seed=94

x=0
for i in ${init[@]} # loop for all simulations
do
    te=${init_te[$x]}

    for phi in ${phi_tab[@]}
    do
        for alpha in ${alpha_h[@]}
        do
            for pa in ${p_a[@]}
            do
                for _ in `seq 1 $number_of_simulations` #number of simulations for each parameter
                do
                    printf "$i, %.5d, $phi, $alpha, $b_h, $d_h, $b_t, $d_t, $pa, $te \n" $seed >> $file
                    let "seed++"
                done
            done
        done
    done
done
