"""
--- Day 7: No Space Left On Device ---
You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device
Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
cd / switches the current directory to the outermost directory, /.
ls means list. It prints out all of the files and directories immediately contained by the current directory:
123 abc means that the current directory contains a file named abc with size 123.
dir xyz means that the current directory contains a directory named xyz.
Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
Directory d has total size 24933642.
As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.
To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?

To begin, get your puzzle input.

--- Part Two ---
Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least 30000000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

Delete directory e, which would increase unused space by 584.
Delete directory a, which would increase unused space by 94853.
Delete directory d, which would increase unused space by 24933642.
Delete directory /, which would increase unused space by 48381165.
Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?


"""
import re
import json
__author__ = "Adrián Ángel Moya Moruno"

def execute_command(command,parameter):
  if (command == "cd"):
    move_position(parameter)
  #if the command is ls, there isn't necessary to do anything

def move_position(parameter):
  if ('..' in parameter):
    current_position.pop()
    return
  current_pos = get_current_position_in_tree()
  if not parameter in current_pos:
    current_pos[parameter] = {}
  current_position.append(parameter)

def get_current_position_in_tree():
  pos = directory_tree 
  for fold in current_position:
    pos = pos[fold]
  return pos

def set_folder_size(current_folder):
  folder_size = 0
  for element, content in current_folder.items():
    if type(content) is dict:
      #Use of recursive function
      set_folder_size(content)
      folder_size += content['size']
    else:
      folder_size += int(content)
  
  if(folder_size > 0):
    current_folder['size'] = folder_size
    if(folder_size <= 100000):
      solution['part_1'] += folder_size
    
def find_best_folder_to_delete(folder, needed_space):
  for element, content in folder.items():
    if type(content) is dict:
      if(content['size'] >= needed_space):
          if (solution['part_2'] > content['size']):
            solution['part_2'] = content['size']
      find_best_folder_to_delete(content, needed_space)


solution = {
  "part_1": 0,
  "part_2": 999999999
}
f = open("./input.txt", "r")
directory_tree = {}
current_position = []

system_size = 70000000
update_size = 30000000



#Gp 1 says if the line is a command or not. Then gp 2 is the name of the command and finally if it exists, gp 3 gives us the parameter for cd
command_regex = r'(\$)\s+(cd|ls) ?([\w/.]+)?'
#Gp 1 gives us if it is a dir or file, gp 2 gives us the name of it
dir_file_regex = r'(dir|\d+) ([\w.]+)'
for line in f.readlines():
  line = line.replace("\n", "")
  line_match_command = re.search(command_regex,line)
  #cd or ls
  if(line_match_command):
    command = line_match_command[2]
    param = line_match_command[3]
    execute_command(command,param)
  #showing a directory or file
  else:
    line_match_file = re.search(dir_file_regex,line)
    #this if controls if the line is a file
    if not 'dir' in line_match_file[1]:
      file_size = line_match_file[1]
      file_name = line_match_file[2]
      current_pos = get_current_position_in_tree()
      current_pos[file_name] = file_size


set_folder_size(directory_tree)

#Solution for part 2
occuped_size = directory_tree['size']
free_space = system_size - occuped_size
needed_space = 30000000 - free_space

find_best_folder_to_delete(directory_tree,needed_space)


# Serializing directory tree. This is not necessary but I did to get it more visual  
with open('tree.json', 'w') as fp:
  json.dump(directory_tree, fp,indent = 4)

#Solutions
print("The solution for 1st part is: "+str(solution['part_1']))
print("The solution for 2nd part is: "+str(solution['part_2']))