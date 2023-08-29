import re
import pyconll
import pickle

def extract_errors(error_string):
    errors = re.findall(r'<(?![/])(?!C)(?!i)(?!i>)(?!c>|C)[a-zA-Z]+[^>]*>', error_string)
    return errors

def count_errors(data):
    error_counter = {1: {'es': 0, 'de': 0, 'en': 0, 'fr': 0},
                     2: {'es': 0, 'de': 0, 'en': 0, 'fr': 0},
                     3: {'es': 0, 'de': 0, 'en': 0, 'fr': 0}}
    
    token_counter = {1: {'es': 0, 'de': 0, 'en': 0, 'fr': 0},
                     2: {'es': 0, 'de': 0, 'en': 0, 'fr': 0},
                     3: {'es': 0, 'de': 0, 'en': 0, 'fr': 0}}  
    
    error_count_by_lev_nat = {1: {'es': 0, 'de': 0, 'en': 0, 'fr': 0},
                              2: {'es': 0, 'de': 0, 'en': 0, 'fr': 0},
                              3: {'es': 0, 'de': 0, 'en': 0, 'fr': 0}}

    for sentence in data:
        split_id = re.split('-|_', sentence.id)
        nat = split_id[2]
        lev = int(split_id[3])
        
        if (nat, lev) not in token_counter:
            token_counter[lev][nat] = 0
        
        for token in sentence:
            token_counter[lev][nat] += 1
        
        error_string = sentence.meta_value('err')
        errors = extract_errors(error_string)
        for error in errors:
            error_count_by_lev_nat[lev][nat] += 1
            error_counter[lev][nat] += 1  


    return error_counter, token_counter, error_count_by_lev_nat


def main():
    file_path = 'UD_Valico.conllu'
    data = pyconll.load_from_file(file_path)
    level_nationality_letter_errors = {1: {'es': {}, 'de': {}, 'en': {}, 'fr': {}},
                                       2: {'es': {}, 'de': {}, 'en': {}, 'fr': {}},
                                       3: {'es': {}, 'de': {}, 'en': {}, 'fr': {}}}
    
    error_counter, token_counter, error_count_by_lev_nat = count_errors(data)
    
    for sentence in data:
        split_id = re.split('-|_', sentence.id)
        nat = split_id[2]
        lev = int(split_id[3])

        
        for error in extract_errors(sentence.meta_value('err')):
            first_letter = error[2]  
            if first_letter in level_nationality_letter_errors[lev][nat]:
                if error in level_nationality_letter_errors[lev][nat][first_letter]:
                    level_nationality_letter_errors[lev][nat][first_letter][error] += 1 
                else:
                    level_nationality_letter_errors[lev][nat][first_letter][error] = 1 
            else:
                level_nationality_letter_errors[lev][nat][first_letter] = {error: 1}

                
    
    
    aggregate_relative_frequencies = {
        1: {'es': {}, 'de': {}, 'en': {}, 'fr': {}},
        2: {'es': {}, 'de': {}, 'en': {}, 'fr': {}},
        3: {'es': {}, 'de': {}, 'en': {}, 'fr': {}}
    }

    
    for lev, nationality_data in level_nationality_letter_errors.items():
        print(f'Level {lev}:')
        print ('________________________________________________________________________________')
        for nat, letter_data in nationality_data.items():
            print ('____________________')
            print(f'  Nationality {nat}:')
            print ('____________________')
            for letter, error_types in letter_data.items():
                print(f'    Starting letter: {letter}')
                for error, freq in error_types.items():
                    rel_freq = freq / error_counter[lev][nat]
                    level_nationality_letter_errors[lev][nat][letter][error] = rel_freq
                    print(f'      {error}: {rel_freq:.6f}')
                aggregate_freq = sum(
                    level_nationality_letter_errors[lev][nat][letter].get(error, 0)
                    for letter in letter_data.keys()
                    for error in error_types.keys()
                )
                aggregate_relative_frequencies[lev][nat][letter] = aggregate_freq
                print(f'    Aggregate Relative Frequency: {aggregate_freq:.6f}')

    all_data = {
        'level_nationality_letter_errors': level_nationality_letter_errors,
        'error_counter': error_counter,
        'error_count_by_lev_nat': error_count_by_lev_nat,
        'aggregate_relative_frequencies': aggregate_relative_frequencies
    }

  
    with open('error_data.pickle', 'wb') as f:
        pickle.dump(all_data, f)
if __name__ == "__main__":
    main()
