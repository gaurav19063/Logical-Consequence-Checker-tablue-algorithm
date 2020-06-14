def checkBranches(value,operator): #To check for a perticular operator on a perticulat T/F how many branches should be there and what value of left operand and right operand will take
    if(operator=='+'):
        if (value=='F'):
            return 1 ,'FF'
        else:
            return 2,'TT'
    elif(operator=='.'):
        if (value=='T'):
            return 1,'TT'
        else:
            return 2,'FF'
    elif (operator == '*'):
        if (value == 'T'):
            return 2,'FT'
        else:
            return 1,'TF'
    elif (operator == '='):
        if (value == 'T'):
            return 2,'00'
        else:
            return 2,'00'
def Tablue(expression_stack,l,t):     #Tablue call for expression

    # print("Fun ",t)
    end=True
    r=0
    for x in expression_stack:       # to check if all expression changed to operand or not
        if len(x)==5 and x[2]=='~':
            if x[0]=='T':
                expression_stack.remove(expression_stack[r])
                expression_stack.insert(0,'F'+x[3:-1])
            else:
                expression_stack.remove(expression_stack[r])
                expression_stack.insert(0, 'T' + x[3:-1])

        if(len(expression_stack[r])!=2):
            end=False
        r=r+1
    print(expression_stack)
    if end:                               # All the expression has changed to expression
        expression_stack = list(set(expression_stack))
        i=0
        for x in expression_stack:
            # r=0
            for j in range(len(expression_stack)):
                if x[1]==(expression_stack[j])[1] and x[0]!=(expression_stack[j])[0]:
                    return True        # return True if Contradiction found
        return False                    # return false in branch open
    expression=expression_stack.pop()
    expression_temp = expression[2:-1]
    flag=0
    if expression_temp[0]=='~':                    # negation handling
        expression_temp=expression_temp[2:-1]
    count = 0
    i = 0
    for x in expression_temp:
        if (x == '('):
            count = count + 1
        elif (x == ')'):
            count = count - 1
        if (count == 0):
            break

        i = i + 1
    value = expression[0]
    operation = expression_temp[i + 1]
    no_of_branches, values = checkBranches(value, operation)  # to check how many branches should be in the next step of tablue
    left_exp = expression_temp[0:i + 1]
    if (expression_temp[i + 1] == '='):
        right_exp = expression_temp[i + 3:]               #dividing the left and right expression
    else:
        right_exp = expression_temp[i + 2:]
    expression_stack_temp = expression_stack.copy()
    if (left_exp[0] == '~'):
        if values[0] == 'F':
            left_exp_final = 'T' + left_exp[1:]
        else:
            left_exp_final = 'F' + left_exp[1:]
    else:
        left_exp_final = values[0] + left_exp
    if(right_exp[0]=='~'):
        if(values[1]=='F'):
            right_exp_final='T'+right_exp[1:]
        else:
            right_exp_final='F'+right_exp[1:]
    else:
        right_exp_final=values[1]+right_exp

    if no_of_branches == 1:         #When branch no is 1 push both operands or expression into stack
        if (len(left_exp) == 1):
            m = 0
        else:
            m = len(expression_stack_temp)
        if (len(right_exp) == 1):
            n = 0
        else:
            n = len(expression_stack_temp)
        expression_stack_temp.insert(m, left_exp_final)
        expression_stack_temp.insert(n, right_exp_final)
        return Tablue(expression_stack_temp,l,t+1)

    elif no_of_branches == 2:    # When no of branches are 2 then push each operand or expression accordingly
        expression_stack_temp1 = expression_stack.copy()
        expression_stack_temp2 = expression_stack.copy()
        if (len(left_exp) == 1):
            m = 0
        else:
            m = len(expression_stack_temp1)
            # m2=len(expression_stack_temp2)
        if (len(right_exp) == 1):

            n = 0
        else:
            n = len(expression_stack_temp1)

        if (operation == '='):   # specific handling for == operator
            if(left_exp[0]=='~'):
                expression_stack_temp1.insert(m, 'F' + left_exp)
                expression_stack_temp2.insert(m, 'T' + left_exp)
            else:
                expression_stack_temp1.insert(m, 'T' + left_exp)
                expression_stack_temp2.insert(m, 'F' + left_exp)
            if (right_exp[0]=='~'):
                expression_stack_temp1.insert(n, 'T' + right_exp)
                expression_stack_temp2.insert(n, 'F' + right_exp)

            else:
                expression_stack_temp1.insert(n, 'F' + right_exp)
                expression_stack_temp2.insert(n, 'T' + right_exp)

        else:
            expression_stack_temp1.insert(m, left_exp_final)
            expression_stack_temp2.insert(n, right_exp_final)
        return Tablue(expression_stack_temp1,l,t+1) and Tablue(expression_stack_temp2,l,t+1)

def normalizeformula(formula):  #to make formula  formated
    count=0
    i=0
    for x in formula:
        if(x=='('):
            count=count+1
        elif(x==')'):
            count=count-1
        # print(count)
        if count==0:
            break
        i=i+1
    if i!=len(formula)-1:
        formula='('+formula+')'
    return formula




def find_validity(formula,consequence,l):  #main call for validiti finding
    formula=normalizeformula(formula)
    consequence=normalizeformula(consequence)
    expression_stack=[]
    if len(consequence)==1:    #giving truth value to expression and push it into stack
        expression_stack.append("F" + consequence)
        expression_stack.append("T" + formula)
    else:

        expression_stack.append("T" + formula)
        expression_stack.append("F" + consequence)
    t=0
    if(Tablue(expression_stack,l,t)):
        print("Yes")
    else:
        print("N0")
print("Please Use optimal parentheses otherwise error may occur") #for input
print ("Enter your formula :")

formula=input()
print ("Enter your consequence :")
consequence=input()
operands=[]
for x in formula:
    if x not in ['+','.','*','(',')','~']:
        operands.append(x)
find_validity(formula,consequence,len(list(set(operands))))