'''
This is a fun little discussion of closures and mutable state
The file is meant to be read from top to bottom, and may be executed, as is
'''


'''
I was thinking about closures and mutable state and came up with a function that counts while keeping track of mutable state internally.

The goal is to print out the numbers 1 to 5 using numbers generated from a closure.

These block comments are for my commentary, and regular comments are for the code.
'''

def counter(starting):
    n = starting - 1 # We increment n in nextValueF before returning, and we want our first return to be `starting`
    def nextValueF():
         # The nonlocal keyword is for referencing vars in outer non global scope (the keyword `global` is used for global scope) 
        nonlocal n
        n = n + 1
        return n
    return nextValueF


print("Mutable 1 to 5")
# Usage
count = counter(1)
value = count()

while value <= 5:
    print(value)
    value = count()

'''
And that does the job. Value is assigned to 1 .. 5 throughout the various calls to count.
But while writing the loop I got the wrong answer three (3!) times:

My first attempt:
while count() <= 5:
    print(count())

Did not get the correct answer because of mutable state: count incremented n (the enclosed value) twice per loop.

My second attempt:
value = count()
while value <= 5:
    value = count()
    print(value)

was off by 2 because we increment before printing in combination with the last problem:

def counter(starting):
    n = starting
    def nextValueF():
        nonlocal n
        n = n + 1
        return n
    return nextValueF

> n = starting
We increment n before returning it in nextValueF, so we're off by 1.
'''

'''
We can do better than that.
Can we remove the mutable state from the function call process entirely?
Yes, by returning a function that gets us the next value!
'''

def generateChain(currentValue):
    def nextValueF():
        return generateChain(currentValue + 1)
    return (currentValue, nextValueF)

'''
I've named the function generateChain because you call it in a chain:
You call it once and get your value and function, then to get the
next value you call the function you just reveived, and so on for all
values you want.
'''

print()
print("Immutable 1 to 5")

value, getNext = generateChain(1)

while value <= 5:
    print(value)
    value, getNext = getNext()


'''
Two of the mistakes I made in the previous closure I __couldn't__ make here:
Changing mutable state by calling functions more than once (I will demonstrate that next)

Not subtracting 1 from the starting value to have the correct value on return.
This is because there is no value to change in our return, that's done on the next function call.
A trick to be wary of, however: we're working with numbers here, which are immutable, if we were working with mutable values calling the next function would result in potentially mutating the object. It depends on the operation (our operation here is +).



The bug that does apply here, and that I did not put in, is the misordering of print and getting the next value. I suspect having done it incorrectly the first time prevented me from doing it incorrectly the second but it seems more obvious (to me at least) that we should print the value before calling getNext.
'''


'''
Calling count multiple times changes the state:
(Yes I'm reusing variables, it's for readability I promise).

We also need to remember to reset the state of our counter, and while that is true for how we've used `function` I will also show that that is not strictly necessary.
'''

print()
print("count() 1 to 4")

count = counter(1)
print(count()) # 1
print(count()) # 2
print(count()) # 3
print(count()) # 4





print()
print("Chaining 1 to 4")

f1 = generateChain(0)[1] # We're keeping the functions to the next value
f2 = f1()[1]
f3 = f2()[1]
f4 = f3()[1]

print(f1()[0]) # 1
print(f2()[0]) # 2
print(f3()[0]) # 3
print(f4()[0]) # 4

'''
And the already used values are still available:
'''
print("And reusing items:")

print(f1()[0]) # 1
print(f1()[0]) # 1
print(f1()[0]) # 1
print(f1()[0]) # 1

'''
The syntax is a little ugly I'll admit. One could add a function to remove the need to use the syntax directy though:
'''

def value(t):
    return t[0]

def nxt(t):
    return t[1]

'''
The main benefit for this (apart from removing mutable state, if you believe that's a benefit) is you get to easily keep old results AND the path to the next result.
This is true even if you leave out results in your storage, you can always chain the functions to get to later values!
'''

print()
print("Saving the results")

results = []
r = generateChain(1)

while value(r) <= 4:
    results.append(r)
    r = nxt(r)()

print("Values:")
print(list(map(value, results)))

print("Functions (not that printing functions makes a lot of sense):")
print(list(map(nxt, results)))
