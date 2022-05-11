from lark import Lark
my_grammar = """
?start: query_args
query_args: query+ 
 
?query: select_arg 
            | from_arg 
            | where_arg 
            | group_by_arg 
  
select_arg: "SELECT" summary_arg -> sel_smry
            | "SELECT *" -> sel_all
            | "SELECT" var_sel -> sel_var
 
summary_arg: "MAX(" var_sel ")" -> mx 
            | "MIN(" var_sel ")" -> mn
            | "SUM(" var_sel ")" -> sm
            | "AVG(" var_sel ")" -> avge
 
var: NAME
dat: NAME
var_group: NAME
var_sel: NAME
 
from_arg: "FROM" dat 
 
literal: NUMBER
 
where_arg: "WHERE" expression+
            | "WHERE" bool+
 
?bool: expression
        | "(" bool "AND" bool ")" -> and_st
        | "(" bool "OR" bool ")" -> or_st
 
?expression: var
            | literal
            | expression "=" expression  -> eq
            | expression "<>" expression -> neq
            | expression ">" expression  -> gth
            | expression ">=" expression -> gth_eq
            | expression "<" expression -> lth
            | expression "<=" expression -> lth_eq
 
group_by_arg: "GROUP_BY" var_group 
 
%import common.CNAME -> NAME
%import common.INT -> NUMBER
%import common.NEWLINE -> NEWLINE
%import common.WS
%ignore WS
"""

found_from = False
found_where = False
found_group = False
found_smry = False
found_sel_var = False
found_sel_all = False
given_data = ''


def find_data(t):

  if t.data == 'query_args':
    return '\n'.join(map(find_data, t.children))
  elif t.data == 'from_arg':
    global given_data 
    given_data = translate(t.children[0])
    global found_from
    found_from = True
    return ''

  elif t.data == 'where_arg':
    global found_where 
    found_where = True
    return ''

  elif t.data == 'group_by_arg':
    global found_group   
    found_group = True
    return ''

  elif t.data == 'sel_smry':
    global found_smry 
    found_smry = True
    return ''

  elif t.data == 'sel_all':
    global found_sel_all 
    found_sel_all = True
    return ''

  elif t.data == 'sel_var':
    global found_sel_var
    found_sel_var = True
    return ''          

def reorder(my_input):
  my_input = list(my_input.split('\n'))
  num_elems = len(my_input)
  new_program = [''] * (num_elems)
  for item in my_input:
    if item.startswith("WHERE"):
      new_program[1] = item

    elif item.startswith("FROM"):
      new_program[0] = item

    elif item.startswith("SELECT"):
      if found_group and not found_smry:
        new_program[-2] = item
      else:
        new_program[-1] = item

    elif item.startswith("GROUP_BY"):
      if found_smry:
        new_program[-2] = item
      else:
        new_program[-1] = item
  return new_program

def translate(t):

  if t.data == 'query_args':
    return '\n'.join(map(translate, t.children))

  elif t.data == 'sel_all':
    return ''

  elif t.data == 'sel_smry':
    my_args = t.children[0]
    return given_data + ' <- summarise(' + given_data + ', ' + translate(my_args) + ')'

  elif t.data == 'sel_var':
    my_args = t.children[0]
    return given_data + ' <- filter(' + given_data + ', ' + translate(my_args) + ')'

  elif t.data == 'from_arg':
    return '' 

  elif t.data == 'mx':
    return 'max(' + translate(t.children[0]) + ')'

  elif t.data == 'mn':
    return 'min(' + translate(t.children[0]) + ')'

  elif t.data == 'sm':
    return 'sum(' + translate(t.children[0]) + ')'

  elif t.data == 'avge':
    return 'avg(' + translate(t.children[0]) + ')'

  elif t.data == 'where_arg':
    where_stuff = t.children[0]
    return given_data + ' <- filter(' + given_data + ', ' + translate(where_stuff) + ')'

  elif t.data == 'literal':
    return t.children[0]

  elif t.data == 'var':
    return t.children[0]

  elif t.data == 'var_group':
    return t.children[0]

  elif t.data == 'var_sel':
    return t.children[0]

  elif t.data == 'dat':
    return t.children[0]

  elif t.data == 'eq':
    lhs = t.children[0]
    rhs = t.children[1]
    return translate(lhs) + ' = ' + translate(rhs)      
  
  elif t.data == 'neq':
    lhs = t.children[0]
    rhs = t.children[1]
    return translate(lhs) + ' != ' + translate(rhs)

  elif t.data == 'gth':
    lhs = t.children[0]
    rhs = t.children[1]
    return translate(lhs) + ' > ' + translate(rhs)

  elif t.data == 'gth_eq':
    lhs = t.children[0]
    rhs = t.children[1]
    return translate(lhs) + ' >= ' + translate(rhs)        
  
  elif t.data == 'lth':
    lhs = t.children[0]
    rhs = t.children[1]
    return translate(lhs) + ' < ' + translate(rhs)

  elif t.data == 'lth_eq':
    lhs = t.children[0]
    rhs = t.children[1]
    return translate(lhs) + ' <= ' + translate(rhs)

  elif t.data == 'group_by_arg':
    return given_data + ' <- group_by(' + given_data + ', ' + translate(t.children[0]) + ')'
  
  elif t.data == 'and_st':
    lhs = t.children[0]
    rhs = t.children[1]
    return '(' + translate(lhs) + ' & ' + translate(rhs) + ')'

  elif t.data == 'or_st':
    lhs = t.children[0]
    rhs = t.children[1]
    return '(' + translate(lhs) + ' | ' + translate(rhs) + ')'

  else:
    raise SyntaxError("bad tree")
   
parser = Lark(my_grammar)

input_file = input("Enter file path: ")
open_file = open(input_file, "r")
program = open_file.read()
open_file.close()

parse_tree = parser.parse(program)
#print(parse_tree.pretty())
find_data(parse_tree)
new_program = reorder(program)
new_program = '\n'.join(new_program)
final_parse_tree = parser.parse(new_program)
#print(final_parse_tree.pretty())
print("library(tidyverse)\n")
print(translate(final_parse_tree))
