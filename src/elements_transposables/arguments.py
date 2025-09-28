import argparse

def receipt_of_arguments():
    """
    Function which take the arguments in entrance
    """
    parser = argparse.ArgumentParser(
        description='Modelisation of TEs dynamics for asexual individuals',
    )

    parser.add_argument(
        '-o',
        type=str,
        help='Output data file. (Default: 000_all.csv)',
        default='rstat/0000_all.csv',
    )
    parser.add_argument(
        '-time',
        type=int,
        help='Delta time (Default: 10000)',
        default=10000,
    )
    parser.add_argument(
        '-popGenome',
        type=int,
        help='Initial population size. (Default: 100)',
        default=100,
    )
    parser.add_argument(
        '-popTe',
        type=int,
        help='Initial number of TEs per host. (Default: 3)',
        default=3,
    )
    parser.add_argument(
        '--verbose',
        help='Verbose execution',
        action="store_true",
    )

    required_args = parser.add_argument_group('required arguments')

    required_args.add_argument(
        '-s',
        type=int,
        help='Random seed',
        required=True,
    )
    required_args.add_argument(
        '-bh',
        type=float,
        help='Host birth rate',
        required=True,
    )
    required_args.add_argument(
        '-dh',
        type=float,
        help='Host death rate',
        required=True,
    )
    required_args.add_argument(
        '-a',
        type=float,
        help='Competition rate',
        required=True,
    )
    required_args.add_argument(
        '-phi',
        type=float,
        help='Deleterious effects of TE',
        required=True,
    )
    required_args.add_argument(
        '-bt',
        type=float,
        help='TE Transposition rate',
        required=True,
    )
    required_args.add_argument(
        '-dt',
        type=float,
        help='TE Deletion rate',
        required=True,
    )
    required_args.add_argument(
        '-pa',
        type=float,
        help='Proportion of active copies. Mandatory for PARTIAL type model',
        required=True,
    )
    required_args.add_argument(
        '-init',
        type=int,
        help='Know what type of installation to use',
        required=True,
    )
    
    args = parser.parse_args()
    return args