pathToFile = "./ru_ar_cut.txt"
pathToResultFile = "./parseResult.txt"


resultContent = ""
i = 0

with open(pathToFile, "r", encoding="utf8") as file:
    with open(pathToResultFile, "a+", encoding="utf8") as resultFile:
        lines = file.readlines()[:1000000]
        wasWord = False
        for line in lines:
            i = i + 1
            print(i)
            firstWord = line.partition('\t')[0]
            if firstWord != '<p>\n' and firstWord != '</p>\n' and firstWord != '<g/>\n' and firstWord != '</doc>\n' and not firstWord.startswith('<doc') and not firstWord.startswith('<p'):
                if firstWord == '</s>\n':
                    resultContent = resultContent + "\n"
                elif firstWord == "," or firstWord == "\"" or firstWord == "!" or firstWord == "?":
                    resultContent = resultContent + firstWord
                elif firstWord == "(" or firstWord == "�":
                    resultContent = resultContent + " " + firstWord
                    wasWord = False
                elif firstWord == ")" or firstWord == "�":
                    resultContent = resultContent + firstWord
                    wasWord = False
                elif firstWord == "<s>\n":
                    resultContent = resultContent + "\n"
                elif firstWord != '<s>\n':
                    if wasWord and firstWord != ".":
                        resultContent = resultContent + " " + firstWord
                    else:
                        resultContent = resultContent + firstWord

                    wasWord = True

        resultFile.write(resultContent)
