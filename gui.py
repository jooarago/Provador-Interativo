from os import popen
from pyswip import Prolog
from pyswip import Functor
from tkinter import *
from tkinter import messagebox

prolog = Prolog()
prolog.consult("provador.pl")

#FUNÇÕES PARA FORMATAÇÃO
def format_value(value):
    output = ""
    if isinstance(value, list):
        output = "[ " + ", ".join([format_value(val) for val in value]) + " ]"
    elif isinstance(value, Functor) and value.arity == 2:
        output = "{0}{1}{2}".format(value.args[0], value.name, value.args[1])
    else:
        output = "{}".format(value)

    return output

def format_result(result):
    result = list(result)

    if len(result) == 0:
        return "false."

    if len(result) == 1 and len(result[0]) == 0:
        return "true."

    output = ""
    for res in result:
        tmpOutput = []
        for var in res:
            tmpOutput.append(var + " = " + format_value(res[var]))
        output += ", ".join(tmpOutput) + " ;\n"
    output = output[:-3] + " ."

    return output

#ACESSANDO O PROVADOR
prolog = Prolog()
prolog.consult("provador.pl")



#     CÓDIGO PRINCIPAL
root = Tk()
root.title("Sat Interactive Prover")

#entrada
e = Entry(root, width=35, borderwidth=5)

e.grid(row=0, column=0)

#MOSTRA A LINHA DE DEDUCAO DA ENTRADA QUANDO CLICADO
def button1click():
    global pop 
    pop = Toplevel(root)
    pop.geometry("250x150")
    pop.title("Satisfatibilidade de "+e.get())

    list(prolog.query("reiniciar()"))
    list(prolog.query("translate("+e.get()+")"))
    list(prolog.query("resolucao()"))

    #DIZER SE A FÓRMULA É SATISFATÍVEL OU NÃO
    i = prolog.query("clause([])")
    if(format_result(i)=="true."):
        label = Label(pop, text=e.get()+" é insatisfatível, pois do conjunto de premissas foi deduzida a cláusula vazia.")
        label.grid()
    else:
        label = Label(pop, text=e.get()+" é satisfatível, pois do conjunto de premissas não foi deduzida a cláusula vazia.")
        label.grid()


    #MOSTRAR PREMISSAS
    for i in prolog.query("clause(R), not(res(_,_,R)), clausenum(R, NumR)"):
        label = Label(pop, text=format_value(i['NumR'])+" "+format_value(i['R'])+" PREMISSA")
        label.grid()
    
    #MOSTRAR O RESTO DA DEDUCAO
    for i in prolog.query("clause(R), res(X,Y,R), clausenum(X, NumX), clausenum(Y, NumY), clausenum(R, NumR)"):
        
        string = format_value(i['NumR'])+" "+format_value(i['R'])+' RES '+format_value(i['NumX'])+' '+format_value(i['NumY'])
        
        label = Label(pop, text=string)
        label.grid()
   
button1 = Button(root, text="Checar satisfatibilidade", command=button1click)

button1.grid()

root.mainloop()