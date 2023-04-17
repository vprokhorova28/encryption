def get_bigrams(input_file_name, encoding, alphabet_set):
    occurrence = {}
    num_all_letters = 0
    with open(input_file_name, "r", encoding=encoding) as f_in:
        for line in f_in:
            for character in line.lower():
                if character not in alphabet_set:
                    continue
                num_all_letters += 1
                if character not in occurrence:
                    occurrence[character] = 0
                occurrence[character] += 1
    for letter in occurrence:
        if letter == 'ё':
            occurrence['е'] += (occurrence['ё'] / num_all_letters) * 100
            occurrence['ё'] = 0
        occurrence[letter] = (occurrence[letter] / num_all_letters) * 100
    return occurrence