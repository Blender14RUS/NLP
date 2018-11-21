from Practice_3.nlp4is_word_embeddings.src.config import *
import gensim.models

def load_models(mode=None, emb_type=None):

    if emb_type == "vec": binary = False
    elif emb_type == "bin": binary = True
    else: raise Exception()

    print("\n\n**** Model:", mode, " binary:", binary)

    word_model = gensim.models.KeyedVectors.load_word2vec_format(MODEL_PATH + mode + ".model", binary=binary)

    word_model.init_sims(replace=True) # clean up RAM
  
    return word_model, None

def print_details(task_res, msg):
    print("\n" + msg)
    for res in task_res:
        print("Task: %s -- Found: %s -- Correct: %s\n" % (res[0], res[1], res[2]))


def print_latex_version(results, method, FILTER_SECTIONS):
    """
        create a latex version of the results dictionary 
        --> for easy updates of publication data
    """
    vals, counts = [],[]
    for sec, data in results.items():

        if not sec in FILTER_SECTIONS:
            continue

        vals.append(str(round(data['perc'], 3)))
        counts.append(str(data['counts']))

    print('Number of tasks:       &', " & ".join(counts) , " \\\\ \hline \hline")
    print(method, "               & ", " & ".join(vals) , " \\\\ \hline")


if __name__ == "__main__":
    model, crap = load_models(mode='IDIOT_preproc', emb_type='vec')
    print('\n\nMODEL', model)
