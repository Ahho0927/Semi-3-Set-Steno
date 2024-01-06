from hgtk.letter import compose, decompose, NotHangulException
from hgtk.checker import is_hangul, has_batchim
from pynput.keyboard import Key
from keyboard import write
from data.key import Keys
from json import load
from re import sub
from data.VKCODE import VK_SPACE

keys = Keys()
class Translation:
    def __init__(self) -> None:
        self.KEY_TO_CONSONANT: dict[str] = dict(zip('qwertasdfgzxcv', 'ㅂㅈㄷㄱㅅㅁㄴㅇㄹㅎㅋㅌㅊㅍ'))
        self.KEY_TO_VOWEL: dict[str] = dict(zip('yuiophjklnm', 'ㅛㅕㅑㅐㅔㅗㅓㅏㅣㅜㅡ'))
        self.KEY_TO_SPECIAL_KEY: dict[str] = dict(zip("[b;',./1234567890", 'ㄲㅆ凵冂,.丅1234567890'))
        self.KEY_TO_SPECIAL_KEY.update({'space': '空'})

        self.HANGUL_TO_KEY: dict[str] = {'ㄱ': 'r', 'ㄲ': 'R', 'ㄳ': 'rt', 'ㄴ': 's', 'ㄵ': 'sw', 'ㄶ': 'sg', 'ㄷ': 'e', 'ㄸ': 'E', 
                                         'ㄹ': 'f', 'ㄺ': 'fr', 'ㄻ': 'fa', 'ㄼ': 'fq', 'ㄽ': 'ft', 'ㄾ': 'fx', 'ㄿ': 'fv', 'ㅀ': 'fg', 
                                         'ㅁ': 'a', 'ㅂ': 'q', 'ㅃ': 'Q', 'ㅄ': 'qt', 'ㅅ': 't', 'ㅆ': 'T', 'ㅇ': 'd', 
                                         'ㅈ': 'w', 'ㅉ': 'W', 'ㅊ': 'c', 'ㅋ': 'z', 'ㅌ': 'x', 'ㅍ': 'v', 'ㅎ': 'g', 
                                         'ㅏ': 'k', 'ㅐ': 'o', 'ㅑ': 'i', 'ㅒ': 'O', 'ㅓ': 'j', 'ㅔ': 'p', 'ㅕ': 'u', 'ㅖ': 'P', 
                                         'ㅗ': 'h', 'ㅘ': 'hk', 'ㅙ': 'ho', 'ㅚ': 'hl', 'ㅛ': 'y', 'ㅜ': 'n', 'ㅝ': 'nj', 'ㅞ': 'np', 'ㅟ': 'nl', 'ㅠ': 'b', 
                                         'ㅡ': 'm', 'ㅢ': 'ml', 'ㅣ': 'l'}
        
        with open("./data/macros.json", "rt", encoding="UTF8") as file:
            self.MACRO_DATA: dict[str] = load(file)['macro_data']

        self.previous: str = ''
        self.backspace_pressed_count = 0

    def reset_previous(self) -> None:
        self.previous = '으'
        if self.allomorphic:
            self.previous = '을'
        if self.result_end_with_space:
            self.previous += ' '

        self.allomorphic = False
        self.result_end_with_space = False

    def key_to_string_indicator(self, keys):
        consonants, vowels, special_keys = '', '', ''
        for key in keys:
            consonants += self.KEY_TO_CONSONANT.get(key, '')
            vowels += self.KEY_TO_VOWEL.get(key, '')
            special_keys += self.KEY_TO_SPECIAL_KEY.get(key, '')

        result = ''.join(sorted(consonants) + ['/'] + sorted(vowels) + ['/'] + sorted(special_keys))
        print(result)
        return result
    
    def indicator_to_result(self, indicator):
        indicator_list = indicator.split('/')
        consonants, vowels, special_keys = indicator_list[0], indicator_list[1], indicator_list[2]

        result = ''
        self.backspace_pressed_count = 0
        self.result_end_with_space = False
        try:
            result = self.MACRO_DATA[indicator]
            if result[-1] == ' ':
                self.result_end_with_space = True

            stick, combine, self.allomorphic = False, False, False
            if '⇤' in result:
                stick = True
                result = result[1:]
            if '-' in result:
                combine = True
                result = result[1:]
            if '|' in result:
                self.allomorphic = True
                result_list = result.split('|')

            if stick:
                previous_space_count = 0
                for i, letter in enumerate(self.previous[::-1]):
                    if letter != ' ':
                        previous_space_count = i
                        break
                
                self.backspace_pressed_count += previous_space_count
                if previous_space_count:
                    self.previous = self.previous[:-previous_space_count]

            if self.allomorphic:
                result = result_list[1]
                if has_batchim(self.previous[-1]):
                    result = result_list[0]

            if combine:
                d_cho, d_jung, d_jong = decompose(self.previous[::-1][previous_space_count])
                result = compose(d_cho, d_jung, result[0]) + result[1:]
                write('-')
                self.backspace_pressed_count += 2
                self.previous = self.previous[:-1]
                
        except Exception:
            cho, jung, jong = '', '', ''
            if consonants and len(consonants) <= 2:
                cho = consonants[0]
                if '凵' in special_keys:
                    jong = cho
                    if len(consonants) == 2:
                        cho = consonants[1]
                elif len(consonants) == 2:
                    jong = consonants[1]

            if '冂' in special_keys:
                cho = {'ㄱ': 'ㄲ', 'ㄷ': 'ㄸ', 'ㅂ': 'ㅃ', 'ㅅ': 'ㅆ', 'ㅈ': 'ㅉ'}.get(cho, cho)
            if 'ㅆ' in special_keys:
                jong = {'ㄱ': 'ㄺ', 'ㅁ': 'ㄻ', 'ㅂ': 'ㅄ', 'ㅅ': 'ㄽ', 
                        'ㅌ': 'ㄾ', 'ㅍ': 'ㄿ', 'ㅎ': 'ㅀ', '': 'ㅆ'}.get(jong, jong)
            if 'ㄲ' in special_keys:
                jong = {'ㅅ': 'ㄳ', 'ㅈ': 'ㄵ', 
                        'ㅎ': 'ㄶ', 'ㅂ': 'ㄼ', '': 'ㄲ'}.get(jong, jong)

            jung = {'ㅏㅗ': 'ㅘ', 'ㅐㅗ': 'ㅙ', 'ㅐㅡ': 'ㅒ', 
                    'ㅓㅜ': 'ㅝ', 'ㅔㅜ': 'ㅞ', 'ㅔㅡ': 'ㅖ', 
                    'ㅗㅣ': 'ㅚ', 'ㅜㅡ': 'ㅠ', 'ㅜㅣ': 'ㅟ', 'ㅡㅣ': 'ㅢ'}.get(vowels, vowels)
            
            try:
                result = compose(cho, jung, jong)
            except NotHangulException:
                pass # result = ''

            if '.' in special_keys:
                result += '. '
            if ',' in special_keys:
                result += ', '
            if '丅' in special_keys:
                result += '? '
            if '空' in special_keys:
                result += ' '
        
        print(result)
        return result

    
    def transform_to_keys(self, string: str):
        result: str = ''
        for letter in string:
            if is_hangul(letter):
                for character in decompose(letter):
                    result += self.HANGUL_TO_KEY.get(character, '')
            else: result += letter
        
        return result