# Closure thoughts
I was doing some thinking about closures and mutable state, and decided to write down my thoughts on the matter - code and documentation are available in main.py.

## Background
### What is a closure?
A closure is a function that references some external state. It "closes" over the state, so that is available where the function is called.

### Why is this useful?
Let's say you have a function that takes another function that takes an int (in pseudocode):

int function1(function<int> f):
    return f(1) + 2 // x is 1

innerFunction = x -> return x + 1

function1(innerFunction)
// return (x + 1) + 2 where x = 1
// return (1 + 1) + 2
// return 4

A closure might be useful here if we have some state we need to reference in f for the purposes of calculating f's result but we can't pass in that state because:
a) f when in function1 must take an int (as per the type signature)
b) function1 may not have access to that state

### So how do we make a closure?

We need a function that returns another function, and for the returned function to reference some state in the outer function (these could be calculated or parameters, it doesn't make a difference - but we will see a difference when the state is mutable):

function<int> closureCreator(int outerState1, int outerState2, int outerState3):
    return (int x) -> return outerState1 + outerState2 - outerState3 + x

function<int> myClosure = closureCreator(10, 9, 8)
myClosure(7) // return 10 + 9 - 8 + 7 --> 18

Notice that myClosure only takes 1 argument but references 10, 9, and 8 that we passed in earlier.
Now the hard part's over, we can use myClosure in other functions:

function1(myClosure) // (10 + 9 - 8 + 1) + 2 --> 14