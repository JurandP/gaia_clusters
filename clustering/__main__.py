def prepare_argparse():
        parser = argparse.ArgumentParser()
        parser.add_argument("-b", "--bin_size", type=int,
            help="Add size of bins to divide spectrum. Default --bin_size = 3", default=3)
        parser.add_argument("-m", "--only_max", type=str2bool,
            help="Use only information about spectra in maximum of lightcurve. \
            Default --only_max = True", default=True)

    return parser


def main()
    args = prepare_argparse()

if __name__ == '__main__':
    main()
