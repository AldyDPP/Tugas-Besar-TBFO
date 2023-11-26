from Input_Handling.PDAconfig import*
from Input_Handling.htmltokenizer import*
from PDA_Model.PushDownAutomaton import*
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('pdaconfig', help='')
parser.add_argument('htmlpath', help='')

arguments = parser.parse_args()

def read_file_lines(file_name):
    lines = []
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line)
    return lines


# main
# Initialize PDA and tokenize HTML file
PDA = getPDA(arguments.pdaconfig)
InputTokens, rowinfo, colinfo = TokenizeThisHtmlFile(arguments.htmlpath)

# Initialize start node
start_node = node(PDA.start_state, InputTokens, stack(PDA.start_symbol))
start_nodes = PDA.epsilonclosure(start_node)

# DEBUGGER MODE HERE!
# set the debugmode to true and you good to go!
RemainingTokensLength,Accepted = compute(PDA, start_nodes, 1, debugmode = False)
ErrorIndex = len(InputTokens) - RemainingTokensLength

# Output
if (Accepted):
    print("\x1b[32mAccepted\033[0m")
else:
    if ErrorIndex == len(InputTokens) - 1: 
        # I don't know why but I guess the indexing got messed up somewhere
        Line = rowinfo[0]
        Column = colinfo[0]
    else:
        Line = rowinfo[ErrorIndex+1]
        Column = colinfo[ErrorIndex+1]

    print(f"\x1b[31mSyntax Error\x1b[36m" + f" at [Ln {Line}, Col {Column}]:\033[0m\n", end="")

    # print the error line
    lines = read_file_lines(arguments.htmlpath)
    Line = lines[Line - 1]
    length = len(Line)
    print(Line, end = "")
    print("`" * Column + "^")