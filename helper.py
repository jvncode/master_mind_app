def read_file(path):
    with open(path, 'r') as file:
        return file.read()


def check_hits(code, bet):
    codeL, betL = (list(code), list(bet))
    blacks, whites = (0, 0)
    new_bet, new_code = ([], [])
    '''
    Iteration on both lists (Secret Code and Bet) to detect the matching elements in colour and index. The result will be the black tokens.
    '''
    for ix, l in enumerate(betL):
        if l == codeL[ix]:
            blacks += 1
        else:  # The respective elements that do not fulfil the condition I add them in two new lists of Secret Code(new_code) and Bet(new_bet).
            new_bet.append(l)
            new_code.append(codeL[ix])
    '''
    Set creation of the new_bet list (to avoid repeated items) and query how many items match in the new_code list.
    The result will be the white tokens.
    '''
    for nb in set(new_bet):
        whites += new_code.count(nb)

    return (blacks, whites)