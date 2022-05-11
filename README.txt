(1) I am parsing a subset of SQL into R code. The available SQL arguments are 'SELECT', 'FROM', 'WHERE', and 'GROUP_BY'. 'SELECT' takes a single argument of
    either a variable or an aggregate applied to a variable. The available aggregate functions are 'MAX', 'MIN', 'SUM', and 'AVG'. 'FROM' takes a single argument
    of a data frame to use to perform the operations of the query. 'WHERE' can take several arguments. First, it can take a single boolean comparison expression, 
    comparing either two numbers, two variables, or a variable and a number. The specific boolean comparisons available are 'greater than', 
    'greater than or equal to', 'less than', 'less than or equal to', 'equal to', and 'not equal to'. Secondly, it can take a boolean operator that compares two
    boolean expressions. The two boolean operators available are 'AND' and 'OR'. The 'AND' and 'OR' expressions can also be nested. For example it is possible to 
    have the expression (1 <> 2 AND 35 = total_hours) OR num_days_present > num_days_absent) as the 'WHERE' argument. Finally, the argument from the 'FROM' 
    statement is isolated and treated as the data frame, For the translation, the variable from the 'FROM' statement is used as the data frame, the contents of 
    the 'WHERE' statement are put into a 'filter' statement, 'SELECT' statements with a variable argument are converted into 'filter' statements, 'SELECT *' 
    statements are essentially ignored - as they select all of the variables there is no need to filter -, the 'GROUP_BY' statements are turned into 'group_by' 
    statements with proper R syntax, and lastly, if a 'SELECT' statement is used with an aggregate function argument, it is converted into a 'summarise' 
    statement at the very end. The data frame given in 'FROM' is changed each time any of these statements are used. 

(2) It is worth noting that the order in which each of the statement conversions was explained above is the order in which they are converted. The 'tidyverse'
    library is also imported at the beginning of the R program. To ensure the conversions occurred in this order, the input program had to be completely
    re-written before it could be parsed and translated correctly. Admittedly the code does not always work correctly. Each of the sample programs work at least 
    sometimes, but it may take several times of running the code for it to occur. However, test_program3 appears to work correctly all of the time. Also, note 
    that white space is not important in R.

    The output for test_program1 should be:
    library(tidyverse)

    hi <- filter(hi, this > that)
    hi <- group_by(hi, clique)

    The output for test_program2 should be:
    library(tidyverse)

    hi <- filter(hi, this > that)
    hi <- filter(hi, stuff)
    hi <- group_by(hi, clique)

    The output for test_program3 should be:
    library(tidyverse)

    hi <- group_by(hi, clique)
    hi <- summarise(hi, max(stuff))

    The output for test_program4 should be:
    library(tidyverse)

    hi <- filter(hi, (this > that & i != team))
    hi <- filter(hi, stuff)

    The output for test_program5 should be:
    library(tidyverse)
    
    hi <- filter(hi, (this > that & (team > i | potato = potato)))
    hi <- filter(hi, stuff)

(3) To run my program from the terminal you need to go to the directory where the Project.py file is downloaded. Then you need to type 'python Project.py' and
    hit 'Enter'. Next, the program will prompt you for a file with a program to run - it should be noted that this program was only tested using .txt files. 
    At this point, you need to enter the full file path of the text file you want to translate and hit 'Enter'. Then the program should output the translation
    and terminate itself.  




