import argparse
import logging
import pefile # Reference https://github.com/erocarrera/pefile
import sys

# Constants
E_MAGIC = b"\x4d\x5a"

def validatePeFile(x):
    """
    Validates the input file.
    """
    try:
        # Attempt to open the file
        with open(x, 'rb') as fileHandle:
            # Attempt to read the e_magic (4 bytes) from the input file
            e_magic = fileHandle.read(len(E_MAGIC))
            logging.debug("e_magic: {}".format(e_magic))

            # Validate e_magic
            if E_MAGIC != e_magic:
                logging.error("Input File \'{}\' is not a PE File.".format(x))
                sys.exit(1)
        return x
    except Exception:
        logging.error("Input File \'{}\' does not exist. Valid: path to \'<file>.exe\ file.'".format(x))
        sys.exit(1)

def validateVirtualAddress(x):
    """
    Validates the target virtual address.
    """
    try:
        # Attempt to convert the input string to an int
        return int(x, 16) if x[:2] == '0x' else int(x)
    except Exception:
        logging.error("Target Virtual Address \'{}\' is invalid. Valid: \'0x##\' (hexadecimal) or \'##\' (decimal).".format(x))
        sys.exit(1)

def main ():
    """
    This file implements the vapid assignment outlined at https://github.com/hawkinsw/CS5138/tree/main/Assignment1.
    """
    # Build arg parser
    parser = argparse.ArgumentParser(description='%(prog)s is a Virtual Address Pointer In Disk (vapid) translation \
        tool for 32-bit PE files.', usage='python3 ./%(prog)s <32-bit PE File> <Target Virtual Address>')
    parser.add_argument('pe_file', type=str, metavar='<32-bit PE File>', help='The name/path of a 32-bit PE File')
    parser.add_argument('target_virtual_address', type=str, metavar='<Target Virtual Address>',
        help='The target virtual address')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enables logging.')
    args = parser.parse_args()

    # Setup Log
    log_level = logging.DEBUG if args.verbose else logging.ERROR
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')

    # Validate Arguments
    peFile = validatePeFile(args.pe_file)
    logging.info('32-bit PE File: {}'.format(peFile))
    iTargetAddress = validateVirtualAddress(args.target_virtual_address)
    logging.info('Target Virtual Address: {}'.format(hex(iTargetAddress)))

    # Create a pe file object using the pefile python library
    peFileHandle = pefile.PE(peFile)
    logging.debug('e_lfanew: 0x{:X}'.format(peFileHandle.DOS_HEADER.e_lfanew))

    # Exit
    sys.exit(0)

if __name__ == "__main__":
    main()