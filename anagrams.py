# Given an array of strings, group anagrams together.
# Input: ["eat", "tea", "tan", "ate", "nat", "bat"]
# Output:[["ate","eat","tea"], ["nat","tan"],["bat"]]

def groupAnagrams(strs): strs -> List str
  def convert(s):
    temp = [0] * 26
    for char in s:
      temp[ord(char) - ord("a")] += 1
    return tuple(temp)
  res = []
  dic = {}
  for s in strs:
    t = convert(s)
    if t in dic:
      res[dic[t]].append(s)
    else:
      res.append([s])
      res[t] = len(res) - 1
  return res
  
  
