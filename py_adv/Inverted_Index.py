import pickle
import argparse

class InvertedIndex:
   def __init__(self, word_to_docs_mapping):
       self._word_2_doc = word_to_docs_mapping

   def query(self, words):
       common_articles = None
       for word in words:
           if common_articles is None:
               common_articles = self._word_2_doc.get(word, set()).copy()
               continue
           common_articles &= self._word_2_doc.get(word, set())
       return common_articles

   def dump(self, filepath):
       pickle.dump(self, open(filepath, 'wb'))

   @classmethod
   def load(cls, filepath):
       obj = pickle.load(open(filepath, 'rb'))
       return obj

def load_document(filepath):
   articles = {}
   with open(filepath, 'r', encoding='utf-8') as f:
       for line in f:
           idx, other = line.split('\t', 1)
           articles[int(idx)] = other.strip()
   return articles

def build_inverted_index(articles):
   inv_index = {}
   for idx, text in articles.items():
       for word in set(text.split()):
           idx_set = inv_index.setdefault(word, set())
           idx_set.add(idx)
   return InvertedIndex(inv_index)

def build(args):
    articles = load_document(args.dataset)
    inv_index = build_inverted_index(articles)
    inv_index.dump(args.index)

def query(args):
    inv_index = InvertedIndex.load(args.index)
    with open(args.query_file, 'r', encoding='utf-8') as f:
        for line in f:
            print(*sorted(inv_index.query(line.split())), sep=',', end='\n')

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

build_parser = subparsers.add_parser('build')
build_parser.add_argument('--dataset', type=str)
build_parser.add_argument('--index', type=str)
build_parser.set_defaults(function=build)

query_parser = subparsers.add_parser('query')
query_parser.add_argument('--index', type=str)
query_parser.add_argument('--query_file', type=str)
query_parser.set_defaults(function=query)

def main(command_line=None):
    args = parser.parse_args(command_line)
    args.function(args)

if __name__ == '__main__':
    main()
