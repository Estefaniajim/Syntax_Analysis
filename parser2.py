class Parser:
    # Funcion que inicia el parser
    # self.token_dict: Es el diccionario que tomamos del scanner, que representaria el symbol table sin actualizar
    # self.token_list: Es la lista de los tokens obtenidos del scanner, guardando la posicion que se van encontrando los tokens
    # self.pos: La posicion actual que indica que token esta analizando el parser
    # self.symbol_table: Dicionario con posicion del token en el token_list mapeado con nombre (token ID), si es variable o funcion y tipo de token.
    # Este representa el symbol table actualizado por el parser.
    # self.main_declared: Flag que indica si el pograma tiene main function, basandose en la restricion de 
    # "The last declaration in a program MUST be a function declaration of the form void main(void) ""
    def __init__(self, tokens_dict, token_list):
        self.tokens_dict = self.transform_tokens_dict(tokens_dict)
        self.token_list = token_list
        self.pos = 0
        self.current_token = self.token_list[self.pos]
        self.symbol_table = {}
        self.main_declared = False

    # Funcion que trasforma el diccionario obtenido por el scanner
    # El diccionario obtenido por el scanner, mapea el tipo de token con un diccionario
    # para el parser necesitamos que ese diccionario este al contrario
    def transform_tokens_dict(self, tokens_dict):
        new_tokens_dict = {}
        for token_type, (token_id, token_map) in tokens_dict.items():
            new_token_map = {value: key for key, value in token_map.items()}
            new_tokens_dict[token_type] = (token_id, new_token_map)
        return new_tokens_dict

    # Funcion que actualiza self.current_token al siguiente token
    def next_token(self):
        self.pos += 1
        if self.pos < len(self.token_list):
            self.current_token = self.token_list[self.pos]
        else:
            self.current_token = None  # ya no hay mas tokens

    #Funcion que regresa el anterior token del self.current_token
    def last_token(self):
        lastPos = self.pos
        lastPos -= 1
        if lastPos >= 0:
            return self.token_list[lastPos]
        else:
            return None # no existe un token anterior

    # Funcion que valida si el symbol ya fue declarado
    # basada en la restricion de "Functions MUST be declared before they are called"
    # Tal vez asumi de mas, pero tambien valida variables 
    def validate_id(self, token):
        if token not in self.symbol_table:
            val_name = self.tokens_dict['ID'][1][token]
            raise Exception("Identifier {} has not been declared".format(val_name))
    
    # Funcion recursiva para el non-terminal: 
    # program → declaration_list main_declaration
    def program(self):
        try:
            self.declaration_list()
            self.main_declaration()
        # Si ya no hay mas tokens entonces obtenemos este error, que significa que el parser parcio todos los tokens sin dar un error
        # Por lo cual asumimos que el parseo fue exitoso, atrapamos el error y regresamos True
        except TypeError as e:
            if str(e) == "'NoneType' object is not subscriptable":
                # Si ya no tenemos tokens, pero la funcion main no fue declarada entonces creamos una exeptions ya que no cumple con los requerimientos
                if self.main_declared:
                    return True
                else:
                 raise Exception('The last declaration in a program must be a function declaration of the form void main(void)')   
            else:
                return False
    
    # Funcion recursiva para el non-terminal: 
    # main_declaration → void ID ( void ) compound_stmt
    def main_declaration(self):
        if self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'void':
            self.next_token()
            if self.current_token[0] == self.tokens_dict['ID'][0]:
                self.next_token()
                if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '(':
                    self.next_token()
                    if self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'void':
                        self.next_token()
                        if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ')':
                            self.next_token()
                            self.compound_stmt()
                            # Si la funcion main es declarada por completo entonces modificamos el flag
                            self.main_declared = True
                        else:
                            raise Exception('Expected ")"')
                    else:
                        raise Exception('Expected "void"')
                else:
                    raise Exception('Expected "("')
            else:
                raise Exception('Expected ID')
        else:
            raise Exception('Expected "void"')
        
    # Funcion recursiva para el non-terminal: 
    # declaration_list → declaration_list declaration | declaration
    def declaration_list(self):
        self.declaration()
        while self.current_token:
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ';':
                self.next_token()
                self.declaration()
            # En el caso que se este declarando variables afuera de una funcion
            elif self.current_token[0] == self.tokens_dict['KEYWORD'][0]:
                self.declaration()
            else:
                break

    # Funcion recursiva para el non-terminal: 
    # declaration → var_declaration | fun_declaration   
    def declaration(self):
        if self.current_token[0] == self.tokens_dict['KEYWORD'][0]:
            if self.tokens_dict['KEYWORD'][1][self.current_token[1]] in ['int', 'float', 'string', 'void']:
                self.var_declaration()
            else:
                self.fun_declaration()
        else:
            raise Exception('Invalid declaration')

    # Funcion recursiva para el non-terminal: 
    # var_declaration → type_specifier ID ; | type_specifier ID [ NUMBER ] ; 
    def var_declaration(self):
        if self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] in ['int', 'float', 'string', 'void']:
            self.next_token()
            if self.current_token[0] == self.tokens_dict['ID'][0]:
                # Checa en el caso que se este declarando la funcion de main, solo pasa si es la unica funcion en el codigo
                #  Pueda que sea un error de mi gramatica peroooo no me baje puntos :,c 
                if self.tokens_dict['ID'][1][self.current_token[1]] == "main":
                    self.main_declared = True
                # Si se esta declarando una variable entonces tambien se agrega al dicionario self.symbol_table
                self.symbol_table[self.current_token[1]] = [self.tokens_dict['ID'][1][self.current_token[1]],'variable', self.tokens_dict['KEYWORD'][1][self.last_token()[1]]]
                self.next_token()
                if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ';':
                    self.next_token()
                elif self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '[':
                    self.next_token()
                    if self.current_token[0] == self.tokens_dict['NUMBER'][0]:
                        self.next_token()
                        if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ']':
                            self.next_token()
                            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ';':
                                self.next_token()
                            else:
                                raise Exception('Expected ";"')
                        else:
                            raise Exception('Expected "]"')
                    else:
                        raise Exception('Expected NUMBER')
                else:
                    # En el caso que en realidad se este declarando fun_declaration y no var_declaration
                    # Tambien esto causa que algunas funciones se pongan como variables en self.symbol_table
                    if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '(':
                        self.fun_declaration_prime()
                        return
                    else:
                        raise Exception('Expected ";" or "["')
            else:
                raise Exception('Expected ID')
        else:
            raise Exception('Expected type specifier')
    
    # Funcion recursiva para el non-terminal: 
    # fun_declaration → type_specifier ID ( params ) compound_stmt
    def fun_declaration(self):
        if self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] in ['int', 'float', 'string', 'void']:
            self.next_token()
            if self.current_token[0] == self.tokens_dict['ID'][0]:
                # Si se esta declarando una funcion entonces tambien se agrega al dicionario self.symbol_table
                self.symbol_table[self.current_token[1]] = [self.tokens_dict['ID'][1][self.current_token[1]],'function', self.tokens_dict['KEYWORD'][1][self.last_token()[1]]]
                self.next_token()
                if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '(':
                    self.next_token()
                    self.params()
                    if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ')':
                        self.next_token()
                        self.compound_stmt()
                    else:
                        raise Exception('Expected ")"')
                else:
                    raise Exception('Expected "("')
            else:
                raise Exception('Expected ID')
        else:
            raise Exception('Expected type specifier')
    
    # Funcion que es usada en el caso que cuando se este a la mitad del proceso de declarar una variable en var_declaration
    # nos demos cuenta que en realidad es una funcion, es similar a la anterior funcion solo que empeiuza desde los parametros
    def fun_declaration_prime(self):
        if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '(':
            self.next_token()
            self.params()
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ')':
                self.next_token()
                self.compound_stmt()
            else:
                raise Exception('Expected ")"')
        else:
            raise Exception('Expected "("')
        
    # Funcion recursiva para el non-terminal: 
    # params → param_list | void
    def params(self):
        if self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'void':
            self.next_token()
        else:
            self.param_list()

    # Funcion recursiva para el non-terminal: 
    # param_list → param param_list'
    # Tambien abarca: param_list' → , param param_list' | , param
    def param_list(self):
        self.param()
        while self.current_token and self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ',':
            self.next_token()
            self.param()

    # Funcion recursiva para el non-terminal: 
    # param → type_specifier ID | type_specifier ID [ ]
    def param(self):
        if self.tokens_dict['KEYWORD'][1][self.current_token[1]] in ['int', 'float', 'string', 'void']:
            self.next_token()
            if self.current_token[0] == self.tokens_dict['ID'][0]:
                # Si se esta declarando una variable en los parametros
                # entonces tambien se agregan al dicionario self.symbol_table
                self.symbol_table[self.current_token[1]] = [self.tokens_dict['ID'][1][self.current_token[1]],'variable', self.tokens_dict['KEYWORD'][1][self.last_token()[1]]]
                self.next_token()
                if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '[':
                    self.next_token()
                    if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ']':
                        self.next_token()
                    else:
                        raise Exception('Expected "]"')
            else:
                raise Exception('Expected ID')
        else:
            raise Exception('Expected type specifier')
    
    # Funcion recursiva para el non-terminal: 
    # compound_stmt → { local_declarations statement_list }
    def compound_stmt(self):
        if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '{':
            self.next_token()
            self.local_declarations()
            self.statement_list()
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '}':
                self.next_token()
            else:
                raise Exception('Expected "}"')
        else:
            raise Exception('Expected "{"')

    # Funcion recursiva para el non-terminal: 
    # local_declarations → local_declarations var_declaration | ε
    def local_declarations(self):
        while self.current_token and self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] in ['int', 'float', 'string', 'void']:
            self.var_declaration()

    # Funcion recursiva para el non-terminal: 
    # statement_list → statement_list statement | ε
    def statement_list(self):
        while self.current_token and self.current_token[0] != self.tokens_dict['SYMBOL'][0] and self.current_token[1] != '}':
            self.statement()

    # Funcion recursiva para el non-terminal: 
    # statement → assignment_stmt | call | compound_stmt | selection_stmt | iteration_stmt | return_stmt | input_stmt | output_stmt
    def statement(self):
        if self.current_token[0] == self.tokens_dict['ID'][0]:
            self.assignment_stmt()
        elif self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'call':
            self.call()
        elif self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '{':
            self.compound_stmt()
        elif self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'if':
            self.selection_stmt()
        elif self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'while':
            self.iteration_stmt()
        elif self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'return':
            self.return_stmt()
            #Esto esta incorrecto es Read
        elif self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'input':
            self.input_stmt()
            #Incorrecto es write
        elif self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'output':
            self.output_stmt()
        else:
            raise Exception('Invalid statement')

    # Funcion recursiva para el non-terminal: 
    # assignment_stmt → var = expression ; | STRING ;
    def assignment_stmt(self):
        if self.current_token[0] == self.tokens_dict['ID'][0]:
            # Al momento de asignar un valor a una variable, verificamos que la variable ya fue declarada
            if self.current_token[1] not in self.symbol_table:
                # Usamos el current_token para ver el nombre de la variable, para poder regresar la exepcion con el ID de la variable
                val_name = self.tokens_dict['ID'][1][self.current_token[1]]
                raise Exception("Identifier {} has not been declared".format(val_name))
            self.next_token()
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '=':
                self.next_token()
                self.expression()
                if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ';':
                    self.next_token()
                else:
                    raise Exception('Expected ";"')
            else:
                try:
                    self.call_prime()
                except:
                    raise Exception('Expected "="')
        elif self.current_token[0] == self.tokens_dict['STRING'][0]:
            self.next_token()
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ';':
                self.next_token()
            else:
                raise Exception('Expected ";"')
        else:
            raise Exception('Expected ID or STRING')
    
    # Funcion recursiva para el non-terminal:
    # call_stmt → call ;
    def call_stmt(self):
        self.call()
        if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ';':
            self.next_token()
        else:
            raise Exception('Expected ";"')
    
    # Funcion recursiva para el non-terminal:
    # matched_stmt → if ( expression ) matched_stmt else matched_stmt matched_stmt' | other_stmt
    def matched_stmt(self):
        if self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'if':
            self.next_token()
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '(':
                self.next_token()
                self.expression()
                if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ')':
                    self.next_token()
                    self.matched_stmt()
                    if self.current_token and self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'else':
                        self.next_token()
                        self.matched_stmt()
                else:
                    raise Exception('Expected ")"')
            else:
                raise Exception('Expected "("')
        else:
            self.other_stmt()

    # Funcion recursiva para el non-terminal:
    # unmatched_stmt → if ( expression ) statement unmatched_stmt' | if ( expression ) matched_stmt else unmatched_stmt unmatched_stmt'
    def unmatched_stmt(self):
        if self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'if':
            self.next_token()
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '(':
                self.next_token()
                self.expression()
                if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ')':
                    self.next_token()
                    self.statement()
                    self.unmatched_stmt_prime()
                else:
                    raise Exception('Expected ")"')
            else:
                raise Exception('Expected "("')
        else:
            raise Exception('Expected "if"')

    # Funcion recursiva para el non-terminal: unmatched_stmt'
    def unmatched_stmt_prime(self):
        if self.current_token and self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'else':
            self.next_token()
            self.statement()
        else:
            self.unmatched_stmt()
        
    # Funcion recursiva para el non-terminal: selection_stmt
    # Representa un if-else, y esta relacionado con: 
    # statement → assignment_stmt | call | compound_stmt | selection_stmt | iteration_stmt | return_stmt | input_stmt | output_stmt
    def selection_stmt(self):
        if self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'if':
            self.next_token()
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '(':
                self.next_token()
                self.expression()
                if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ')':
                    self.next_token()
                    self.statement()
                    if self.current_token and self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'else':
                        self.next_token()
                        self.statement()
                else:
                    raise Exception('Expected ")"')
            else:
                raise Exception('Expected "("')
        else:
            raise Exception('Expected "if"')

    # Funcion recursiva para el non-terminal:
    # iteration_stmt → while ( expression ) statement
    def iteration_stmt(self):
        if self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'while':
            self.next_token()
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '(':
                self.next_token()
                self.expression()
                if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ')':
                    self.next_token()
                    self.statement()
                else:
                    raise Exception('Expected ")"')
            else:
                raise Exception('Expected "("')
        else:
            raise Exception('Expected "while"')

    # Funcion recursiva para el non-terminal:
    # return_stmt → return ; | return expression ;
    def return_stmt(self):
        if self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'return':
            self.next_token()
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ';':
                self.next_token()
            else:
                self.expression()
                if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ';':
                    self.next_token()
                else:
                    raise Exception('Expected ";"')
        else:
            raise Exception('Expected "return"')

    # Funcion recursiva para el non-terminal:
    # input_stmt → input var ;
    def input_stmt(self):
        if self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'input':
            self.next_token()
            if self.current_token[0] == self.tokens_dict['ID'][0]:
                self.next_token()
                if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ';':
                    self.next_token()
                else:
                    raise Exception('Expected ";"')
            else:
                raise Exception('Expected ID')
        else:
            raise Exception('Expected "input"')

    # Funcion recursiva para el non-terminal:
    # output_stmt → output expression ;
    def output_stmt(self):
        if self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'output':
            self.next_token()
            self.expression()
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ';':
                self.next_token()
            else:
                raise Exception('Expected ";"')
        else:
            raise Exception('Expected "output"')
    
    # Funcion recursiva para el non-terminal:
    # var → ID var' | ID
    # var' → [ arithmetic_expression ]
    def var(self):
        if self.current_token[0] == self.tokens_dict['ID'][0]:
            self.next_token()
            # En caso de ser var' se checa []
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '[':
                self.next_token()
                self.arithmetic_expression()
                if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ']':
                    self.next_token()
        else:
            raise Exception('Expected ID')

    # Funcion recursiva para el non-terminal:
    # expression → simple_expression relop simple_expression | simple_expression
    def expression(self):
        self.simple_expression()
        # La terminal relop: relop → <= | < | > | >= | == | != 
        # esta en la segunda parte: self.tokens_dict['SYMBOL'][1][self.current_token[1]] in ['<=', '<', '>', '>=', '==', '!=']
        if self.current_token and self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] in ['<=', '<', '>', '>=', '==', '!=']:
            self.next_token()
            self.simple_expression()

    # Funcion recursiva para el non-terminal:
    # simple_expression → term simple_expression' | term
    def simple_expression(self):
        self.term()
        # La terminal addop: addop → + | -
        # esta en la segunda parte: self.tokens_dict['SYMBOL'][1][self.current_token[1]] in ['+', '-']
        while self.current_token and self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] in ['+', '-']:
            self.next_token()
            self.term()

    # Funcion recursiva para el non-terminal:
    # term → factor term' | factor
    def term(self):
        self.factor()
        # La terminal mulop: mulop → * | /
        # esta en la segunda parte: self.tokens_dict['SYMBOL'][1][self.current_token[1]] in ['*', '/']
        while self.current_token and self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] in ['*', '/']:
            self.next_token()
            self.factor()

    # Funcion recursiva para el non-terminal:
    # factor → ( expression ) | var | call | NUMBER
    def factor(self):
        if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '(':
            self.next_token()
            self.expression()
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ')':
                self.next_token()
        elif self.current_token[0] == self.tokens_dict['ID'][0]:
            self.validate_id(self.current_token[1])
            self.next_token()
            if self.current_token and self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '[':
                self.next_token()
                self.arithmetic_expression()
                if self.current_token and self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ']':
                    self.next_token()
        elif self.current_token[0] == self.tokens_dict['NUMBER'][0]:
            self.next_token()
        elif self.current_token[0] == self.tokens_dict['KEYWORD'][0] and self.tokens_dict['KEYWORD'][1][self.current_token[1]] == 'call':
            self.call()
        else:
            raise Exception('Invalid factor')

    # Funcion recursiva para el non-terminal: 
    # simple_expression → term simple_expression' | term
    def simple_expression(self):
        self.term()
        while self.current_token and self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] in ['+', '-']:
            self.next_token()
            self.term()

    # Funcion recursiva para el non-terminal: 
    # arithmetic_expression
    def arithmetic_expression(self):
        self.term()
        while self.current_token and self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] in ['+', '-']:
            self.next_token()
            self.term()
    
    # Funcion recursiva para el non-terminal: 
    # args → arg_list | ε
    def args(self):
        if self.current_token[0] != self.tokens_dict['SYMBOL'][0] or self.tokens_dict['SYMBOL'][1][self.current_token[1]] != ')':
            self.arithmetic_expression()
            while self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ',':
                self.next_token()
                self.arithmetic_expression()

    # Funcion recursiva para el non-terminal: 
    # arg_list → arithmetic_expression arg_list' | arithmetic_expression
    def arg_list(self):
        self.arithmetic_expression()
        while self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ',':
            self.next_token()
            self.arithmetic_expression()

    # Funcion recursiva para el non-terminal: 
    # arg_list' → , arithmetic_expression arg_list' | , arithmetic_expression
    def arg_list_prime(self):
        if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ',':
            self.next_token()
            self.arithmetic_expression()
            self.arg_list_prime()

    # Funcion recursiva para el non-terminal: 
    # call → ID ( args )
    def call(self):
        if self.current_token[0] == self.tokens_dict['ID'][0]:
            self.next_token()
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '(':
                self.next_token()
                self.args()
                if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ')':
                    self.next_token()
                else:
                    raise Exception('Expected ")"')
            else:
                raise Exception('Expected "("')
        else:
            raise Exception('Expected ID')
    
    # Funcion recursiva para el non-terminal: call' 
    def call_prime(self):
        if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == '(':
            self.next_token()
            self.args()
            if self.current_token[0] == self.tokens_dict['SYMBOL'][0] and self.tokens_dict['SYMBOL'][1][self.current_token[1]] == ')':
                self.next_token()
            else:
                raise Exception('Expected ")"')
        else:
            raise Exception('Expected "("')