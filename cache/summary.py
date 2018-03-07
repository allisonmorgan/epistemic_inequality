import pickle

DIR_CS_SI = "CS_SI.p"
DIR_HIS_SI = "HIS_SI.p"
DIR_BUSI_SI = "BUSI_SI.p"

DIR_CS_SI_JUMP_PROBABILITY = "random_jump/CS_SI.p"
DIR_HIS_SI_JUMP_PROBABILITY = "random_jump/HIS_SI.p"
DIR_BUSI_SI_JUMP_PROBABILITY = "random_jump/BUSI_SI.p"

dirs = [DIR_CS_SI, DIR_HIS_SI, DIR_BUSI_SI]

all_departments_SI = [("Business", DIR_BUSI_SI), ("Computer Science", DIR_CS_SI), ("History", DIR_HIS_SI)]
all_departments_SI_random_jump = [("Business", DIR_BUSI_SI_JUMP_PROBABILITY), ("Computer Science", DIR_CS_SI_JUMP_PROBABILITY), ("History", DIR_HIS_SI_JUMP_PROBABILITY)]


def n_trials_of_dir(cache_dir):
    cache = pickle.load(open(cache_dir, 'rb'))
    try:
        a_prob_key = cache["size"].iterkeys().next()
        a_node_key = cache["size"][a_prob_key].iterkeys().next()
        a_sizes_val = cache["size"][a_prob_key][a_node_key]
        return len(a_sizes_val)
    except:
        return 0

if __name__ == "__main__":
	# Returns how many trials there are for each epidemic with a particular transmission
	# probability and starting from a particular node.
    print ">>> SI"
    for (title, cache_dir) in all_departments_SI:
        print("Number of trials: {0}\tTitle: {1}".format(n_trials_of_dir(cache_dir), title))

    print ">>> SI + RANDOM HOP"
    for (title, cache_dir) in all_departments_SI_random_jump:
        print("Number of trials: {0}\tTitle: {1}".format(n_trials_of_dir(cache_dir), title))