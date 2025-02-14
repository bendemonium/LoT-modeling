import numpy as np
import random
import itertools
import Levenshtein
import difflib
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

class StringGenerator:

    def __init__(self, symbol_sets, len_seq, n_seq=6, n_rounds=1000):
        self.symbol_sets = symbol_sets
        self.len_seq = len_seq
        self.symbols = set.union(*symbol_sets)
        self.n_seq = n_seq
        self.n_rounds = n_rounds

    class Round:
        
        def __init__(self, symbol_sets, len_seq, n_seq=6):
            self.symbol_sets = symbol_sets
            self.len_seq = len_seq
            self.n_seq = n_seq
            self.sequences = self.round(n_seq)
            self.sequence_list = list(itertools.chain.from_iterable(self.sequences))
            self.pairs = list(itertools.combinations(self.sequence_list, 2))
            self.levenshtein = np.array([Levenshtein.distance(s1, s2) for s1, s2 in self.pairs])
            self.lcs = np.array([self.longest_common_substring(s1, s2) for s1, s2 in self.pairs])
            self.lcs_len = np.array([len(lcs) for lcs in self.lcs])

        @staticmethod
        def longest_common_substring(s1, s2):
            matcher = difflib.SequenceMatcher(None, s1, s2)
            match = matcher.find_longest_match(0, len(s1), 0, len(s2))
            return s1[match.a: match.a + match.size]

        def sequencer(self):
            permutations = ["".join(random.sample(list(symbol_set), self.len_seq)) for symbol_set in self.symbol_sets]
            return permutations
    
        def round(self, n_seq):
            sequences = []
            for _ in range(n_seq):
                sequences += [self.sequencer()]
            return sequences

    class Simulator:

        def __init__(self, parent, n_seq=6, n_rounds=1000):
            self.parent = parent
            self.n_seq = n_seq
            self.n_rounds = n_rounds
            self.levenshtein = None
            self.lcs = None
            self.lcs_len = None
            self.lcs_len_norm = None
            
        def run_simulation(self):
            all_levenshtein = []
            all_lcs = []
            all_lcs_length = []
            len_seq = self.parent.len_seq
            
            for _ in range(self.n_rounds):
                round_instance = self.parent.Round(self.parent.symbol_sets, self.parent.len_seq, self.n_seq)
                all_levenshtein.extend(round_instance.levenshtein)
                all_lcs.extend(round_instance.lcs)
                all_lcs_length.extend(round_instance.lcs_len)

            # Store the results as attributes of the instance
            self.levenshtein = np.array(all_levenshtein)
            self.similarity = 1 - (self.levenshtein / len_seq)
            self.lcs = np.array(all_lcs)
            self.lcs_len = np.array(all_lcs_length)
            self.lcs_len_norm = self.lcs_len / len_seq

            return (self.levenshtein, self.lcs_len, self.similarity, self.lcs_len_norm, len_seq)
            

def plot_simulation(metrics):
    
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Metric Distributions", fontsize=16)
    
    metric1, metric2, metric3, metric4, len_seq = metrics
    titles = ["Levenshtein Distance", "Longest Common Substring", "Similarity", "Longest Common Substring (normalized)"]

    for i, (metric, title) in enumerate(zip([metric1, metric2, metric3, metric4], titles)):
        ax = axes[i // 2, i % 2]

        if i < 2:  # Top two plots (discrete bins, integer x-ticks from 0 to len_seq)
            sns.histplot(metric, discrete=True, bins=int(max(metric) - min(metric) + 1), ax=ax)
            ax.set_xticks(range(0, len_seq + 1))  # X-ticks from 0 to len_seq
        else:  # Bottom two plots (len_seq bins)
            sns.histplot(metric, bins=len_seq, ax=ax)

        ax.set_title(title, fontsize=14)
        ax.set_xlabel("Value", fontsize=12)
        ax.set_ylim(0, 120000)  # Set y-limits

        # Display count on top of each bar
        for patch in ax.patches:
            height = patch.get_height()
            if height > 0:
                ax.annotate(f'{int(height)}', 
                            (patch.get_x() + patch.get_width() / 2., height),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
