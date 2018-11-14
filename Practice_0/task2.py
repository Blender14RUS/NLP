specSymbols = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~«»"""
#set flags for place where space is needed
def where_space(char):
    befor = False
    after = True
    #after this symbols don't print space
    if char in "[(«\"":
        befor = True
        after = False
    #spaces on both sides
    elif char == '-':
        befor = True
        after = True
    #shouldn't be rounded
    elif char == '.':
        befor = False
        after = False
    return befor, after


def process_lines(lines, out):
    sentence = ""
    after = True
    for line in lines:
        first_column = line.split()[0].strip()
        #skip other tags
        #replace </s> to new line
        if first_column.startswith('<'):
            if first_column == "</s>":
                out.write(sentence.lstrip(' ') + "\n")
                sentence = ""
            continue
        # whitespace
        if first_column in specSymbols:
            befor, after = where_space(first_column)
            sentence += (" " if befor else "") + first_column
        else:
            sentence += (" " if after else "") + first_column
            after = True

pathToFile = "./ru_ar_cut.txt"
pathToResultFile = "./task2_text.txt"
lines = ""
with open(pathToFile, 'r', encoding='utf-8') as file:
    lines = file.readlines()
with open(pathToResultFile, "w", encoding='utf-8') as out:
    process_lines(lines, out)

