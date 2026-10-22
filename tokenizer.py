import argparse;

from util import Tokenize;

################################################################################

def main():
  parser = argparse.ArgumentParser();

  parser.add_argument("NAME", type=str);

  args = parser.parse_args();

  tokens = Tokenize(args.NAME);

  print(f"{ args.NAME } -> { tokens }");

################################################################################

if __name__ == "__main__":
  main();
