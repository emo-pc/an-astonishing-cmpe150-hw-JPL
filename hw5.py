import pickle
import sys
from curses.ascii import isalpha

function_type=sys.argv[1]

if function_type=="-compile":
    input_file=sys.argv[2]
    object_file=sys.argv[3]
    #adding all lines separately into a list
    with open(input_file,"r") as f:
        lines=[]
        for line in f:
            line=line.rstrip("\n")
            lines.append(line)
    #checking whether first line is correct or not
    if lines[0]!="Puroguramu o hajimeyo .":
        error_line=1
        raise Exception(f"Compile error line_no={error_line}")
    else:
        variables={
        }
        jpl_keywords=["wa","o","no","atai","de","aru","print","suru","tasu","seisu","moji-retsu","kakeru","kaikakko","tojikakko","puroguramu","hajimeyo","oware"]
        type_list=["seisu","moji-retsu"]
        #a list which includes all processes for executing
        processes=[]
        #a function which separates lines meaningful tokens
        def tokening(line,line_no):
            processed_tokens=[]
            token=""
            is_string=False
            for a in line:
                #capturing end or beginning of a string tokens
                if a=="-":
                    if is_string:
                        is_string=False
                    elif token=="":
                        is_string=True
                    token+=a
                elif a==" ":
                    # in string there may be space between characters...
                    if is_string:
                        token+=a
                    else:
                        #...but anywhere else if it results in double space it is an error...
                        if token=="":
                            raise Exception(f"Compile error line_no={line_no+1}")
                        else:
                            #...if it results in single space it is a token
                            processed_tokens.append(token)
                            token=""
                #capturing non_string types
                else:
                    token+=a
            #adding the last token
            if token:
                processed_tokens.append(token)
            return processed_tokens
        #a function which returns type of  token
        def token_type(token1,line_no):
            #capturin string
            if token1.startswith("-") and token1.endswith("-") and "-" not in token1[1:-1] and len(token1)-2<10000:
                return "string"
            #checking whether it is a variable,if it is returning its type from dict
            elif token1.lower() in variables:
                return variables[token1.lower()][0]
            #capturing integer
            elif all(k.isdigit() for k in token1.replace(",","")):
                token_comma=token1.replace(",","")
                #checking some compile rules
                if len(token_comma)>10:
                    raise Exception(f"Compile error line_no={line_no+1}")
                elif len(token_comma)>1 and token1.startswith("0"):
                    raise Exception(f"Compile error line_no={line_no+1}")
                #checking the comma situations
                elif "," in token1:
                    if len(token_comma) < 5:
                        raise Exception(f"Compile error line_no={line_no + 1}")
                    elif token1.startswith(",") or token1.endswith(","):
                        raise Exception(f"Compile error line_no{line_no + 1}")
                    #looking for whether all commas are in the right place
                    else:
                        remainder=len(token_comma)%4
                        complete=len(token_comma)-remainder
                        if remainder>0:
                            a=remainder
                            sub_comma=token_comma[0:remainder]
                        else:
                            sub_comma=token_comma[0:4]
                            a=4
                        while a<complete:
                            sub_comma=sub_comma+","
                            sub_comma=sub_comma+token_comma[a:a+4]
                            a=a+4
                        if sub_comma!=token1:
                            raise Exception(f"Compile error line_no={line_no + 1}")
                        else:
                            return "integer"
                #accepting integers doesn't have comma
                elif "," not in token1 and len(token1)<5:
                    return "integer"
            else:
                raise Exception(f"Compile error line_no={line_no + 1}")
        #a function which decides the type of  process' result and checks for compatibility of tokens
        def check_doability(process,type_l,type_r,line_no):
            if process=="tasu":
                if type_l=="integer" and type_r=="integer":
                    return "integer"
                elif type_l=="string" and type_r=="string":
                    return "string"
                else:
                    raise Exception(f"Compile error line_no={line_no + 1}")
            elif process=="kakeru":
                if type_l=="integer" and type_r=="integer":
                    return "integer"
                elif type_l=="integer" and type_r=="string":
                    return "string"
                else:
                    raise Exception(f"Compile error line_no={line_no + 1}")
            else:
                raise Exception(f"Compile error line_no={line_no+1}")
        #a function which operates all processes of an operation on tokens
        def processing(process,tokens1,line_no):
            #sustaining the function till there is no process token of an operation
            while process in tokens1:
                process_index=0
                #capturing the index of operation token
                for a in range(len(tokens1)-1,-1,-1):
                    if tokens1[a]==process:
                        process_index=a
                        break
                #an exception which results in compile error
                if process_index<=0 or process_index>=len(tokens1)-1:
                    raise Exception(f"Compile error line_no={line_no + 1}")
                #finding the type of tokens which are operated
                left_type=token_type(tokens1[process_index-1],line_no)
                right_type=token_type(tokens1[process_index+1],line_no)
                #finding the type of result by using check_doability function
                final_type=check_doability(process,left_type,right_type,line_no)
                #making up a name for operation's result in order to provide sustainability
                resultant_token=f"{left_type}_{process}_{right_type}_{line_no}_{process_index}"
                variables[resultant_token]=[final_type]
                #changing the token list with appropriate changes
                tokens1=tokens1[:process_index-1] + [resultant_token] + tokens1[process_index+2:]
            return tokens1
        #a function which operates first kakeru then tasu on a token list since kakeru has precedence
        def processing_expression(tokens2,line_no):
            tokens2=processing("kakeru",tokens2,line_no)
            tokens2=processing("tasu",tokens2,line_no)
            #although there are no more operations left on the list ,if there is more than one token it is an error
            if len(tokens2)!=1:
                raise Exception(f"Compile error line_no={line_no + 1}")
            #returning the type of the expressions' result
            resultant_type=token_type(tokens2[0],line_no)
            return resultant_type
        #a function which finds proper parentheses and compiles the type of the expression inside the parentheses
        def kaikakko_tojikakko(tokens3,line_no):
            a=0
            b=True
            while b:
                closed_parentheses=False
                for c in range(a,len(tokens3)):
                    #after finding a proper parentheses we have to break the for loop since we are changing the token list below
                    if closed_parentheses==True:
                        break
                    if tokens3[c]=="kaikakko":
                        kaikakko_index=c
                        for d in range(c+1,len(tokens3)):
                            #handling the expression inside the parentheses
                            if tokens3[d]=="tojikakko":
                                tojikakko_index=d
                                #making up a name and adding it to dict in order to provide sustainability
                                name=f"kaikakko_{kaikakko_index}_tojikakko_{tojikakko_index}_{line_no}"
                                #a list which includes tokens between the parentheses(kaikakko.......tojikakko)
                                subexpression=tokens3[kaikakko_index+1:tojikakko_index]
                                subexpression_type=processing_expression(subexpression,line_no)
                                variables[name]=[subexpression_type]
                                #changing the list
                                tokens3=tokens3[:kaikakko_index]+[name]+tokens3[tojikakko_index+1:]
                                #setting new beginning the right of tojikakko
                                a=kaikakko_index+1
                                #requried in order to break loop
                                closed_parentheses=True
                                break
                        #if there is just kaikakko without tojikakko,ERROR-(kaikakko........)
                        else:
                            raise Exception(f"Compile error line_no={line_no+1}")
                    #if there is a tojikakko without kaikakko,ERROR-(........tojikakko)
                    elif tokens3[c]=="tojikakko":
                        raise Exception(f"Compile error line_no={line_no+1}")
                    #if there is no error or parentheses we should keep going on
                    else:
                        continue
                #if there is no kaikakko-tojikakko anymore,breaking the while loop and returning the processed tokens
                else:
                    b=False
            return tokens3
        #checking all lines single by single
        for k in range(1,len(lines)-1):
            line=lines[k]
            #if there is space at the end,ERROR
            if line!=line.rstrip():
                raise Exception(f"Compile error line_no={k+1}")
            tokens=tokening(line,k)
            #there can be no empty line,ERROR
            if len(tokens)==0:
                raise Exception(f"Compile error line_no={k+1}")
            #there have to be dot at the end
            if tokens[-1]!=".":
                raise Exception(f"Compile error line_no={k+1}")
            #capturing declaring a variable
            if len(tokens)==6 and tokens[1]=="wa" and tokens[3]=="de" and tokens[4]=="aru":
                type_=tokens[2]
                var_=tokens[0]
                #variables are case-insensitive
                var_=var_.lower()
                #there are just two types seisu and moji-retsu,else ERROR
                if type_ not in type_list:
                    raise Exception(f"Compile error line_no={k+1}")
                #checking for variable rules
                if len(var_)>10 or var_.isalpha()==False or var_.isascii()==False or var_ in variables or var_ in jpl_keywords:
                    raise Exception(f"Compile error line_no={k+1}")
                #adding type of variable to dict
                if type_=="seisu":
                    variables[var_]=["integer"]
                elif type_=="moji-retsu":
                    variables[var_]=["string"]
                #adding process to list which we will need at the execution step
                processes.append(("variable",var_,type_,k+1))
            #capturing assignment
            elif len(tokens) >= 7 and tokens[1] == "no" and tokens[2] == "atai" and tokens[3] == "wa" and tokens[-2] == "aru" and tokens[-3] == "de":
                var_=tokens[0]
                var_=var_.lower()
                #if there is no variable to assign,ERROR
                if var_ not in variables or var_ in jpl_keywords:
                    raise Exception(f"Compile error line_no={k+1}")
                var_type=variables[var_][0]
                expression_tokens = tokens[4:len(tokens) - 3]
                #making a copy of expression tokens for processes list
                expression_tokens1=expression_tokens[:]
                #handling parentheses in the expression
                expression_tokens1=kaikakko_tojikakko(expression_tokens1,k)
                #concluding to type of expression
                expression_type=processing_expression(expression_tokens1,k)
                #checking the compatibility of variable and expression types
                if variables[var_][0]!=expression_type:
                    raise Exception(f"Compile error line_no={k+1}")
                #adding process to list which we will need at the execution step
                processes.append(("assign",var_,expression_tokens,k+1))
            #capturing the print
            elif len(tokens)>=5 and tokens[-4]=="o" and tokens[-3]=="print" and tokens[-2]=="suru":
                expression_tokens=tokens[:-4]
                # making a copy of expression tokens for processes list
                expression_tokens1=expression_tokens[:]
                # handling parentheses in the expression
                expression_tokens1=kaikakko_tojikakko(expression_tokens1,k)
                # concluding to type of expression
                expression_type=processing_expression(expression_tokens1,k)
                # adding process to list which we will need at the execution step
                processes.append(("print",expression_tokens,k+1))
            #if there is something else on the line,ERROR
            else:
                raise Exception(f"Compile error line_no={k+1}")
        #checking whether the last line is correct
        else:
            if lines[-1]!="Puroguramu o oware .":
                error_line=len(lines)
                raise Exception(f"Compile error line_no={error_line}")
            else:
                # if there is no compile error creating the object file
                with open(object_file, "wb") as j:
                    pickle.dump(processes, j)

elif function_type=="-execute":
    object_file=sys.argv[2]
    output_file=sys.argv[3]
    with open(output_file,"w") as l:
        pass
    #reading the object file
    with open(object_file,"rb") as g:
        program_data_copy=pickle.load(g)
    processes_copy=program_data_copy[:]
    variables={
    }
    #a function which categorizes tokens and returns a list including token's python version
    def run_tokens(tokens):
        runned_tokens=[]
        for token in tokens:
            if token in ["tasu", "kakeru", "kaikakko", "tojikakko"]:
                runned_tokens.append(token)
            elif token.lower() in variables:
                runned_tokens.append(variables[token.lower()])
            #if a token is a string removing the "-"
            elif token.startswith("-") and token.endswith("-"):
                runned_tokens.append(token[1:-1])
            #if a token is an integer removing commas and turning token into int since it is string right now
            else:
                runned_tokens.append(int(token.replace(",","")))
        return runned_tokens
    #a function which runs an operation
    def run_process(process,token_l,token_r,line_no):
        result=None
        #kakeru--->multiplication
        if process=="kakeru":
            result=token_r*token_l
            #checking for runtime error
            if type(result)==str:
                if len(result)>10000:
                    raise Exception(f"Runtime error line_no={line_no}")
            elif type(result)==int:
                if len(str(result))>10:
                    raise Exception(f"Runtime error line_no={line_no}")
        #tasu--->adding
        elif process=="tasu":
            result=token_l+token_r
            if type(result)==str:
                #checking for runtime error
                if len(result)>10000:
                    raise Exception(f"Runtime error line_no={line_no}")
            elif type(result)==int:
                if len(str(result))>10:
                    raise Exception(f"Runtime error line_no={line_no}")
        return result
    #a function which runs all processes of an operation in token list
    def run_expression(process,tokens1,line_no):
        #function should keep going till there is no process of an operation
        while process in tokens1:
            #capturing the index of an operation
            process_index=0
            for a in range(len(tokens1) - 1, -1, -1):
                if tokens1[a] == process:
                    process_index = a
                    break
            #calculating the result of a process and replacing it with the process
            left_token=tokens1[process_index-1]
            right_token=tokens1[process_index+1]
            final_token=run_process(process,left_token,right_token,line_no)
            tokens1=tokens1[:process_index-1]+[final_token]+tokens1[process_index+2:]
        return tokens1
    #a function which handles expressions in the parentheses(kaikakko......tojikakko)
    def run_kaikakko_tojikakko(tokens2,line_no):
        #function should contunie till there is no parentheses
        while "kaikakko" in tokens2:
            #capturing the list of tokens inside parentheses
            kaikakko_index=tokens2.index("kaikakko")
            tojikakko_index=tokens2.index("tojikakko")
            kai_toji_list=tokens2[kaikakko_index+1:tojikakko_index]
            #first running kakeru then tasu processes since kakeru has precedence
            kai_toji_list=run_expression("kakeru",kai_toji_list,line_no)
            kai_toji_list=run_expression("tasu",kai_toji_list,line_no)
            #replacing the expression in the parentheses with the result of the expression
            kai_toji_result=kai_toji_list[0]
            tokens2=tokens2[:kaikakko_index]+[kai_toji_result]+tokens2[tojikakko_index+1:]
        return tokens2
    #running all processes
    for tuple in processes_copy:
        #capturing the process and line no
        process=tuple[0]
        line_no=tuple[-1]
        if process=="variable":
            var_name=tuple[1]
            type_=tuple[2]
            #adding variable to dict
            if type_=="seisu":
                variables[var_name]=0
            else:
                variables[var_name]=""
        elif process=="assign":
            var_name=tuple[1]
            expression_tokens=tuple[2]
            #processing the expression and concluding to the result
            expression_tokens=run_tokens(expression_tokens)
            expression_tokens=run_kaikakko_tojikakko(expression_tokens,line_no)
            expression_tokens=run_expression("kakeru",expression_tokens,line_no)
            expression_result_list=run_expression("tasu",expression_tokens,line_no)
            expression_result=expression_result_list[0]
            #adding the result opposite of the variable name in dict
            variables[var_name]=expression_result
        elif process=="print":
            #processing the expression and concluding to the result
            expression_tokens=tuple[1]
            expression_tokens = run_tokens(expression_tokens)
            expression_tokens = run_kaikakko_tojikakko(expression_tokens, line_no)
            expression_tokens = run_expression("kakeru", expression_tokens, line_no)
            expression_result_list = run_expression("tasu", expression_tokens, line_no)
            expression_result = expression_result_list[0]
            #if type of the result is int turning it into a string and add commas to the proper places
            if type(expression_result)==int:
                expression_result=str(expression_result)
                #if the integer has more than 4 digits adding commas
                if len(expression_result)>4:
                    remainder=len(expression_result)%4
                    complete=len(expression_result)-remainder
                    if remainder==0:
                        a=4
                        sub_comma=expression_result[:4]
                    else:
                        a=remainder
                        sub_comma=expression_result[:remainder]
                    while a<complete:
                        sub_comma = sub_comma + ","
                        sub_comma = sub_comma + expression_result[a:a + 4]
                        a = a + 4
                    expression_result=sub_comma
            #if type of the result is string adding "-" to the beginning and end
            else:
                expression_result="-"+expression_result+"-"


            #since the process is print, printing result to output
            with open(output_file,"a") as y:
                y.write(expression_result+"\n")














