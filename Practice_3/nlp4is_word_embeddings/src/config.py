
"""
    This is the central config file
    @author: Gerhard Wohlgenannt (2017), ITMO University, St.Petersburg, Russia

    Here you can change pathes, add models, add new BOOK_SERIES, new dataset (towards the end of the file).
    But just to start with existing datasets and models, no change is needed
"""


BOOK_SERIES="IDIOT"

MODEL_PATH="../models/"

if BOOK_SERIES == "IDIOT":
    ## if you have a binary model, set the second value to "bin", else to "vec"
    METHODS = [ 
        ('IDIOT', 'vec'), # default and: -epoch 25 -ws 12
    ]

# -----------------------------------------------------
# for "doesnt_match" evaluation script
# -----------------------------------------------------

if BOOK_SERIES == "IDIOT":
    PRINT_DETAILS = False ## verbose debugging of eval results

    DOESNT_MATCH_FILE = "../datasets/questions_idiot_doesnt_match.txt"
    ANALOGIES_FILE = "../datasets/questions_idiot_analogies.txt"

    ### which sections to show in the paper..
    ANALOGIES_SECTIONS = ['firstname-lastname', 'geo-name-location', 'child-father', 'total']
    DOESNT_MATCH_SECTIONS = [': all',  ': location', 'TOTAL']
