#Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent.
#A mapping of digit to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.
#eg. Input: "23"
#eg. Output: ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].

def phoneNumber(digit):
  if not digit:
    return []
  dic = {"2":"abc", "3":"def", "4":"ghi", "5":"jkl", "6":"mno", "7":"pqrs", "8":"tuv", "9":"wxyz"}
  res = []
  combination = ""
  DFS(digit, dic, res, combination, 0)
  return res

def DFS(digit, dic, res, combination, index):
  if len(combination) == len(digit):
    res.append(path[:])
    return
  
  for i in range(index, len(digit)):
    for j in dic[digit[i]]:
      DFS(digit, dic, res, combination + j, i+1)
  
  
  
  
  
