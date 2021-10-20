from datetime import date


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


def list_yn(descText, quest):

  print(descText)

  selKey = ""
  while not (selKey.casefold() == "j".casefold() or selKey.casefold() == "n".casefold()):
    selKey = input(quest + " (J/N)  ")

  return (selKey == "j" or selKey == "J")


# Convert a string with format "yyyymmdd" to a python date object
def yyyymmdd2date(date_string):
  # Convert to iso format
  isostring = date_string[0:4] + '-' + date_string[4:6] + '-' + date_string[6:]
  return date.fromisoformat(isostring)
