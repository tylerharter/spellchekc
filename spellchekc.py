#!/usr/bin/python
import sys, re, subprocess, collections

class Checker:
    def __init__(self, skip):
        self.words = collections.defaultdict(list)
        with open(skip) as f:
            self.skip = set([l.strip() for l in f])
        
    def check_includes(self, path):
        with open(path) as f:
            for l in f:
                m = re.match(r'\\(include|input)\{(.*?)\}', l)
                if m:
                    self.check_file(m.group(2)+'.tex')

    def check_file(self, path):
        print 'Checking '+path

        with open(path) as f:
            p = subprocess.Popen(['aspell', 'list', '--mode=tex'],
                                 stdin=f, stdout=subprocess.PIPE)
            for l in p.stdout:
                word = l.strip()
                if word in self.skip:
                    continue
                self.words[word].append(path)

        # recurse
        self.check_includes(path)

    def dump(self):
        print '='*40
        print 'WORDS'
        print '='*40
        words = sorted(self.words, key=lambda word: (len(self.words[word]), word))
        for word in words:
            print (word.ljust(30) + ' ' +
                   str(len(self.words[word])).ljust(4) + ' ' +
                   sorted(self.words[word])[0])
        print '='*40
        print 'UNIQ WORDS: ' + str(len(self.words)).rjust(5)
        print 'INSTANCES:  ' + str(sum(map(len, self.words.values()))).rjust(5)
    
def main():
    if len(sys.argv) != 3:
        print 'Usage: %s <main.tex> <skip.txt>' % sys.argv[0]
        sys.exit(1)

    checker = Checker(sys.argv[2])
    checker.check_file(sys.argv[1])
    checker.dump()

if __name__ == '__main__':
    main()
