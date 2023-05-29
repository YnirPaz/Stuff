conv = {
    '∀': 'forall',
    '∃': 'exists',
    '∈': 'in',
    '∉': 'notin',
    '∧': 'land',
    '∨': 'lor',
    '¬': 'neg',
    '⇒': 'Rightarrow',
    '⇔': 'iff',
    '≠': 'ne'
}


def main():
    print('\n' + convert(input()))


def convert(s):
    #s = filter(lambda c : c != ' ', s)
    
    tempLatex = ''
    for i in range(len(s)):
        if s[i] in conv.keys():
            tempLatex += '\\' + conv[s[i]] + ' '
        elif s[i] != ' ':
            tempLatex += s[i] + ' '
        else:
            if s[i + 1] != ')' and s[i + 1] != '∈' and s[i + 1] != '∉':
                tempLatex += ' \ \ '

    latex = ''
    for i in range(len(tempLatex)):
        if i != 0 and i != len(tempLatex) - 1 and tempLatex[i] == ' ' and (tempLatex[i - 1] == '(' or tempLatex[i + 1] == ')'):
            continue

        latex += tempLatex[i]

    
    return latex


if __name__ == '__main__':
    main()
