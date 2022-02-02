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
    targetVirtualAddress = validateVirtualAddress(args.target_virtual_address)
    logging.info('Target Virtual Address: {}'.format(hex(targetVirtualAddress)))

    # Create a pe file object using the pefile python library
    peFileHandle = pefile.PE(peFile)

    # Print Important Structures
    e_lfanew = peFileHandle.DOS_HEADER.e_lfanew
    logging.debug('e_lfanew: 0x{:X}'.format(e_lfanew))

    SizeOfOptionalHeader = peFileHandle.FILE_HEADER.SizeOfOptionalHeader
    logging.debug('SizeOfOptionalHeader: 0x{:X}'.format(SizeOfOptionalHeader))

    NumberOfSections = peFileHandle.FILE_HEADER.NumberOfSections
    logging.debug('NumberOfSections: 0x{:X}'.format(NumberOfSections))

    ImageBase = peFileHandle.OPTIONAL_HEADER.ImageBase
    logging.debug('ImageBase: 0x{:X}'.format(ImageBase))

    # Iterate over the sections of the peFile
    for i, section in enumerate(peFileHandle.sections, start=0):
        logging.debug('section {}: VirtualAddress: 0x{:X}, Misc_VirtualSize: 0x{:x}, PointerToRawData: 0x{:x}'.format(i,
            section.VirtualAddress, section.Misc_VirtualSize, section.PointerToRawData))
        absoluteVirtualAddress = section.VirtualAddress + ImageBase

        # Determine if our targetVirtualAddress falls in this section
        if (absoluteVirtualAddress < targetVirtualAddress) and \
            (targetVirtualAddress < (absoluteVirtualAddress + section.Misc_VirtualSize)):
            # Found our Section!
            logging.debug('absoluteVirtualAddress: 0x{:x}'.format(absoluteVirtualAddress))

            # Calculate the offset
            filePointerOffset = targetVirtualAddress - absoluteVirtualAddress
            logging.debug('filePointerOffset: 0x{:x}'.format(filePointerOffset))

            # Calculate the file pointer
            targetFilePointer = section.PointerToRawData + filePointerOffset
            logging.debug('targetFilePointer: 0x{:x}'.format(targetFilePointer))

            # Print Final Output
            print('0x{:x} -> 0x{:x}'.format(targetVirtualAddress, targetFilePointer))

            # Exit
            sys.exit(0)

    # targetVirtualAddress does not fall in the sections of the peFile!

    # Print Final Output
    print('0x{:x} -> ??'.format(targetVirtualAddress))

    # Exit
    sys.exit(0)


if __name__ == "__main__":
    main()