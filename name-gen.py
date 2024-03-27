import random;
import argparse;
import textwrap

from enum import Enum, auto;
from util import (WeightedRandom,
                  PrefixOK,
                  DigraphsDistribution,
                  TrigraphsDistribution,
                  RemoveTripleLetters,
                  GetRank,
                  AverageRank,
                  ValidPrefixes,
                  Vowels);

################################################################################

class NameGenMode(Enum):
    DIGRAPHS  = auto()
    TRIGRAPHS = auto()
    DIGTRIG   = auto()
    TRIGDIG   = auto()

class NameGen:
  _digraphsDistribution  = {};
  _trigraphsDistribution = {};

  _averageRank = 0.0;

  _debugMode = False;

  # ----------------------------------------------------------------------------

  def __init__(self,
               digraphsDistribution : dict,
               trigraphsDistribution : dict,
               averageRank : float,
               printDistributions=False):
    self._digraphsDistribution  = digraphsDistribution;
    self._trigraphsDistribution = trigraphsDistribution;

    self._averageRank = averageRank;

    if printDistributions:
      self._debugMode = True;

      print("Digraphs distribution:\n");
      print(self._digraphsDistribution);

      print();
      print("-"*80);

      print("Triigraphs distribution:\n");
      print(self._trigraphsDistribution);

      print();
      print("-"*80);

      print();
      print(f"Average rank: { self._averageRank }\n");

  # ----------------------------------------------------------------------------

  def GenDig(self, maxLen) -> str:
    res = "";

    keys  = list(self._digraphsDistribution.keys());
    ind   = random.randrange(0, len(keys));
    first = keys[ind];

    res = first;

    while True:
      if len(res) >= maxLen:
        break;

      weights = self._digraphsDistribution[first];
      next = WeightedRandom(weights);
      res += next;
      first = next;

    return res;

# ----------------------------------------------------------------------------

  def GenTrig(self, maxLen) -> str:
    res = "";

    prefixOk = False;

    keys  = list(self._trigraphsDistribution.keys());
    ind   = random.randrange(0, len(keys));
    first = keys[ind];
    res = first;

    checkPrefix = True;

    while True:
      if len(res) >= maxLen:
        break;

      weights = self._trigraphsDistribution[first];
      next = WeightedRandom(weights);

      triplet = f"{ first }{ next }";

      if checkPrefix:
        if PrefixOK(triplet):
          checkPrefix = False;
        else:
          continue;

      #
      # Last letter of rolled digraph becomes first letter for next iteration.
      #
      first = next[1];

      #
      # Adding rolled digraph to total result.
      #
      res += next;

    return res;

  # ----------------------------------------------------------------------------

  def GenDigTrig(self, maxLen, alternate=False) -> str:
    res = "";

    keys  = list(self._trigraphsDistribution.keys()) if alternate else list(self._digraphsDistribution.keys());
    ind   = random.randrange(0, len(keys));
    first = keys[ind];

    res = first;

    flag = alternate;

    while True:
      if len(res) >= maxLen:
        break;

      if flag:
        weights = self._digraphsDistribution[first];
        next = WeightedRandom(weights);
        res += next;
      else:
        weights = self._trigraphsDistribution[first];
        next = WeightedRandom(weights);
        res += next;

      flag = not flag;

    return res;

  # ----------------------------------------------------------------------------

  def GenScoredDig(self, maxLen, alternate=False) -> str:
    res = "";

    keys  = list(self._digraphsDistribution.keys());
    ind   = random.randrange(0, len(keys));
    first = keys[ind];

    res += first;

    alternateFlag = True;

    while True:
      if len(res) >= maxLen:
        break;

      weights = self._digraphsDistribution[first];
      lettersByWeight = {};
      weightsList = [];

      for k, v in weights.items():

        if v not in weightsList:
          weightsList.append(v);

        if v not in lettersByWeight:
          lettersByWeight[v] = [];

        if k not in lettersByWeight[v]:
          lettersByWeight[v].append(k);

      weightsList.sort();

      candidates = [];

      ln = len(weightsList)
      for i in range(ln):
        candidates.append(weightsList[-(i + 1)]);

      if not alternate:
        mostPopular = candidates[0];
      else:
        if len(candidates) > 1:
          if alternateFlag:
            mostPopular = candidates[0];
          else:
            mostPopular = candidates[1];

          alternateFlag = not alternateFlag;
        else:
          mostPopular = candidates[0];

      lst = lettersByWeight[mostPopular];

      ind = random.randint(0, len(lst) - 1);

      next = lst[ind];
      res += next;
      first = next;

    return res;

  # ----------------------------------------------------------------------------

  def Generate(self, maxLen, mode : NameGenMode, relaxed : bool) -> str:
    maxAttempts = 1000;
    attempt = 0;
    res = "";

    while True:
      attempt += 1;

      if attempt >= maxAttempts:
        break;

      if mode == NameGenMode.DIGRAPHS:
        res = self.GenDig(maxLen);
        #res = self.GenScoredDig(maxLen);
      elif mode == NameGenMode.TRIGRAPHS:
        res = self.GenTrig(maxLen);
      elif mode == NameGenMode.DIGTRIG:
        res = self.GenDigTrig(maxLen);
      elif mode == NameGenMode.TRIGDIG:
        res = self.GenDigTrig(maxLen, True);

      res = RemoveTripleLetters(res);

      if relaxed:
        break;

      if res[0] == "y":
        continue;

      if res[0] not in Vowels and len(res) > 2:
        prefix = res[:2];

        prefixOk = (
          prefix in ValidPrefixes and
          ValidPrefixes[prefix] == 1 and
          res[2] in Vowels
        );

        if not prefixOk:
          continue;

      rank = GetRank(res);

      if (rank > self._averageRank) or (rank < (self._averageRank / 2)):
        continue;

      break;

    res = res.capitalize();

    return res;

################################################################################

def GetDigraphsDistr(lines : list) -> dict:
  res = {};

  for name in lines:
    ln = len(name);
    for i in range(0, ln - 1, 2):
      fl = name[i];
      sl = name[i + 1];

      if fl not in res:
        res[fl] = { sl : 1 };
      else:
        if sl not in res[fl]:
          res[fl][sl] = 1;
        else:
          res[fl][sl] += 1;

  return res;

################################################################################

def GetTrigraphsDistr(lines : list) -> dict:
  res = {};

  for name in lines:
    ln = len(name);
    for i in range(0, ln - 2, 3):
      fl = name[i];
      digraph = f"{ name[i + 1] }{ name[i + 2] }";

      if fl not in res:
        res[fl] = { digraph : 1 };
      else:
        if digraph not in res[fl]:
          res[fl][digraph] = 1;
        else:
          res[fl][digraph] += 1;

  return res;

################################################################################

def main():
  database = None;
  relaxed = False;

  maxLen = 6;
  mode = 0;
  maxNames = 10;

  modes = {
    0 : NameGenMode.DIGRAPHS,
    1 : NameGenMode.TRIGRAPHS,
    2 : NameGenMode.DIGTRIG,
    3 : NameGenMode.TRIGDIG
  };

  addHelp = textwrap.dedent(
  '''
  Modes help:

  0 - construct name based on distribution of one subsequent letter.
  1 - construct name based on distribution of two subsequent letters.
  2 - alternate between mode 0 and 1 on each iteration.
  3 - alternate between mode 1 and 0 on each iteration.

  Most descent results generate with len [ 5 ; 6 ] for mode 0 and 1.
  For modes 2 and 3 len can be increased by 1 or 2 values.
  '''
  );

  parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   epilog=addHelp);

  parser.add_argument("--seed",
                      help=(
                        "Plain text file name with names to build letters "
                        "distribution from (one name per line)"
                      ));
  parser.add_argument("--len",
                      type=int,
                      default=maxLen,
                      help=f"Maximum name length. Default: { maxLen }");
  parser.add_argument("--mode",
                      type=int,
                      default=mode,
                      choices=modes.keys(),
                      help=(
                        "0 - digraphs, "
                        "1 - trigraphs, "
                        "2 - digraphs / trigraphs, "
                        "3 - trigraphs / digraphs. "
                        f"Default: { mode }"
                      ));
  parser.add_argument("--debug",
                      help="Print distributions (e.g. for subsequent hardcoding).",
                      action="store_true")
  parser.add_argument("--names",
                      type=int,
                      default=maxNames,
                      help=f"How many names to generate. Default: { maxNames }");
  parser.add_argument("--relaxed",
                      help="Relax generation rules (high rate of shitty names!). Default: off",
                      action="store_true");

  args = parser.parse_args();

  if args.seed is not None:
    database = args.seed;

  maxLen   = args.len;
  mode     = args.mode;
  maxNames = args.names;

  rankAvg = 0.0;

  if mode not in modes:
    print("Invalid mode!");
    exit(1);

  lines = None;

  if database is not None:
    try:
      with open(database) as f:
        lines = f.readlines();
    except Exception as e:
      print(e);
      exit(1);

    for i in range(len(lines)):
      lines[i] = lines[i].strip().lower();

    d2 = GetDigraphsDistr(lines);
    d3 = GetTrigraphsDistr(lines);

    ranks = [];

    for name in lines:
      ranks.append(GetRank(name));

    rankSum = sum(ranks);

    rankAvg = rankSum / len(ranks);
  else:
    d2 = DigraphsDistribution;
    d3 = TrigraphsDistribution;
    rankAvg = AverageRank;

  nameGen = NameGen(d2, d3, rankAvg, args.debug);

  for i in range(maxNames):
    print(nameGen.Generate(maxLen, modes[mode], args.relaxed));

################################################################################

if __name__ == "__main__":
  main();
