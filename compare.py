import ast
import numpy as np


# При сравнении текстов программ нас не интересуют комментарии, docstrings и имена перемынных,
# так как плагиатер может легко изменить их, не нарушая работу программы.
# Удалим их, оставив только нужный нам синтаксис.
def normalize_files(tree) -> str:

    for node in ast.walk(my_tree):

        # if hasattr(node, 'id'):
        #     print(node.id)
        #     node.id = 'TEST'
        #     print(node.id)

        # let's work only on functions & classes definitions
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
            continue
        
        # if not isinstance(node, ast.Module):
        #     print(node.name)
        #     node.name = ''
        #     print(node.name)

        # if node is empty - skip it
        if not len(node.body):
            continue

        if not isinstance(node.body[0], ast.Expr):
            continue

        if not hasattr(node.body[0], 'value') or not isinstance(node.body[0].value, ast.Str):
            continue

        # Uncomment lines below if you want print what and where we are removing
        #print(node)
        
        #print(node.body[0].value.s)

        node.body = node.body[1:]

        # unparsing deletes newlines and comments
    result = ast.unparse(my_tree)
    result = result.replace(' ', '').replace('\n', '')

    return result

# Done
def levenshtein_distance(s1: str, s2: str):

    # add spaces at the start of the strings
    s1 = ' ' + s1
    s2 = ' ' + s2

    # initialize distance array with zeroes
    dist = np.zeros((len(s1), len(s2)), dtype=int)

    # getting from empty string to target string is straightforward
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

    print(dist, '\n')

    return abs(dist[len(s1)-1, len(s2)-1] / len(s1)-1)


if __name__ == '__main__':

    with open('files/cars196.py', 'r') as f:
        # my_tree = ast.parse(f.read())
        # file1 = normalize_files(my_tree)
        file1 = f.read().replace(' ', '').replace('\n', '')

    with open('plagiat2/cars196.py', 'r') as f:
        # my_tree = ast.parse(f.read())
        # file2 = normalize_files(my_tree)
        file2 = f.read().replace(' ', '').replace('\n', '')
    
    score = levenshtein_distance(file1, file2)
    print(score)

    # with open('out.py', 'w') as f:
    #     f.write(result)

    #normalize_files(my_tree)

