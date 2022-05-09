
from lark import Lark
my_grammar = """
?start: query_args
query_args: query+
 
?query: select_arg
            | from_arg
            | where_arg
            | group_by_arg
  
select_arg: "SELECT" summary_arg+ -> sel_smry
            | "SELECT *" -> sel_all
            | "SELECT" var -> sel_var
 
summary_arg: var 
            | "MAX(" var ")" -> mx 
            | "MIN(" var ")" -> mn
            | "SUM(" var ")" -> sm
            | "AVG(" var ")" -> avge
 
var:   NAME
dat: NAME
dat_name: NAME
 
from_arg: "FROM" dat ";" 
 
val: var
    | NUMBER
 
where_arg: "WHERE" expression ";"
            | "WHERE" bool ";"
 
bool: "(" expression "AND" expression ")" -> and_st
        | "(" expression "OR" expression ")" -> or_st
 
expression: val
            | var
            | expression "=" expression -> eq
            | expression "<>" expression -> neq
            | expression ">" expression -> gth
            | expression ">=" expression -> gth_eq
            | expression "<" expression -> lth
            | expression "<=" expression -> lth_eq
 
group_by_arg: "GROUP_BY(" var ")"
 
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
    return '\n'.join(map(translate, t.children))
  elif t.data == 'sel_all':
    #sel_all = True
    return
  elif t.data == 'sel_smry':
    #sel_smry = True   # currently can't do summary args and just plain vars, or list of multiple summary args? - ie select max(thing1), min(thing2)
    return "summarise(" + translate(t.children) + ")"
  elif t.data == "sel_var":
    #sel_vars = True
    #selected_vars = t.children
    return
  elif t.data == 'from_arg':
    #given_dat = t.children
    return
  elif t.data == 'val':
    return
    #return t.children
  elif t.data == 'mx':
    #mx_present = True
    #mx_var = t.children
    return 
  elif t.data == 'mn':
    #mn_present = True
    #mn_var = t.children
    return 
  elif t.data == 'sm':
    #sm_present = True
    #sm_var = t.children
    return
  elif t.data == 'avge':
    #avge_present = True
    #avge_var = t.children
    return
   
    
  

parser = Lark(my_grammar)
program = """
SELECT MAX(candy_eater_id)
FROM hi
"""
parse_tree = parser.parse(program)
print(translate(parse_tree))
#if sel_smry:
  #r_code += "summarise(max(" + mx_var + ")"
#print(parse_tree.pretty())
