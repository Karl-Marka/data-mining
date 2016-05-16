#!/usr/bin/python

class CodonManager:

   
    def __init__(self, input_string):
        self.initial_string = input_string

    def closest(self, split_index, a, b):
        assert split_index > 0
        assert split_index < len(self.initial_string) * 3

        combinations = CodonManager.get_combinations(self.initial_string, split_index)

#        print("Combinations: %d" % len(combinations))

        try:
            min_temp = float(a)
        except:
            min_temp = None

        try:
            max_temp = float(b)
        except:
            max_temp = None

        list1, list2 = CodonManager.generate_lists(combinations, split_index, min_temp, max_temp)

#        print("List 1: %d" % len(list1))
#        print("List 2: %d" % len(list2))

        closest, closest1, closest2 = CodonManager.find_closest_values(list1, list2)

        if closest is not None:
            codonOutput = []
            for i, codon in enumerate(closest1):
                print "%s = %s \n" % (codon, closest2[i])
   #             codonOutput.append(output)
   #        print codonOutput
        else:
            print("Nothing found")

    @staticmethod
    def get_combinations(initial, split_index):
        middle_index = None
        if (split_index % 3) != 0:
            middle_index = int(split_index / 3)

        combinations = [REPLACEMENT[initial[0]][0]] if middle_index == 0 else REPLACEMENT[initial[0]]

        index = 1
        for character in initial[1:]:
            initial_combinations = list(combinations)
            sub_combinations = []

            for combination in initial_combinations:
                sub_combinations.append(combination + REPLACEMENT[character][0])

            if index != middle_index:
                for replacement in REPLACEMENT[character][1:]:
                    for combination in initial_combinations:
                        sub_combinations.append(combination + replacement)
            combinations = sub_combinations

            index += 1

        return combinations

    @staticmethod
    def generate_lists(combinations, split_index, min_temp, max_temp):

        list1 = {}
        list2 = {}

        substitutions = {
            "a": "t",
            "t": "a",
            "g": "c",
            "c": "g",
        }

        for combination in combinations:
            comb1 = ""
            for character in combination[:split_index][::-1]:
                comb1 += substitutions[character]
            comb2 = combination[split_index:]

            if comb1 not in list1:
                codon1 = Codon(comb1)
                if min_temp is None or codon1.melting_temperature >= min_temp:
                    if max_temp is None or codon1.melting_temperature <= max_temp:
                        list1[codon1.string] = codon1
            if comb2 not in list2:
                codon2 = Codon(comb2)
                if min_temp is None or codon2.melting_temperature >= min_temp:
                    if max_temp is None or codon2.melting_temperature <= max_temp:
                        list2[codon2.string] = codon2

        return list(list1.values()), list(list2.values())

    @staticmethod
    def find_closest_values(list1, list2):
        closest = None
        closest1 = []
        closest2 = []

        for codon1 in list1:
            for codon2 in list2:
                diff = abs(codon1.melting_temperature - codon2.melting_temperature)

                if closest is None:
                    closest = diff

                if diff == closest:
                    closest1.append(codon1)
                    closest2.append(codon2)
                elif diff < closest:
                    closest = diff
                    closest1 = [codon1]
                    closest2 = [codon2]

        return closest, closest1, closest2


class Codon:
    string = ""
    _melting_temp = None

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return "%s (%s)" % (self.string, self.melting_temperature)

    def __repr__(self):
        return self.__str__()

    @property
    def melting_temperature(self):
        if self._melting_temp is not None:
            return self._melting_temp

        temp_h = 0
        temp_s = 0

        for i in range(len(self.string) - 1):
            substring = self.string[i] + self.string[i+1]
            temp_h += TEMPERATURES_H[substring.upper()]
            temp_s += TEMPERATURES_S[substring.upper()]

        melting_temp = round((temp_h + temp_s), 3)
        self._melting_temp = melting_temp

        return self._melting_temp


REPLACEMENT = {
    "A": ["gct", "gcc", "gca", "gcg"],
    "C": ["tgt", "tgc"],
    "D": ["gat", "gac"],
    "E": ["gaa", "gag"],
    "F": ["ttt", "ttc"],
    "G": ["ggt", "ggc", "gga", "ggg"],
    "H": ["cat", "cac"],
    "I": ["att", "atc", "ata"],
    "K": ["aaa", "aag"],
    "L": ["tta", "ttg"],
    "M": ["atg"],
    "N": ["aat", "aac"],
    "P": ["cct", "ccc", "cca", "ccg"],
    "Q": ["caa", "cag"],
    "R": ["cgt", "cgc", "cga", "cgg", "aga", "agg"],
    "S": ["tct", "tcc", "tca", "tcg", "agt", "agc"],
    "T": ["act", "acc", "aca", "acg"],
    "V": ["gtt", "gtc", "gta", "gtg"],
    "W": ["tgg"],
    "Y": ["tat", "tac"],
}

TEMPERATURES_H = {
    "AA": 2, "TT": 2,
    "AT": 2,
    "TA": 2,
    "CA": 3,
    "GT": 3,
    "CT": 3,
    "GA": 3,
    "CG": 4,
    "GC": 4,
    "GG": 4, "CC": 4,
    "TG": 3, "AC": 3,  # Random
    "TC": 3, "AG": 3,  # Random
}

TEMPERATURES_S = {
    "AA": 2, "TT": 2,
    "AT": 2,
    "TA": 2,
    "CA": 3,
    "GT": 3,
    "CT": 3,
    "GA": 3,
    "CG": 4,
    "GC": 4,
    "GG": 4, "CC": 4,
    "TG": 3, "AC": 3,  # Random
    "TC": 3, "AG": 3,  # Random
}
