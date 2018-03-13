####################################################################################################
#
# Babel - An Electronic Document Management System
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import logging

####################################################################################################

import ply.lex as lex
import ply.yacc as yacc
from ply.lex import TOKEN

####################################################################################################

from .Entry import Entry

####################################################################################################

class Parser:

    _logger = logging.getLogger(__name__)

    ##############################################

    tokens = (
        'Comment',
        'Preamble',
        'StringDefinition',
        'Entry',
        'EndOfBlock',
        'Identifier',
        'String',
        'Number',
        'COMMA',
        'EQUAL',
        'SHARP',
        )

    # Declare the lexer states
    states = (
        ('CommentBrace', 'exclusive'),
        ('CommentParenthesis', 'exclusive'),
        ('PreambleBrace', 'exclusive'),
        ('PreambleParenthesis', 'exclusive'),
        ('BlockBrace', 'exclusive'),
        ('BlockParenthesis', 'exclusive'),
        ('StringQuote', 'exclusive'),
        ('StringBrace', 'exclusive'),
        )

    ##############################################

    def t_ANY_error(self, token):
        self._logger.error("Illegal character '%s' at line %u and position %u" %
                           (token.value[0],
                            token.lexer.lineno,
                            token.lexer.lexpos - self._previous_newline_position))
        token.lexer.skip(1)

    ##############################################

    t_ignore  = ' \t'

    def t_ANY_newline(self, token):
        r'\n+'
        # Track newline
        token.lexer.lineno += len(token.value)
        self._previous_newline_position = token.lexer.lexpos

    ##############################################

    def _begin_block(self, token, state):
        self._logger.debug('')
        token.lexer.code_start = token.lexer.lexpos
        token.lexer.level = 1 # Initial brace level
        token.lexer.push_state(state)

    def _increment_block_level(self, token):
        self._logger.debug('')
        token.lexer.level +=1

    def _decrement_block_level(self, token, token_type):
        self._logger.debug('')
        token.lexer.level -=1
        if token.lexer.level == 0:
            token.type = token_type
            token.value = token.lexer.lexdata[token.lexer.code_start:token.lexer.lexpos-1]
            token.lexer.pop_state()
            return token

    ##############################################
    #
    # Comment
    #

    comment_regexp = r'(?i)@comment'

    @TOKEN(comment_regexp + r'\{')
    def t_comment_begin_brace(self, token):
        self._logger.debug('')
        self._begin_block(token, 'CommentBrace')

    @TOKEN(comment_regexp + r'\(')
    def t_comment_begin_parenthesis(self, token):
        self._logger.debug('')
        self._begin_block(token, 'CommentParenthesis')

    def t_CommentBrace_lbrace(self, token):
        r'\{'
        self._logger.debug('')
        self._increment_block_level(token)

    def t_CommentParenthesis_lparenthesis(self, token):
        r'\('
        self._logger.debug('')
        self._increment_block_level(token)

    def t_CommentBrace_rbrace(self, token):
        r'\}'
        self._logger.debug('')
        return self._decrement_block_level(token, 'Comment')

    def t_CommentParenthesis_rparenthesis(self, token):
        r'\)'
        self._logger.debug('')
        return self._decrement_block_level(token, 'Comment')

    t_CommentBrace_CommentParenthesis_ignore = ''

    def t_CommentBrace_CommentParenthesis_content(self, token):
        r'.'
        #self._logger.debug('')
        pass

    ##############################################
    #
    # Preamble
    #

    preamble_regexp = r'(?i)@preamble'

    @TOKEN(preamble_regexp + r'\{')
    def t_preamble_begin_brace(self, token):
        self._logger.debug('')
        self._begin_block(token, 'PreambleBrace')

    @TOKEN(preamble_regexp + r'\(')
    def t_preamble_begin_parenthesis(self, token):
        self._logger.debug('')
        self._begin_block(token, 'PreambleParenthesis')

    def t_PreambleBrace_lbrace(self, token):
        r'\{'
        self._logger.debug('')
        self._increment_block_level(token)

    def t_PreambleParenthesis_lparenthesis(self, token):
        r'\('
        self._logger.debug('')
        self._increment_block_level(token)

    def t_PreambleBrace_rbrace(self, token):
        r'\}'
        self._logger.debug('')
        return self._decrement_block_level(token, 'Preamble')

    def t_PreambleParenthesis_rparenthesis(self, token):
        r'\)'
        self._logger.debug('')
        return self._decrement_block_level(token, 'Preamble')

    t_PreambleBrace_PreambleParenthesis_ignore = ''

    def t_PreambleBrace_PreambleParenthesis_content(self, token):
        r'.'
        #self._logger.debug('')
        pass

    ##############################################
    #
    # Block
    #

    def _begin_identified_block(self, token, state):
        self._logger.debug('')
        token.value = token.value[1:-1]
        if token.value.lower() == 'string':
            token.type = 'StringDefinition'
        else:
            token.type = 'Entry'
        token.lexer.push_state(state)

    def _end_identified_block(self, token):
        self._logger.debug('')
        token.type = 'EndOfBlock'
        token.lexer.pop_state()

    spaces = r' \t'
    delimiters = r'\{\}\(\)"'
    special_characters = r',=@\#'
    numbers = r'0-9'
    excluded_identifier_characters = spaces + delimiters + special_characters
    entry_type_regexp = r'@[^' + excluded_identifier_characters + r']+'

    @TOKEN(entry_type_regexp + r'\{')
    def t_block_begin_brace(self, token):
        self._logger.debug('')
        self._begin_identified_block(token, 'BlockBrace')
        return token

    @TOKEN(entry_type_regexp + r'\(')
    def t_block_begin_parenthesis(self, token):
        self._logger.debug('')
        self._begin_identified_block(token, 'BlockParenthesis')
        return token

    def t_BlockBrace_rbrace(self, token):
        r'\}'
        self._logger.debug('')
        self._end_identified_block(token)
        return token

    def t_BlockParenthesis_rparenthesis(self, token):
        r'\)'
        self._logger.debug('')
        self._end_identified_block(token)
        return token

    ##############################################

    t_BlockBrace_BlockParenthesis_ignore = ' \t'
    t_BlockBrace_BlockParenthesis_SHARP = r'\#'
    t_BlockBrace_BlockParenthesis_EQUAL = r'='
    t_BlockBrace_BlockParenthesis_COMMA = r','
    t_BlockBrace_BlockParenthesis_Identifier = \
        r'[^' + excluded_identifier_characters + numbers + ']'+ \
        r'[^' + excluded_identifier_characters + r']*'
    t_BlockBrace_BlockParenthesis_Number = r'\d+'

    ##############################################
    #
    # String
    #

    def t_BlockBrace_BlockParenthesis_begin_quoted_string(self, token):
        r'"'
        self._logger.debug('')
        self._begin_block(token, 'StringQuote')

    def t_BlockBrace_BlockParenthesis_begin_braced_string(self, token):
        r'{'
        self._logger.debug('')
        self._begin_block(token, 'StringBrace')

    def t_StringBrace_lbrace(self, token):
        r'\{'
        self._logger.debug('')
        self._increment_block_level(token)

    def t_StringQuote_end(self, token):
        r'"'
        self._logger.debug('')
        return self._decrement_block_level(token, 'String')

    def t_StringBrace_rbrace(self, token):
        r'\}'
        self._logger.debug('')
        return self._decrement_block_level(token, 'String')

    t_StringBrace_StringQuote_ignore = ''

    def t_StringQuote_StringBrace_content(self, token):
        r'.'
        #self._logger.debug('')
        pass

    ##############################################
    #
    # Outer Contents
    #

    def t_text(self, token):
        r'[^@]'
        #self._logger.debug('')
        pass

    ##############################################
    #
    # Grammar
    #

    def p_statements(self, p):
        ''' statements : statements statement
                       | statement '''
        self._logger.debug('')

    def p_statement(self, p):
        ''' statement : Preamble
                      | Comment
                      | string_definition
                      | entry_definition '''
        self._logger.debug('')

    def p_string_definition(self, p):
        'string_definition : StringDefinition Identifier EQUAL string_expression EndOfBlock'
        self._logger.debug('Define string %s = "%s"' % (p[2], p[4]))
        self._string_definitions[p[2]] = p[4]

    def p_entry_definition(self, p):
        'entry_definition : Entry Identifier COMMA key_value_pair_sequence EndOfBlock'
        entry_type, identifier, pairs = p[1], p[2], p[4]
        entry = Entry(entry_type, identifier, pairs)
        self._entries.append(entry)
        self._logger.debug('Entry\n' + str(entry))

    def p_key_value_pair_sequence(self, p):
        ''' key_value_pair_sequence : key_value_pair COMMA key_value_pair_sequence
                                    | key_value_pair COMMA
                                    | key_value_pair '''
        self._logger.debug('')
        if len(p) == 4:
            pairs, pair = p[3], p[1]
            pairs.append(pair)
            p[0] = pairs
        else:
            pair = p[1]
            p[0] = [pair]

    def p_key_value_pair(self, p):
        ' key_value_pair : Identifier EQUAL value '
        pair = (p[1], p[3])
        self._logger.debug('Pair ' + str(pair))
        p[0] = pair

    def p_value(self, p):
        ''' value : string_expression
                  | Number '''
        self._logger.debug('')
        p[0] = p[1]

    def p_string_concatenation_left(self, p):
        ''' string_concatenation_left : Identifier SHARP string_expression '''
        self._logger.debug('')
        p[0] = self._string_definitions[p[1]] + p[3]

    def p_string_concatenation_right(self, p):
        ''' string_concatenation_right : string_expression SHARP Identifier '''
        self._logger.debug('')
        p[0] = p[1] + self._string_definitions[p[3]]

    def p_string_expression(self, p):
        ''' string_expression : String
                              | string_concatenation_left
                              | string_concatenation_right '''
        self._logger.debug('')
        p[0] = p[1]

    ##############################################

    def __init__(self):

        self._build()

    ##############################################

    def _build(self, **kwargs):

        self._lexer = lex.lex(module=self, **kwargs)
        self._parser = yacc.yacc(module=self, **kwargs)

    ##############################################

    def _reset(self):

        self._previous_newline_position = 0
        self._string_definitions = {}
        self._entries = []

    ##############################################

    def parse(self, text):

        self._reset()
        self._parser.parse(text, lexer=self._lexer)

        return self._entries

    ##############################################

    def test_lexer(self, text):

        self._reset()
        self._lexer.input(text)
        while True:
            token = self._lexer.token()
            if not token:
                break
            print(token)
