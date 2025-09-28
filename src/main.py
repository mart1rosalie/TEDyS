from elements_transposables import gillespie
from elements_transposables import arguments as arg

if __name__ == '__main__':
    #-s 5 -bh 0.06 -dh 0.04 -a 2e-4 -phi 1.5e-4 -bt 0.001 -dt 1e-4 -pa 0.3 -popGenome 1000  -popTe 120 -time 500 -o data.csv
    args = arg.receipt_of_arguments()

    # Modeling parameters
    bh = args.bh # 0.06
    dh = args.dh # 0.04
    αh = args.a # 2e-4 #2e-5
    φ = args.phi # 1.5e-4
    bt = args.bt # 0.001
    dt = args.dt # 1e-4
    rt = bh - dh
    duration = args.time
    seed = args.s
    p_a = args.pa

    verbose = False
    if args.verbose:
        verbose = True

    # Simulation
    gillespie.simulation(duration,seed,p_a,args.o,args.popGenome,args.popTe,args.init,args.bh,args.dh, args.a, args.phi, args.bt, args.dt,verbose)
