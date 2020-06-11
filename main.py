from enum import Enum

class LexemsEnum(Enum):
    """
    The list of all lexems
    """
    km_word = 'km'
    kmm_word = 'kmm'
    kmmm_word = 'kmmm'
    dot_symbol = '.'
    equality_symbol = '='
    plus_symbol = '+'
    minus_symbol = '-'
    d_d = ('0', '1', '10')
    d_o = ('2', '3')


class Lexer:
    output_file = 'output_data.txt'
    input_file = 'input_data.txt'

    def __init__(self):
        self.current_line = 0
        self.input_lines = []
        self.head_position = 0

    def read_input(self):
        with open(self.input_file) as file:
            self.input_lines = file.readlines()
        
    def clean_output_file(self):
        with open(self.output_file, 'w') as file:
            print('The file was cleaned\n')

    def write_lexem_to_file(self, lexem_type, lexem):
        display_message = f'<{lexem_type} \'{lexem}\'>\n'
        with open(self.output_file, 'a') as file:
            file.write(display_message)
        print(display_message)

    def write_error_to_file(self, error_type, position):
        """
        If there was error move to the next line
        """
        error_message = f'<error in sentence {self.current_line} in position {position}, {error_type}>\n'
        with open(self.output_file, 'a') as file:
            file.write(error_message)
        print(error_message)
        self.current_line += 1
        self.head_position = 0

    def get_symbol(self):
        """
        :return: the current symbol
        """
        if self.current_line >= len(self.input_lines):
              # if we reach the end of the file
            return ''

        line = self.input_lines[self.current_line]

        if self.head_position > len(line) - 1:
            # if we have reach the end of the line
            self.head_position = 0
            self.current_line += 1
            return self.get_symbol()
        else:
            current_symbol = line[self.head_position]
            self.head_position += 1
            return current_symbol

    def return_head(self):
        """
        returns head to the previous position
        """
        self.head_position -= 1

    def get_token(self):
        """
        main method that processes the token
        """
        current_symbol = self.get_symbol()

        if current_symbol == '':
            print('We have reached the end of the program!')
            return
        elif current_symbol == '\n':  # in case we reach end of the line
            self.head_position += 1
            self.get_token()
        elif current_symbol == ' ':  # skipping spaces
            self.get_token()
        elif current_symbol == 'k':
            self.process_word('k')
        elif current_symbol == LexemsEnum.dot_symbol.value:
            self.write_lexem_to_file(LexemsEnum.dot_symbol.name, LexemsEnum.dot_symbol.value)
            self.get_token()
        elif current_symbol == LexemsEnum.equality_symbol.value:
            self.write_lexem_to_file(LexemsEnum.equality_symbol.name, LexemsEnum.equality_symbol.value)
            self.get_token()
        elif current_symbol == LexemsEnum.plus_symbol.value:
            self.write_lexem_to_file(LexemsEnum.plus_symbol.name, LexemsEnum.plus_symbol.value)
            self.get_token()
        elif current_symbol == LexemsEnum.minus_symbol.value:
            self.write_lexem_to_file(LexemsEnum.minus_symbol.name, LexemsEnum.minus_symbol.value)
            self.get_token()
        elif current_symbol in LexemsEnum.d_d.value:
            self.process_dd(current_symbol)
        elif current_symbol in LexemsEnum.d_o.value:
            self.process_do(current_symbol)
        else:
            self.write_error_to_file(f'unknown symbol {current_symbol}', self.head_position)
            self.get_token()

    def process_word(self, letter):
        next_symbol = self.get_symbol()
        current_word = f'{letter}'

        m_counter = 1
        while next_symbol == 'm' and m_counter < 4:  # while next symbol is m (and there are not too much ms)
            m_counter += 1
            next_symbol = self.get_symbol()
            current_word = f'{current_word}m'

        self.return_head()
        was_found = False
        for lexem in LexemsEnum:
            if lexem.value == current_word:
                was_found = True
                self.write_lexem_to_file(lexem.name, lexem.value)
                self.get_token()
        
        if not was_found:
            self.write_error_to_file(f"incorrect word {current_word}", self.head_position+1)
            self.get_token()

    def process_dd(self, number):
        if number == '0':
            self.write_lexem_to_file(LexemsEnum.d_d.name, '0')
            self.get_token()
            return

        next_symbol = self.get_symbol()
        if next_symbol == '0':
            self.write_lexem_to_file(LexemsEnum.d_d.name, '10')
            self.get_token()
            return

        self.return_head()
        self.write_lexem_to_file(LexemsEnum.d_d.name, '1')
        self.get_token()

    def process_do(self, letter):
        next_symbol = self.get_symbol()
        current_iden = f'{letter}'

        while next_symbol in LexemsEnum.d_o.value:
            current_iden = f'{current_iden}{next_symbol}'
            next_symbol = self.get_symbol()
        
        self.return_head()
        self.write_lexem_to_file(LexemsEnum.d_o.name, current_iden)
        self.get_token()


if __name__ == '__main__':
    l = Lexer()
    l.clean_output_file()
    l.read_input()
    l.get_token()
