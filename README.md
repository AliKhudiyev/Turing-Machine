# Turing Machine

A small coding challenge from a live stream about a revolutionary idea of Alan Turing. For more details about the Turing machine, visit [this link](https://en.wikipedia.org/wiki/Turing_machine).

## Compiler

There is a simple compiler to compile and run the Turing machine compatible programs. The compiler is named *tmac.py* and it is capable of running the programs which has strict typing rules.

You can use it as below:

```bash
python tmac.py -i <program> (-s <speed> --visual)
```

or (if you have anaconda installed)

```bash
path/to/tmac.py -i <program> (-s <speed> --visual)
```

### Program syntax

The program first has to contain the elements of the formal definition of Turing machine given in [this link](https://en.wikipedia.org/wiki/Turing_machine). The order matters, so, each element or parameter has to respect the order given in the link above. After setting up all the parameters(except transitions), you can define one or more transitions with the following syntax:
**Q, S -> S', M, Q'**

*Q - current state, S - current tape symbol, S' - tape symbol to be written, M - tape motion({L, R}; either Left or Right) and Q' - new state.*

Each transition has to be defined in a separate line and there is no way to write comments. Blank lines between transitions are ignored by the program, so, you can put additional blank lines to make your code look readable.

## Examples

- [Language detection](https://github.com/AliKhudiyev/Turing-Machine/tree/main/examples/language)
- [Symbol shifting](https://github.com/AliKhudiyev/Turing-Machine/tree/main/examples/shift)
- [Palindrome checking](https://github.com/AliKhudiyev/Turing-Machine/tree/main/examples/palindrome)
- [Binary addition](https://github.com/AliKhudiyev/Turing-Machine/tree/main/examples/binary-addition)
