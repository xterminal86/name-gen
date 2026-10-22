import argparse;

def main():
  parser = argparse.ArgumentParser();

  parser.add_argument("NAME", type=str);

  args = parser.parse_args();

  vowels     = "aeiouy";
  consonants = "bcdfghjklmnpqrstvwxz";

  name = args.NAME.lower();

  vowsCount = 0;
  consCount = 0;

  vowelGroups = [];

  ln = len(name);

  for i in range(ln):
    letter = name[i];

    if letter in vowels:
      vowelGroups.append(i);

  #print(f"Vowel groups: { vowelGroups }");

  ln = len(vowelGroups);

  splitPositions = [];

  for i in range(ln):
    if i + 1 >= ln:
      break;

    currentGroup = vowelGroups[i];
    nextGroup    = vowelGroups[i + 1];

    #print(f"  cg { currentGroup } ng { nextGroup }");

    cc = 0;

    for j in range(currentGroup, nextGroup, 1):
      letter = name[j];

      #print(f"  letter: { letter }");

      if letter in consonants:
        cc += 1;

    #print(f"  cc { cc }");

    if (cc == 1):
      splitPositions.append(currentGroup);
    elif (cc == 2):
      splitPositions.append(currentGroup + 1);
    elif (cc > 2):
      if (cc % 2 == 0):
        splitPositions.append(currentGroup + 2);
      else:
        splitPositions.append(currentGroup + 1);

  #if not splitPositions and vowelGroups:
  #  splitPositions.append(vowelGroups[0]);

  #print(splitPositions);

  tokens = [];

  part = [];

  lastSplitPos = -1;

  ln = len(name);
  for i in range(ln):
    part.append(name[i]);
    if i in splitPositions:
      tokens.append("".join(part));
      part = [];
      lastSplitPos = i;

  if lastSplitPos < ln:
    tokens.append(name[(lastSplitPos + 1):]);

  print(f"{ args.NAME } -> { tokens }");

if __name__ == "__main__":
  main();
