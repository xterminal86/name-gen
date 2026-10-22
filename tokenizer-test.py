import argparse;
import json;

from util import Tokenize, WeightedRandom;

################################################################################

def main():
  parser = argparse.ArgumentParser();

  parser.add_argument("--file",
                      type=str,
                      help="Text corpus for training (word per line)");

  args = parser.parse_args();

  names = [];

  trie = {};

  if args.file:
    try:
      with open(args.file) as f:
        names = f.readlines();
    except Exception as e:
      print(e);
      exit(1);
  else:
    try:
      with open("model.json", "r") as f:
        trie = json.load(f);
    except Exception as e:
      print(e);
      exit(1);

  maxLen = 0;

  if names:
    maxLen = len(max(names, key=len));

  tokenizedNames = {};

  for name in names:
    stripped = name.strip();
    tokens = Tokenize(stripped);
    ln = len(stripped);
    #spaces = " " * (maxLen - ln);
    #print(f"{ stripped }{ spaces } -> { tokens }");
    tokenizedNames[stripped] = tokens;

  trieHead = trie;

  occurenceKey = "42";

  if not trie:
    for _,tokens in tokenizedNames.items():
      for token in tokens:
        if token not in trieHead.keys():
          trieHead[token] = { occurenceKey : 1 };
          trieHead = trieHead[token];
        else:
          trieHead[token][occurenceKey] += 1;
          trieHead = trieHead[token];
      trieHead = trie;

    with open("model.json", "w") as f:
      json.dump(trie, f);

  wbt = {};

  output = [];

  for k,v in trie.items():
    wbt[k] = v[occurenceKey];

  start = WeightedRandom(wbt);

  output.append(start);

  head = trie[start];

  while True:
    if not head:
      break;

    wbt = {};

    for k,v in head.items():
      if k == occurenceKey:
        continue;

      wbt[k] = v[occurenceKey];

    if not wbt:
      break;

    next = WeightedRandom(wbt);

    output.append(next);

    head = head[next];

  print("".join(output).capitalize());

################################################################################

if __name__ == "__main__":
  main();

