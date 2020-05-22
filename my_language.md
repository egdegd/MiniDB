#Язык запросов к графу
###Описание синтаксиса

Скрипт состоит из нескольких STMT разделенных SEMI. Допускается пустое скрипт. После каждого STMT необходим разделитель, в том числе после последнего.
```
SCRIPT:             ε 
                    | STMT semi SCRIPT
                  
STMT:               kw_connect kw_to string
                    | LIST
                    | SELECT_STMT
                    | NAMED_PATTERN_STMT
                    | kw_write SELECT_STMT kw_to string
                   
LIST:               kw_list kw_all kw_graphs
                    | kw_list kw_all kw_graphs kw_from string
                    
NAMED_PATTERN_STMT: nt_name op_eq PATTERN

SELECT_STMT:        kw_select OBJ_EXPR kw_from string kw_where WHERE_EXPR
                    | kw_select OBJ_EXPR kw_from string

OBJ_EXPR:           VS_INFO
                    | kw_count VS_INFO
                    | kw_exists VS_INFO
                    
VS_INFO:            lbr ident comma ident rbr
                    | lbr ident rbr
                    
WHERE_EXPR:         lbr V_EXPR rbr op_minus PATTERN op_minus op_gr lbr V_EXPR rbr
                    | lbr V_EXPR rbr
                    | lbr V_EXPR comma V_EXPR rbr

V_EXPR:             ident
                    | underscore
                    | ident dot kw_id op_eq int
                   
PATTERN:            ALT_ELEM
                    | ALT_ELEM mid PATTERN
                 
ALT_ELEM:           SEQ
                    | lbr rbr
                    
SEQ:                SEQ_ELEM
                    | SEQ_ELEM SEQ
                    
SEQ_ELEM:           PRIM_PATTERN
                    | PRIM_PATTERN op_star
                    | PRIM_PATTERN op_plus
                    | PRIM_PATTERN op_q       
                    
PRIM_PATTERN:       ident
                    | nt_name
                    |lbr PATTERN rbr                                                             
```

###Токены (терминальный алфавит)
```
semi = ';'
kw_connect = 'CONNECT'
kw_to = 'TO'
string = '['([aA−zZ]|[0−9]|('−'|''|'_'|'/'|'.'))∗']'
kw_list = 'LIST'
kw_all = 'ALL'
kw_graphs = 'GRAPHS'
nt_name = [A-Z][a-z]*
op_eq = '='
kw_write = 'WRITE'
kw_select = 'SELECT'
kw_from = 'FROM'
kw_where = 'WHERE'
kw_count = 'COUNT'
kw_exists = 'EXISTS'
lbr = '('
rbr = ')'
ident = [a-z][a-z]*
comma = ','
op_minus = '-'
op_gr = '>'
underscore = '_'
dot = '.'
kw_id = 'ID'
int = 0 | [1-9][0-9]*
mid = '|'
op_star = '*'
op_plus = '+'
op_q = '?'
```

####Примеры скриптов
```
CONNECT TO [\home\graph];
S = a S b S | ();
SELECT COUNT(u) FROM [graph] where (v.ID = 2) - S -> (u);
```
```
CONNECT TO [\home\graph213];
SELECT  EXISTS(u, v) FROM [my_graph.txt] where (u) - (a)* -> (u);
WRITE SELECT COUNT(a, b) FROM [my_graph.txt] WHERE (a.ID = 1) - S -> (b.ID = 2) TO [file.txt];
```
```
CONNECT TO [\home\graphs];
LIST OF ALL GRAPHS;
```
```
CONNECT TO [\home\graphs];
LIST OF ALL GRAPHS FROM [\home\other_graphs];
```