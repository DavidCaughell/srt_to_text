"""Creates readable text file from SRT file.

NOTES
 * Run from command line as
 ** python srt_to_txt.py file.srt cp1252
 * Creates file.txt with extracted text from file.srt 
 * Script assumes that lines beginning with lowercase letters or commas 
 * are part of the previous line and lines beginning with any other character
 * are new lines. This won't always be correct. 

Verbosity: 0 is silent. 2 is after every file. 1 is upon completion only.
"""

# TODO:
# test that it still works via argv
# consider letting them flag that they want the whole directory done, in argv,

import re, sys, os

_ONE_FILE = True
_FILE = None
_ENCODING = None
_OUT_FORMAT = 1
_VERBOSITY = 0
_ONE_FILE = False
##_FILE = 'L1_S1-en.srt'
_OUT_FORMAT = 2
_OUT_FORMAT = 3
_VERBOSITY = 1
_VERBOSITY = 2


def is_time_stamp(l):
  if l[:2].isnumeric() and l[2] == ':':
    return True
  return False

def has_letters(line):
  if re.search('[a-zA-Z]', line):
    return True
  return False

def has_no_text(line):
  l = line.strip()
  if not len(l):
    return True
  if l.isnumeric():
    return True
  if is_time_stamp(l):
    return True
  if l[0] == '(' and l[-1] == ')':
    return True
  if not has_letters(line):
    return True
  return False

def is_lowercase_letter_or_comma(letter):
  if letter.isalpha() and letter.lower() == letter:
    return True
  if letter == ',':
    return True
  return False

def clean_up(lines):
  '''Get rid of all non-text lines and try to combine text broken into multiple lines.'''
  new_lines = []
  for line in lines[1:]:
    if has_no_text(line):
      continue
    elif len(new_lines) and is_lowercase_letter_or_comma(line[0]):
      #combine with previous line
      new_lines[-1] = new_lines[-1].strip() + ' ' + line
    else:
      new_lines.append(line)
  return new_lines

def main_argv(args):
  """
    args[1]: file name
    args[2]: encoding. Default: utf-8.
      - If you get a lot of [?]s replacing characters,
      - you probably need to change file_encoding to 'cp1252'
  """
  file = args[1]
  file_encoding = 'utf-8' if len(args) < 3 else args[2]

  with open(file, encoding=file_encoding, errors='replace') as f:
    lines = f.readlines()
    new_lines = clean_up(lines)
  new_file = file[:-4] + '.txt'
  with open(new_file, 'w') as f:
    for line in new_lines:
      f.write(line)

def output_all_files(encoding=None, out_format=None):
    '''Writes a file *.txt from *.srt for each .srt in the cwd.'''
    files = scan_cwd_for_srt_files()
    if _VERBOSITY >= 1:
        print('Writing Files:')
    for f in files:
        output_one_file(f, encoding, out_format)
    if _VERBOSITY >= 1:
        print('Done writing all files.')

def scan_cwd_for_srt_files():
    '''Returns a list of the .srt files in the cwd.'''
    files = [f for f in os.listdir('.') if os.path.isfile(f) and eval("'.srt' in f")]
    return files

def trunc_after_80(line):
  outlines = []
  while len(line) > 80:
    # is 80 NOT whitespace?
    if line[80].split():
      wordlen = len(line[80:].split()[0])
      outlines.append(line[:80 + wordlen] + '\n')
      line = line[80 + wordlen + 1:]
    else:
      outlines.append(line[:80] + '\n')
      line = line[81:]
  else:
    outlines.append(line)
    return outlines
  
def output_one_file(file, encoding=None, out_format=None):
    '''Writes a file *.txt from *.srt, using utf-8 encoding by default.
    out_format:
        1 = Simple file with one line per entry in the .srt
        2 = Blank line between every entry
        3 = Like 2, but with strings split after whitespace on col 80+
    '''
    
    file_encoding = encoding
    new_file = file[:-4] + '.txt'

    if out_format is None:
        out_format = _OUT_FORMAT
    if file_encoding is None:
        file_encoding = 'utf-8'

    with open(file, encoding=file_encoding, errors='replace') as f:
        lines = f.readlines()
        new_lines = clean_up(lines)

    if out_format >= 2:
      new_lines = [line + '\n' for line in new_lines]

    if out_format == 3:
      formatted_lines = []
      for line in new_lines:
        for new in trunc_after_80(line):
          formatted_lines.append(new)
      new_lines = formatted_lines

    with open(new_file, 'w') as f:
        for line in new_lines:
          f.write(line)

    if _VERBOSITY == 2:
        print('Wrote file:', new_file)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main_argv(sys.argv)
    else:
        print('\n\n')
        if _ONE_FILE:
            output_one_file(_FILE, encoding=_ENCODING, out_format=_OUT_FORMAT)
        else:
            output_all_files(encoding=_ENCODING, out_format=_OUT_FORMAT)
        print('\n\n')


##From stackexchange:
##But be careful while applying this to other directory, like
##
##files = [f for f in os.listdir(somedir) if os.path.isfile(f)].
##
##which would not work because f is not a full path but relative to the current dir.
##
##Therefore, for filtering on another directory, do os.path.isfile(os.path.join(somedir, f)) '''
