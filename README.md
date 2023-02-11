# Seminar-Datenkompression-2022

For High-Quality animations use **-pqh** instead of **-pql**. Note that this will drastically increase the compiling time.

# Execute encoding.py
1. python module **manim** needs to be installed and executable from terminal
2. open terminal in .\Seminar-Datenkompression-2022\python
3. execute **manim -pql -v critical encoding.py**
4. when prompted, write desired string to be encoded
5. wait for the animation to be created

#### Example
````
> main -pql -v critical encoding.py
> to encode: Hello
````

# Execute decoding.py
1. python module **manim** needs to be installed and executable from terminal
2. open terminal in .\Seminar-Datenkompression-2022\python
3. execute **manim -pql -v critical decoding.py**
4. when prompted, write encoded binary string (e.g. 0.1001011)
5. when prompted, write occurrences like a python dictionary (e.g {"H": 1, "e": 1, "l": 2, "o": 1})
6. wait for the animation to be created

#### Example
```
> main -pql -v critical decoding.py
> to decode: 0.000100011
> occurrences: {"e":1, "l":2, "H": 1, "o": 1}
````
# Execute Datenkompression.html
1. open one of the three html files in the HTML folder
2. switch to the Datenkompression one through the navigation bar
3. fill the upper textfield with your input string (using UTF-8 Symbols)
4. use either the "naives-" or "genaus-" "Kompressionsverfahren" button to encode your input
5. (optional) clear input field
6. use the corresponding "Dekompressionsverfahren" button to decode your message from the lower field