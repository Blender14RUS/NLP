def process_lines(lines, out):
    sentence = ""
    for line in lines:
        first_column = line.split()[0].strip()
        #skip other tags
        #replace </s> to new line
        if first_column.startswith('<'):
            if first_column == "</s>":
                out.write(sentence.lstrip(' ') + "\n")
                sentence = ""
            continue

        sentence += " " + first_column

pathToFile = "./ru_ar_cut.txt"
pathToResultFile = "./task2_text.txt"
lines = ""
with open(pathToFile, 'r', encoding='utf-8') as file:
    lines = file.readlines()
with open(pathToResultFile, "w", encoding='utf-8') as out:
    process_lines(lines, out)

