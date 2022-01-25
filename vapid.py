import argparse
import logging
import os
import sys

def validateInputFile(x):
    """
    Validates the input file.
    """
    if os.path.isfile(x):
        return x
    else:
        logging.error("Input File \'{}\' does not exist.".format(x))
        sys.exit(1)


def validateVirtualAddress(x):
    """
    Validates the target virtual address.
    """
    return x

def main ():
    """
    This file implements the vapid assignment outlined at https://github.com/hawkinsw/CS5138/tree/main/Assignment1.
    """
    
    # Build arg parser
    parser = argparse.ArgumentParser(description='Virtual Address Pointer In Disk')
    parser.add_argument('input_file', type=validateInputFile, help='The name/path of a 32-bit PE File')
    parser.add_argument('target_virtual_address', type=validateVirtualAddress, help='The target virtual address')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Enables Verbose Logging')
    args = parser.parse_args()

    # Validate Arguments 


    # Setup Log
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')
    logging.debug('Verbose Logging Enabled.')

    # Exit 
    sys.exit(0)
    
if __name__ == "__main__":
    main()