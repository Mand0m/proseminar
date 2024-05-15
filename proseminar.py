from z3 import *
import random
import string

# assume a string input of length 1 to 20
def cases(input : str):
    if (len(input) < 4):
        return 1
    elif("RWTH" in input):
        if (input.find("RWTH") == 0):
            return 2
        else:
            return 3
    else:
        return 4

# generate i random strings of length 1 to 20 (8 in the presentation)
def random_test(i: int):
    res = []
    characters = string.ascii_letters + string.digits + string.punctuation
    for x in range(i):
        res.append(''.join(random.choices(characters, k=random.randint(1, 20))))
    return res

# define z3 input variable
input = String('input')
# define path constraints, where a single constraint symbolizes an if/elif statement without
# more nested constraints; a tuple represents an if/elif path + a list of nested ite branches
# (recursive definition) and True stands for the else branch
constraints = [Length(input) < 4,(Contains(input, "RWTH"),[IndexOf(input, "RWTH") == 0, True]), True]

# returns a list with i test values per branch (2 in the presentation)
def symbolic_test(constraints: list, i: int):
    s = Solver()
    return help_symbolic_test(s, constraints, i)


def help_symbolic_test(s: z3.Solver, constraints: list, i: int):
    res = []
    for constraint in constraints:
        # calcutating values for the constraint and adding the negation
        # for the rest of the ite block
        if isinstance(constraint, z3.BoolRef):
            s.push()
            s.add(constraint)
            res = res + generate_cases(s, i)
            s.pop()
            s.add(Not(constraint))
        # adding the constraint and recursively calling the method for the nested constraints
        elif isinstance(constraint, tuple):
            s.push()
            s.add(constraint[0])
            res = res + help_symbolic_test(s, constraint[1], i)
            s.pop()
            s.add(Not(constraint[0]))
        else:
            res = res + generate_cases(s, i)
    return res

def generate_cases(s:z3.Solver, i: int):
    res = []
    s.push()
    for x in range(i):
        if (s.check() == sat):
            # adding the test case t to the list and adding input != t 
            # to the solver so it doesnt generate the same case again
            res.append(s.model().eval(input).as_string())
            s.add(input != s.model().eval(input).as_string())
        else:
            res.append(None)
    s.pop()
    return res

# applying cases to all arguments of a list
def apply_cases(strings: list):
    for i in range(len(strings)):
        strings[i] = cases(strings[i])
    print(strings)


#remove
'''Das wär das Beispiel für 4.2.2 in der Ausarbeitung / im Vortrag, wo wir jeweils 8
   Test Inputs generieren und dann zeigen, wie der Dynamic Symbolic Test viel
   bessere Inputs liefert und alle Pfade unseres Programm erkundet. Wir würden
   in der Präsentation das ganze nach aktuellem Stand im interaktiven Python Modus
   demonstrieren, während wir in der Präsentation den aktuellen Code und ein Bild
   vom Solver Stack zeigen würden.'''
if __name__ == "__main__":
    r = random_test(8)
    print(r)
    print(apply_cases(r))
    s = symbolic_test(constraints, 2)
    print(s)
    apply_cases(s)

#remove
'''das Programm für 4.2.1, an dem wir formale Verifikation zeigen wollen. Wir möchten die 
Terminierung der Schleife zeigen, indem wir beweisen, dass das Intervall echt kleiner wird
bzw. wir zeigen auch, wie die Methode prove() Gegenbeispiele zu unserer Annahme der Terminierung
zeigt und wodurch man "iterativ" seinen Code analysieren und debuggen kann. Die Kommentare mit
später würden auf den Teil verweisen, den man durch die Analyse z.B. während dem Vortrag ändern würde.
Das Beispiel ist ebenfalls vom Paper: Applications of SMT solvers to Program Verification aus Abschnitt
1.6. inspiriert'''
def binarySearch(a: list, key: int):
    l = 0
    r = len(a) - 1
    while l < r:
        mid = (l + r) / 2
        if key < a[mid]:
            r = mid
        elif a[mid] < key:
            l = mid # spaeter hier l = mid + 1
        else:
            return mid
    return None

def checkTerm():
    l, r, mid = Ints('l r mid')
    preConditions = [0 <= l, l <= r, mid == (r + l) / 2]
    postConditions = [Or(mid - l < r - l, r - mid < r - l)] # spaeter hier r - (mid + 1)
    prove(Implies(And(preConditions), And(postConditions)))

checkTerm()
