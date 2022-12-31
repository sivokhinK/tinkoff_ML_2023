import numpy as np
import argparse

def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='location of input file')
    parser.add_argument('output', help='location of output file')
    args = parser.parse_args()
    return args


def normalize(s: str) -> str:
    return s.replace(' ', '').replace('\n', '').lower()


def levenshtein_distance(s1: str, s2: str) -> float:

    # add spaces at the start of the strings
    s1 = ' ' + s1
    s2 = ' ' + s2

    # initialize distance array with zeroes
    dist = np.zeros((len(s1), len(s2)), dtype=int)

    # fill first column and first row in dist
    for i in range(1, len(s1)):
        dist[i, 0] = i
    
    for j in range(1, len(s2)):
        dist[0, j] = j

    for i in range(1, len(s1)):
        for j in range(1, len(s2)):
            if s1[i] == s2[j]:
                subst_cost = 0
            else:
                subst_cost = 1
            
            dist[i, j] = min(
                dist[i-1, j] + 1,
                dist[i, j-1] + 1,
                dist[i-1, j-1] + subst_cost
            )

    # uncomment to print distance matrix
    #print(dist, '\n')

    return abs(dist[len(s1)-1, len(s2)-1] / len(s1)-1)


if __name__ == '__main__':

    # read program arguments
    args = init_argparse()

    # clear output file
    with open(args.output,'a+') as f:
        f.truncate(0)

    with open(args.input, 'r') as f:

        file_names = f.readline().split()

        while file_names:
            
            print('COMPARING', file_names[0], 'TO', file_names[1])

            with open(file_names[0], 'r') as file1:
                string1 = normalize(file1.read())

            with open(file_names[1], 'r') as file2:
                string2 = normalize(file2.read())

            score = round(levenshtein_distance(string1, string2), 2)
            print('Score:', score, '\n')

            with open(args.output, 'a') as out:
                out.write(str(score) + '\n')

            # update
            file_names = f.readline().split()
            
