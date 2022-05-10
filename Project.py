
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
            | "SELECT" var+ -> sel_var
 
summary_arg: var 
            | "MAX(" var ")" -> mx 
            | "MIN(" var ")" -> mn
            | "SUM(" var ")" -> sm
            | "AVG(" var ")" -> avge
 
var:   NAME
dat: NAME
dat_name: NAME
 
from_arg: "FROM" dat 
 
literal: NUMBER
 
where_arg: "WHERE" expression+
            | "WHERE" bool+
 
bool: expression
        | bool
        | "(" bool+ "AND" bool+ ")" -> and_st
        | "(" bool+ "OR" bool+ ")" -> or_st
 
?expression: var
            | literal
            | expression "=" expression -> eq
            | expression "<>" expression -> neq
            | expression ">" expression -> gth
            | expression ">=" expression -> gth_eq
            | expression "<" expression -> lth
            | expression "<=" expression -> lth_eq
 
group_by_arg: "GROUP_BY" var 
 
%import common.CNAME -> NAME
%import common.INT -> NUMBER
%import common.WS
%ignore WS
"""
r_code = ""
sel_smry = False
mx_present = False
mx_var = ""

def translate(t):

  if t.data == 'query_args':
    #print(t.children)
    return '\n'.join(map(translate, t.children))

  elif t.data == 'sel_all':
    #sel_all = True
    #stuff = t.children[0]
    return "" #translate(stuff)

  elif t.data == 'sel_smry':
    #sel_smry = True   # currently can't do summary args and just plain vars, or list of multiple summary args? - ie select max(thing1), min(thing2)
    my_args = t.children[0]
    #print(my_args)
    return 'summarise(' + translate(my_args) + ')'

  elif t.data == 'sel_var':
    #sel_vars = True
    #selected_vars = t.children
    return "select(" + t.children[0] + ")"

  elif t.data == 'from_arg':
    #given_dat = t.children
    #print("in from")
    print(t.children[0])
    words = t.children[0]
    return 'from ' + translate(words)
    #return t.children

  elif t.data == 'mx':
    #mx_present = True
    #mx_var = t.children
    return "max(" + translate(t.children[0]) + ")"

  elif t.data == 'mn':
    #mn_present = True
    #mn_var = t.children
    return "min(" + translate(t.children[0]) + ")"

  elif t.data == 'sm':
    #sm_present = True
    #sm_var = t.children
    return "sum(" + translate(t.children[0]) + ")"

  elif t.data == 'avge':
    #avge_present = True
    #avge_var = t.children
    return "avg(" + translate(t.children[0]) + ")"

  elif t.data == 'where_arg':
    where_stuff = t.children[0]
    return 'filter(' + translate(where_stuff) + ')'

  elif t.data == 'literal':
    return t.children[0]

  elif t.data == 'var':
    return t.children[0]

  elif t.data == 'dat':
    return t.children[0]

  elif t.data == 'eq':
    lhs = t.children[0]
    rhs = t.children[1]
    return translate(lhs) + ' = ' + translate(rhs)        # or is is '=='
  
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
    return "group_by(" + translate(t.children[0]) + ")"
  
  elif t.data == 'and_st':
    lhs = t.children[0]
    rhs = t.children[1]
    return translate(lhs) + ' & ' + translate(rhs)

  elif t.data == 'and_st':
    lhs = t.children[0]
    rhs = t.children[1]
    return translate(lhs) + ' | ' + translate(rhs)

  else:
    raise SyntaxError("bad tree")
   
parser = Lark(my_grammar)
program = """
SELECT MAX(this)
FROM hi
WHERE ((9 = 1 OR 9 = 3) AND x > 7)
"""
parse_tree = parser.parse(program)
print(translate(parse_tree))
#if sel_smry:
  #r_code += "summarise(max(" + mx_var + ")"
#print(parse_tree.pretty())


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
            | "SELECT" var+ -> sel_var
 
summary_arg: var 
            | "MAX(" var ")" -> mx 
            | "MIN(" var ")" -> mn
            | "SUM(" var ")" -> sm
            | "AVG(" var ")" -> avge
 
var:   NAME
dat: NAME
dat_name: NAME
 
from_arg: "FROM" dat 
 
literal: NUMBER
 
where_arg: "WHERE" expression+
            | "WHERE" bool+
 
bool: expression
        | bool
        | "(" bool+ "AND" bool+ ")" -> and_st
        | "(" bool+ "OR" bool+ ")" -> or_st
 
?expression: var
            | literal
            | expression "=" expression -> eq
            | expression "<>" expression -> neq
            | expression ">" expression -> gth
            | expression ">=" expression -> gth_eq
            | expression "<" expression -> lth
            | expression "<=" expression -> lth_eq
 
group_by_arg: "GROUP_BY" var 
 
%import common.CNAME -> NAME
%import common.INT -> NUMBER
%import common.WS
%ignore WS
"""
r_code = ""
sel_smry = False
mx_present = False
mx_var = ""

def translate(t):

  if t.data == 'query_args':
    #print(t.children)
    return '\n'.join(map(translate, t.children))

  elif t.data == 'sel_all':
    #sel_all = True
    #stuff = t.children[0]
    return "" #translate(stuff)

  elif t.data == 'sel_smry':
    #sel_smry = True   # currently can't do summary args and just plain vars, or list of multiple summary args? - ie select max(thing1), min(thing2)
    my_args = t.children[0]
    #print(my_args)
    return 'summarise(' + translate(my_args) + ')'

  elif t.data == 'sel_var':
    #sel_vars = True
    #selected_vars = t.children
    return "select(" + t.children[0] + ")"

  elif t.data == 'from_arg':
    #given_dat = t.children
    #print("in from")
    print(t.children[0])
    words = t.children[0]
    return 'from ' + translate(words)
    #return t.children

  elif t.data == 'mx':
    #mx_present = True
    #mx_var = t.children
    return "max(" + translate(t.children[0]) + ")"

  elif t.data == 'mn':
    #mn_present = True
    #mn_var = t.children
    return "min(" + translate(t.children[0]) + ")"

  elif t.data == 'sm':
    #sm_present = True
    #sm_var = t.children
    return "sum(" + translate(t.children[0]) + ")"

  elif t.data == 'avge':
    #avge_present = True
    #avge_var = t.children
    return "avg(" + translate(t.children[0]) + ")"

  elif t.data == 'where_arg':
    where_stuff = t.children[0]
    return 'filter(' + translate(where_stuff) + ')'

  elif t.data == 'literal':
    return t.children[0]

  elif t.data == 'var':
    return t.children[0]

  elif t.data == 'dat':
    return t.children[0]

  elif t.data == 'eq':
    lhs = t.children[0]
    rhs = t.children[1]
    return translate(lhs) + ' = ' + translate(rhs)        # or is is '=='
  
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
    return "group_by(" + translate(t.children[0]) + ")"
  
  elif t.data == 'and_st':
    lhs = t.children[0]
    rhs = t.children[1]
    return translate(lhs) + ' & ' + translate(rhs)

  elif t.data == 'and_st':
    lhs = t.children[0]
    rhs = t.children[1]
    return translate(lhs) + ' | ' + translate(rhs)

  else:
    raise SyntaxError("bad tree")
   
parser = Lark(my_grammar)
program = """
SELECT MAX(this)
FROM hi
WHERE ((9 = 1 OR 9 = 3) AND x > 7)
"""
parse_tree = parser.parse(program)
print(translate(parse_tree))
#if sel_smry:
  #r_code += "summarise(max(" + mx_var + ")"
#print(parse_tree.pretty())

