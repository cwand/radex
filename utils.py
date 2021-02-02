
# Choose an option from a list of items using keyboard input
# Example:
# >>> options = ['A','B','C']
# >>> x = listChoose("Some text","Choice: ",options)
# Some text
#   [1] A
#   [2] B
#   [3] C
# Choice: 3   # 3 was input by the user
# >>> print(x)
# 2
# >>> print(options[x])
# C

def list_choose(descText, quest, options):

    print(descText)

    for key, option in enumerate(options, 1):
        print('  [' + str(key) + ']  ' + str(option))

    selKey = -1
    while (selKey < 0 or selKey >= len(options)):
       selKey = int(input(quest + " ")) - 1

    return selKey
