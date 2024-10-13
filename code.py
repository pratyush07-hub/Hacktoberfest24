import tkinter as tk
from tkinter import ttk
import ply.lex as lex
import ply.yacc as yacc

# Database table attributes
attributes = {'name', 'roll', 'cpi'}

# Define tokens
tokens = [
    'SELECT', 'FROM', 'WHERE', 'UPDATE', 'SET', 'COMPARISON', 'NUMBER', 'ALL',
    'AND', 'OR', 'ID'
]

# Regular expression rules for tokens
t_SELECT = r'select'
t_FROM = r'from'
t_WHERE = r'where'
t_UPDATE = r'update'
t_SET = r'set'
t_COMPARISON = r'[><]=?|!='
t_NUMBER = r'\d+'
t_ALL = r'all'
t_AND = r'and'
t_OR = r'or'
t_ignore = ' \t\n'

# Define a function to handle identifiers (table names, column names)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value.lower() in attributes:
        t.type = t.value.upper()  # Convert to uppercase for reserved words
    return t

# Error handling
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Grammar rules
def p_query(p):
    '''query : select_query
             | update_query'''
    p[0] = p[1]

def p_select_query(p):
    '''select_query : SELECT columns FROM ID where_clause_opt'''
    p[0] = 'select {} from {}'.format(p[2], p[4]) + (' ' + p[5] if p[5] else '')

def p_columns(p):
    '''columns : ALL
               | column_list'''
    p[0] = '*' if p[1].lower() == 'all' else p[1]

def p_column_list(p):
    '''column_list : ID
                   | ID ',' column_list'''
    if len(p) > 2:
        p[0] = p[1] + ', ' + p[3]
    else:
        p[0] = p[1]

def p_where_clause_opt(p):
    '''where_clause_opt : empty
                        | WHERE condition'''
    p[0] = p[2] if len(p) > 2 else ''

def p_condition(p):
    '''condition : ID COMPARISON NUMBER
                 | condition AND condition
                 | condition OR condition'''
    if len(p) == 4:
        p[0] = '{} {} {}'.format(p[1], p[2], p[3])
    else:
        p[0] = '({} {} {})'.format(p[1], p[2], p[3])

def p_update_query(p):
    '''update_query : UPDATE ID SET ID '=' NUMBER WHERE ID '=' NUMBER'''
    p[0] = 'update {} set {}={} where {}={}'.format(p[2], p[4], p[6], p[8], p[10])

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

# Function to parse the input and display the SQL query
def parse_input():
    input_sentence = entry.get()
    result = parser.parse(input_sentence)
    query_text.delete('1.0', tk.END)
    query_text.insert(tk.END, result)

# GUI setup
root = tk.Tk()
root.title("English to SQL Parser")

# Frame for input and button
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

entry = ttk.Entry(input_frame, width=50)
entry.grid(row=0, column=0, padx=5)

parse_button = ttk.Button(input_frame, text="Parse", command=parse_input)
parse_button.grid(row=0, column=1, padx=5)

# Frame for displaying the SQL query
output_frame = ttk.Frame(root)
output_frame.pack(pady=10)

query_text = tk.Text(output_frame, width=50, height=5)
query_text.pack()

root.mainloop()
