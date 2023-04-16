import argparse
import sys
import tempfile

import frequency_analysis
import russian_language_data


def get_shifted_letter(
        letter: str, shift: int, *,
        mapping: dict, alphabet: str, upper_alphabet: str,
        upper_lower_mapping: dict) -> str:
    if letter == '\xa0':
        return ' '
    # Assign lowered_letter = letter if letter is not in mapping
    lowered_letter = upper_lower_mapping.get(letter, letter)
    letter_index = mapping.get(lowered_letter)
    if letter_index is None:
        return letter
    new_letter_index = (letter_index + shift) % len(alphabet)
    if letter in upper_lower_mapping:
        return upper_alphabet[new_letter_index]
    return alphabet[new_letter_index]


def caesar_cipher(input_file_name: str, output_file_name: str, *,
                  shift: int, mode: int, encoding="utf8") -> None:
    # mode = 1 -> cipher
    # mode = -1 -> decipher
    if mode == -1:
        shift = -shift
    with open(output_file_name, "w") as f_out:
        with open(input_file_name, "r", encoding=encoding) as f_in:
            for line in f_in:
                for character in line:
                    character = \
                        get_shifted_letter(character,
                                           shift,
                                           mapping=russian_language_data.RUSSIAN_ALPHABET_MAPPING,
                                           alphabet=russian_language_data.RUSSIAN_ALPHABET,
                                           upper_alphabet=russian_language_data.RUSSIAN_UPPER_ALPHABET,
                                           upper_lower_mapping=russian_language_data.RUSSIAN_ALPHABET_UPPER_TO_LOWER_MAPPING
                                           )
                    f_out.write(character)


def get_delta(
        distribution: dict,
        usual_distribution=russian_language_data.RUSSIAN_LETTERS_OCCURRENCE
) -> float:
    delta = 0
    usual_occurrence = sorted(usual_distribution.items(), key=lambda x: x[0])
    current_occurrence = sorted(distribution.items(), key=lambda x: x[0])
    for i in range(len(usual_occurrence)):
        delta += (usual_occurrence[i][1] - current_occurrence[i][1]) ** 2
    return delta


def get_shift(input_file_name: str, encoding="utf-8"):
    deltas_for_each_shift = []
    for i in range(russian_language_data.RUSSIAN_LETTERS_NUMBER):
        temporary_file = tempfile.NamedTemporaryFile()
        caesar_cipher(input_file_name, temporary_file.name, shift=i, mode=1)
        occurrence = frequency_analysis.get_bigrams(temporary_file.name,
                                                    encoding,
                                                    russian_language_data.RUSSIAN_ALPHABET_SET)
        deltas_for_each_shift.append(get_delta(occurrence))
    min_delta = min(deltas_for_each_shift)
    return deltas_for_each_shift.index(min_delta)

def decipher(input_file_name: str,
             output_file_name: str, *,
             encoding="utf8") -> None:
    shift = get_shift(input_file_name, encoding)
    caesar_cipher(input_file_name, output_file_name, shift=shift, mode=1)


def letter_shifted_with_vigener(
        letter: str, key: str, mode: int, *,
        mapping: dict, alphabet: str, upper_alphabet: str,
        upper_lower_mapping: dict) -> str:
    # mode = -1 -> decipher
    # mode = 1 -> cipher
    lowered_letter = upper_lower_mapping.get(letter, letter)
    letter_index = mapping.get(lowered_letter)
    key_letter_index = mapping.get(key)
    new_letter_index = \
        (letter_index + mode * key_letter_index) % len(alphabet)
    if letter in upper_lower_mapping:
        return upper_alphabet[new_letter_index]
    return alphabet[new_letter_index]


def vigener_cipher(input_file_name: str, output_file_name: str, *,
                   key: str, mode: int, encoding="utf-8"):
    # mode = 1 -> cipher
    # mode = -1 -> decipher
    key = key.lower()
    with open(input_file_name, "r", encoding=encoding) as f_in:
        text = f_in.read()
    key_character = 0
    with open(output_file_name, "w") as f_out:
        for character in text:
            if character == '\xa0':
                f_out.write(' ')
                continue
            if not character.isalpha():
                f_out.write(character)
                continue
            if character.isalpha() and \
                    character.lower() not in russian_language_data.RUSSIAN_ALPHABET_SET:
                f_out.write(character)
                continue
            f_out.write(letter_shifted_with_vigener(character,
                                                    key[key_character],
                                                    mode,
                                                    mapping=russian_language_data.RUSSIAN_ALPHABET_MAPPING,
                                                    alphabet=russian_language_data.RUSSIAN_ALPHABET,
                                                    upper_alphabet=russian_language_data.RUSSIAN_UPPER_ALPHABET,
                                                    upper_lower_mapping=russian_language_data.RUSSIAN_ALPHABET_UPPER_TO_LOWER_MAPPING))
            key_character += 1
            key_character %= len(key)

def main():
    parser = argparse.ArgumentParser(prog="Cipher")
    parser.add_argument("input_file_name")
    parser.add_argument("output_file_name")
    parser.add_argument("-e", "--encoding",
                        action="store",
                        dest="encoding",
                        required=False,
                        default="utf-8",
                        help="")
    parser.add_argument("-m", "--mode",
                        action="store",
                        choices=["encrypt", "decrypt", "hack"],
                        dest="mode",
                        required=True,
                        help="")
    parser.add_argument("-c", "--cipher",
                        action="store",
                        choices=["caesar", "vigener", "vernam"],
                        type=str,
                        dest="cipher_type",
                        required=False,
                        help="")
    parser.add_argument("-k", "--key",
                        action="store",
                        dest="key",
                        type=str,
                        required=False,
                        help="")

    cmd_args = parser.parse_args(sys.argv[1:])
    if cmd_args.mode == "hack":
        decipher(cmd_args.input_file_name,
                 cmd_args.output_file_name,
                 encoding=cmd_args.encoding)
        return
    mode = 1
    if cmd_args.mode == "decrypt":
        mode = -1
    if cmd_args.cipher_type == "caesar":
        # TODO try except
        cmd_args.key = int(cmd_args.key)
        caesar_cipher(cmd_args.input_file_name,
                      cmd_args.output_file_name,
                      shift=cmd_args.key,
                      encoding=cmd_args.encoding,
                      mode=mode)
    if cmd_args.cipher_type == "vigener":
        vigener_cipher(cmd_args.input_file_name,
                       cmd_args.output_file_name,
                       key=cmd_args.key,
                       encoding=cmd_args.encoding,
                       mode=mode)

if __name__ == "__main__":
    main()

