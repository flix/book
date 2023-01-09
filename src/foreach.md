# ForEach

> **Note:** This documentation is relevant for Flix version 0.35.0 or higher.

Flix supports a traditional _foreach_ construct that enables imperative
iteration through collections. 

We typically use the _foreach_ construct when we want to iterate through a
collection and execute an effectful operation for each element.

For example, the program:

```flix
def main(): Unit \ IO = 
    let fruits = List#{"Apple", "Pear", "Mango"};
    foreach(fruit <- fruits) 
        println(fruit)
```

Prints the fruits `Apple`, `Pear`, and `Mango`.

We can also iterate through multiple collections:

```flix
def main(): Unit \ IO = 
    let fruits = List#{"Apple", "Pear", "Mango"};
    let creams = List#{"Vanilla", "Stracciatella"};
    foreach(fruit <- fruits) 
        foreach(cream <- creams)
            println("Would you like some ${fruit} with ${cream} icecream?")
```

The same loop can also be written:

```flix
def main(): Unit \ IO = 
    let fruits = List#{"Apple", "Pear", "Mango"};
    let creams = List#{"Vanilla", "Stracciatella"};
    foreach(fruit <- fruits; cream <- creams) 
        println("Would you like some ${fruit} with ${cream} icecream?")
```



<!--
- Filtering
- Iterable/Foldable construct?
- Braces
- Return type
-->

