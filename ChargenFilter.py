#!/usr/bin/python

import sys
import argparse


def getLinePQR(recordName, serial, atomName, residueName, chainID, residueNumber, X, Y, Z, charge):
    space = "                                                                                          "
    line = space
    line = recordName + line
    line = line[:7] + serial + line[7:]
    line = line[:13] + atomName + line[13:]
    line = line[:18] + residueName + line[18:]
    line = line[:22] + chainID + line[22:]
    line = line[:23] + residueNumber + line[23:]
    line = line[:31] + X + line[31:]
    line = line[:39] + Y + line[39:]
    line = line[:47] + Z + line[47:]
    line = line[:55] + charge + line[55:]
    # line = line[:77] + atomName + line[77:]
    # line = line[:79] + 'P' + line[79:]
    return line + '\n'


def getInformation(fileobj, start_line="ATOMIC_POSITIONS (angstrom)", lines_left=0, end_line='\n', appendUntil=''):
    active = False
    positions = []
    tempLine = ''
    for line in fileobj:
        if active == False:
            if line.find(start_line) != -1:
                positions = []
                active = True
        else:
            if lines_left > 0:
                lines_left = lines_left - 1
                continue
            if end_line == '\n':
                if line != end_line:
                    if appendUntil == '':
                        positions.append(line.split())
                    else:
                        if line.find(appendUntil) != -1:
                            tempLine = tempLine + line
                            positions.append(tempLine.split())
                            tempLine = ''
                        else:
                            tempLine = tempLine + line[:-1]
                else:
                    active = False
            else:
                if line.find(end_line) != -1:
                    active = False
                else:
                    if line == '\n':
                        continue
                    else:
                        if appendUntil == '':
                            positions.append(line.split())
                        else:
                            if line.find(appendUntil) != -1:
                                tempLine = tempLine + line
                                positions.append(tempLine.split())
                                tempLine = ''
                            else:
                                tempLine = tempLine + line[:-1]
    return positions


def banner():
    print '''
  ___ _                           ___ _ _ _           
 / __| |_  __ _ _ _ __ _ ___ _ _ | __(_) | |_ ___ _ _     
| (__| ' \/ _` | '_/ _` / -_) ' \| _|| | |  _/ -_) '_|    
 \___|_||_\__,_|_| \__, \___|_||_|_| |_|_|\__\___|_|      
       .   .     , |___/    .     .     .                 
                  ,# #   ,         ,# #                   
   ,*(//,*/*/,*////*#(**//*(*/ *////*##**/ *///,*/**/*/   
    *  / #  *    / *#*//. .  / ( .(.****.(.   .  . .  /   
    .../.#../ .  , *.*,(     * #  * *#*/ *    .       /   
   */(//*/(//*/(///#.(*/(//(//./(////##*//./(//*//*/(//   
                                    /  .                  
 Developed by:                     / .  ,                 
  M. de la Rosa (Eraledm)          * .,@#,@ /             
   and P.G Nieto-Delgado               ,@* %                
	'''


def main():
    parser = argparse.ArgumentParser(
        description='This script formats the outputs of Quantum Espresso to convert it to a PQR format, allowing to have partial charges',
        epilog="Please, report any error"
    )
    parser.add_argument('-x', '--input-xyz',
                        type=argparse.FileType('r'),
                        help="name of pw.x output file with atomic positions")

    parser.add_argument('-t', '--type-calc',
                        type=str,
                        choices=['scf', 'relax'],
                        help="type of calculus output from -x argument")

    parser.add_argument('-e', '--input-energy',
                        type=argparse.FileType('r'),
                        help="name of file with atomic energy")

    parser.add_argument('-c', '--input-charges',
                        type=argparse.FileType('r'),
                        help="name of file with atomic charge")

    parser.add_argument('-o', '--output',
                        help="name of output file")

    parser.add_argument('-p', '--polarization',
                        action='store_true',
                        help="change charge for polarization")

    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    if args.input_xyz is None or args.input_charges is None or args.input_energy is None:
        # parser.print_help()
        print('\n\nERROR: Input(s) file(s) not defined?\n\n')
        sys.exit()

    if args.type_calc is None:
        # parser.print_help()
        print('\n\nERROR: Type of calculus output not defined. Use sfc, relax...\n\n')
        sys.exit()

    banner()
    print ('    [*] Getting positions')
    sline = "s"
    eline = "s"
    lline = 0
    aline = ''

    if args.type_calc == 'scf':
        sline = 'ATOMIC_POSITIONS'
        eline = 'CELL_PARAMETERS'
        aline = 'polarization'
    if args.type_calc == 'relax':
        sline = "Begin final coordinates"
        eline = "End final coordinate"
        lline = 2

    positions = getInformation(
        args.input_xyz,
        start_line=sline,
        end_line=eline,
        lines_left=lline)

    print len(positions)

    print ('    [*] Getting pseudopotencials')
    pseudo = getInformation(
        args.input_energy,
        start_line="atomic species   valence    mass     pseudopotential")

    pseudoPotencital = {}
    for ps in pseudo:
        pseudoPotencital[ps[0]] = ps[1]


    print ('    [*] Getting Lowdin Charges')
    charges = getInformation(
        args.input_charges,
        start_line="Lowdin Charges: ",
        end_line="Spilling Parameter",
        lines_left=1,
        appendUntil=aline)

    print len(charges)

    if len(positions) != len(charges):
        print('\n\nERROR: Inputs not from the same molecule?\n\n')
        sys.exit()

    name = ''
    if args.output is not None:
        if args.polarization == False:
            name = args.output+'.pqr'
        else:
            name = args.output+'_polarization.pqr'

    outputFile = open(name, 'w')

    print ('    [*] Generating PQR format')
         i = i+1
    for i, pos in enumerate(positions):
        if args.polarization == False:
            line = getLinePQR("HETATM", str(i+1), pos[0], 'UNK', '', str(i+1), '%.3f' % float(pos[1]), '%.3f' % float(pos[2]), '%.3f' % float(pos[3]),  '%.3f' % (
                float(pseudoPotencital[pos[0]]) - float(charges[i][6][:-1])))
        else:
            line = getLinePQR("HETATM", str(i+1), pos[0], 'UNK', '', str(i+1), '%.3f' % float(
                pos[1]), '%.3f' % float(pos[2]), '%.3f' % float(pos[3]),  '%.3f' % (float(charges[i][44][:-1])))
        if args.output is None:
            print (line[:-1])
        else:
            outputFile.write(line)

    if args.output is not None:
        print ('    [*] Generating ' + name + ' file')
        outputFile.close()

    print ('    [*] Done...')


if __name__ == "__main__":
    main()
