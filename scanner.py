# Class of token types 
class TokenType:
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    ID = "ID"
    STRING = "STRING"
    NUMBER = "NUMBER"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"
    ERROR = "ERROR"

""" DFA transition table: 
    Dictionary that maps 
    (current state, character type) -> (next state, action)
 """
transitionTable = {
    ('letter', 'start'): ('ID', 'continue'),
    ('digit', 'start'): ('NUMBER', 'continue'),
    ('whitespace', 'start'): ('WHITESPACE', 'continue'),
    ('"', 'start'): ('STRING', 'continue'),
    ('+', 'start'): ('SYMBOL', 'accept'),
    ('-', 'start'): ('SYMBOL', 'accept'),
    ('*', 'start'): ('SYMBOL', 'continue'),
    ('/', 'start'): ('SYMBOL', 'continue'),
    ('<', 'start'): ('SYMBOL', 'continue'),
    ('>', 'start'): ('SYMBOL', 'continue'),
    ('=', 'start'): ('SYMBOL', 'continue'),
    (';', 'start'): ('SYMBOL', 'accept'),
    (',', 'start'): ('SYMBOL', 'accept'),
    ('.', 'start'): ('SYMBOL', 'accept'),
    ('(', 'start'): ('SYMBOL', 'accept'),
    (')', 'start'): ('SYMBOL', 'accept'),
    ('[', 'start'): ('SYMBOL', 'accept'),
    (']', 'start'): ('SYMBOL', 'accept'),
    ('{', 'start'): ('SYMBOL', 'accept'),
    ('}', 'start'): ('SYMBOL', 'accept'),

    ('letter', 'ID'): ('ID', 'continue'),
    ('digit', 'ID'): ('ID', 'continue'),
    ('letter', 'STRING'): ('STRING', 'continue'),
    ('string', 'STRING'): ('STRING', 'continue'),


    ('digit', 'NUMBER'): ('NUMBER', 'continue'),
    ('.', 'NUMBER'): ('NUMBER', 'continue'),

    ('whitespace', 'WHITESPACE'): ('WHITESPACE', 'continue'),

    ('*', 'SYMBOL'): ('COMMENT', 'continue'),
    ('/', 'SYMBOL'): ('COMMENT', 'accept'),

    ('"', 'STRING'): ('start', 'continue'),

    ('=', '<'): ('SYMBOL', 'accept'),
    ('=', '>'): ('SYMBOL', 'accept'),
    ('=', '='): ('SYMBOL', 'accept'),
    ('!', 'start'): ('SYMBOL', 'continue'),
    ('=', 'SYMBOL'): ('SYMBOL', 'accept'),

    ('*', 'COMMENT'): ('COMMENT', 'continue'),
    ('/', 'COMMENT'): ('COMMENT', 'accept'),

    ('letter', 'STRING'): ('STRING', 'continue'),
    ('digit', 'STRING'): ('STRING', 'continue'),
    (',', 'STRING'): ('STRING', 'continue'),
    (' ', 'STRING'): ('STRING', 'continue'),
    ('"', 'STRING'): ('STRING', 'accept'),
}

# Keywords of the language
keywords = [
    "int", "float", "string", "for", "if", "else", "while", "return",
    "read", "write", "void"
]

""" States table: 
    Dictionary that maps 
    (Token class) -> (key of token class, dictionary of different tokens)
 """
statesTableDict = {
    "KEYWORD" : (1,
        {
            "int" : 1, 
            "float" : 2, 
            "string" : 3, 
            "for" : 4, 
            "if" : 5, 
            "else" : 6, 
            "while" : 7, 
            "return" : 8,
            "read" : 9, 
            "write" : 10,
            "void" : 11
        }
    ),
    "SYMBOL" : (2, {}),
    "ID" : (3, {}),
    "STRING" : (4, {}),
    "NUMBER" : (5, {})
}

""" Character class function: Determines what type of token the character is
    param c: A character
    param state:The current state
    Returns tokens: A type of token
 """
def charType(c, state):
    if state == 'STRING' and c != '"':
        return 'string'
    elif c.isalpha():
        return 'letter'
    elif c.isdigit():
        return 'digit'
    elif c.isspace():
        return 'whitespace'
    else:
        return c

""" Scanner function: Process the input and returns the tokens found
    param inputString: A string with the characters that wants to be process
    Returns tokens: A list of tokens found
 """
def scanner(inputString):
    tokens = []
    state = 'start'
    currentToken = ""
    tokenType = ""
    comment = False

    for i, c in enumerate(inputString):
        if c == "/" and i + 1 < len(inputString) and inputString[i + 1] == "*":
            comment = True
        if comment and  c == "/" and inputString[i -1] == "*":
            comment = False
            continue
        if comment:
            continue

        ctype = charType(c, state)
        action = transitionTable.get((ctype, state))

        if action is None:
            action = ('ERROR', 'accept')

        nextState, mode = action

        if mode == 'continue':
            if state != 'STRING' or (state == 'STRING' and c != '"'):
                currentToken += c
            state = nextState
        elif mode == 'accept':
            if state not in [TokenType.WHITESPACE, TokenType.COMMENT]:
                if state == 'ID' and currentToken.lower() in keywords:
                    tokenType = TokenType.KEYWORD
                else:
                    tokenType = state
                if tokenType != "start":
                    if ctype == "\"":
                        currentToken += "\""
                    elif ctype == "=":
                        currentToken += "="
                    tokens.append((tokenType, currentToken))
                    currentToken = ""
                    state = 'start'
                    if ctype == "\"" or ctype == "=":
                        continue

            currentToken = ""
            state = 'start'

            if ctype != 'whitespace':
                action = transitionTable.get((ctype, state))
                if action is not None:
                    nextState, nextMode = action
                    if nextMode == 'continue':
                        currentToken += c
                        state = nextState
                    elif nextMode == 'accept' and nextState not in [TokenType.WHITESPACE, TokenType.COMMENT]:
                        tokens.append((nextState, c))


    if currentToken and state not in [TokenType.WHITESPACE, TokenType.COMMENT]:
        tokens.append((state, currentToken))

    return tokens

""" Filter Tokens function: 
    Process a list of tokens and formats them into (type, value)
    param tokens: List of tokens found in input by scanner
    Returns tokens: A list of duples of tokens
 """
def filterFormatTokens(tokens):
    filteredTokens = []
    for tokenType, tokenVal in tokens:
        if tokenType not in [TokenType.WHITESPACE, TokenType.COMMENT, TokenType.ERROR]:
            filteredTokens.append((tokenType, tokenVal))
    return filteredTokens

""" Make State Tokens Dictionary function: 
    Process a list of tokens and populates the dictionary of States table
    param tokens: List of tokens found in input by scanner
 """
def makeStateTokensDict(tokens):
    for tokenType, tokenVal in tokens:
        if tokenType in statesTableDict and tokenVal not in statesTableDict[tokenType][1]:
            lastVal = 0
            if statesTableDict[tokenType][1]:
                lastVal = list(statesTableDict[tokenType][1].values())[-1]
            statesTableDict[tokenType][1][tokenVal] = lastVal + 1         

""" Trasform Tokens function: 
    Process a list of tokens and formats them into (token class value, token value)
    param tokens: List of tokens found in input by scanner
    Returns tokens: A list of duples of tokens values
 """
def trasformsTokens(tokens):
    makeStateTokensDict(tokens)
    filteredTokens = []
    for tokenType, tokenVal in tokens:
        if tokenType in statesTableDict and tokenVal in statesTableDict[tokenType][1]:
                tokenNum, tokenDic = statesTableDict[tokenType]
                filteredTokens.append((tokenNum, tokenDic[tokenVal]))
    return (filteredTokens, statesTableDict)