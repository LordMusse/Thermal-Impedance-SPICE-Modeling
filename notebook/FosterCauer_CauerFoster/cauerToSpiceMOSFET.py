# # Spice SubCircuit format to myCR data format converter
# 2019/05/06 created by Tom HARA
# 2025/05/18 edited by LordMusse from line 71 to fit modified SOAtherm format
import argparse
import datetime

# version of this script
myVersion = '0.0.01'

##############################################################################
# arg parsing
##############################################################################
parser = argparse.ArgumentParser(
    prog='myCRformat2Spice.py',
    usage='myCR data format to Spice SubCircuit format converter.',
    epilog='end',
    add_help=True
    )

parser.add_argument('input_file', help='specify input filename',
                    action='store', type=str)
parser.add_argument('output_file', help='specify output filename',
                    action='store', type=str)
parser.add_argument('junction_to_ambient', help='specify junction to ambient thermal resistance(use dot as decimal divider))',
                    action='store', type=str)
parser.add_argument('-f', '--FosterNetwork',
                    help='consider input file as Foster ' +
                    'network. Default: Cauer Network.',
                    action='store_true')

parser.add_argument('--version', action='version',
                    version='%(prog)s ' + myVersion)

args = parser.parse_args()

# Input file and output file:
input_file = args.input_file
output_file = args.output_file
junction_to_ambient = args.junction_to_ambient
isFoster = args.FosterNetwork
cauerOrFoster = "FOSTER" if isFoster else "CAUER"

##############################################################################

"""
https://stackoverflow.com/questions/13890935/does-pythons-time-time-return-the-local-or-utc-timestamp
"""
# time stamp when the script started.
timestamp = str(datetime.datetime.now()).split('.')[0].replace(":", "-")

with open(input_file, 'r', encoding="utf-8") as fileobj:
    datastr = fileobj.read()         # read all data from a file
    adatastr = datastr.rstrip()      # remove the last "\n"
    datalist = adatastr.split("\n")  # create a list (size: n row * 1 column)

c_list = list()                      # a list for foster network Cth
r_list = list()                      # a list for foster network Rth

for line in datalist:                # read one row at a time
    tmplist = line.split()           # split a row into a list
    # print(tmplist)
    if tmplist == []:                # skip empty rows
        continue
    if tmplist[0][0] == '#':         # skip comment rows
        continue
    if tmplist[0][0:6] == "STAGES":  # number of RC stages
        stages = int(tmplist[1])
        print("stages = " + str(stages))
        continue
    # start reading actual data
    # (1st column is stage number)
    c_list.append(float(tmplist[1]))        # Cth on the 2nd column
    r_list.append(float(tmplist[2]))        # Rth on the 3rd column

with open(output_file, "w") as fileobj:
    tmpstring = ""
    # header
    tmpstring = "***************************************************\n"
    fileobj.write(tmpstring)
    tmpstring = "* MOSFET SOAtherm shield format\n"
    fileobj.write(tmpstring)
    tmpstring = "* Created: " + timestamp + "\n"
    fileobj.write(tmpstring)
    tmpstring = "* First stage (C1 and R1) is connected to the Junction.\n"
    fileobj.write(tmpstring)
    tmpstring = "* nth stage (Cn and Rn) is connected to the Case.\n"
    fileobj.write(tmpstring)
    tmpstring = "***************************************************\n"
    fileobj.write(tmpstring)

    tmpstring = ".SUBCKT transistorThermal Drain Gate Source Drain2 Gate2 Source2 1 " + str(stages+1) + " T_Ambient\n\n"
    fileobj.write(tmpstring)

    tmpstring = "*** current sensing ***\n\n"
    fileobj.write(tmpstring)

    tmpstring = "* Drain current sense \n"
    fileobj.write(tmpstring)
    tmpstring = "RsenseDrain Drain Drain2 .01m\n\n"
    fileobj.write(tmpstring)

    tmpstring = "* Current sense Gate \n"
    fileobj.write(tmpstring)
    tmpstring = "RsenseGate Gate Gate2 1m\n\n"
    fileobj.write(tmpstring)

    tmpstring = "* Current sense Source (used in SOAtherm but not here) \n"
    fileobj.write(tmpstring)
    tmpstring = "RsenseSource Source Source2 .01m\n\n"
    fileobj.write(tmpstring)

    tmpstring = "* Calculation of power dissipated P_D\n"
    fileobj.write(tmpstring)
    tmpstring = "BI1 0 1 I=(V(Drain,Source)*I(RsenseDrain) + V(Gate,Source)*I(RsenseGate))\n\n"
    fileobj.write(tmpstring)

    tmpstring = "*** Thermal Circuit from Junction to Case ***\n"
    fileobj.write(tmpstring)

    tmpstring = "** Junction to Ambient **\n"
    fileobj.write(tmpstring)
    tmpstring = "Rth 1 T_Ambient " + str(junction_to_ambient) + "\n\n"
    fileobj.write(tmpstring)

    tmpstring = "** cauer chain **\n"
    fileobj.write(tmpstring)

    if isFoster:
        for i in range(stages):
            tmpstring = "C" + str(i+1) + " " + str(i+1) + " " + \
                        str(i+2) + " " + str(c_list[i]) + "\n"
            fileobj.write(tmpstring)
            tmpstring = "R" + str(i+1) + " " + str(i+1) + " " + \
                        str(i+2) + " " + str(r_list[i]) + "\n"
            fileobj.write(tmpstring)
    else:  # Cauer network, as default
        for i in range(stages):
            tmpstring = "C" + str(i+1) + " " + str(i+1) + " " + \
                        "0 " + str(c_list[i]) + "\n"
            fileobj.write(tmpstring)
            tmpstring = "R" + str(i+1) + " " + str(i+1) + " " + \
                        str(i+2) + " " + str(r_list[i]) + "\n"
            fileobj.write(tmpstring)

    tmpstring = "\n.ENDS transistorThermal\n"
    fileobj.write(tmpstring)
