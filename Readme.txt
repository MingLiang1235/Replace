1)Programmes network:
a)    sudo find /mnt/16orig/sdb2 | grep sqlite >&1 | tee ~/work/Replace/sqlite.txt
/mnt/16orig   --->   ~/work/Replace/datafile
	
b)	sudo find / | grep .*[^\.]git.* >&1 | tee git-find-without-dot.txt
/...../...../git   --->   ~/work/Replace/datafile

c)	manual delete no use entry of git-find-without-dot.txt

d)	ChangeName.py -t git-find-without-dot.txt  (To add /mnt/16orig/sdb1 header to each entry of datafile)
./git-find-without-dot.txt   --->   ./git.new-input.txt

e)	ListAttr.py -t git-find-without-dot.origin.txt  (To list the accessable and owner of entry)
./git-find-without-dot.origin.txt   --->   ./git-attr.txt

f)  CopyThem.py -t git-find-without-dot.txt (To Copy gitFiles to /mnt/16orig/sdb1)
./...../...../git   --->   /mnt/16orig/sdb1/.....


2)In cubie2 soc card:
a)Replacer.py -t sqlite.txt  (cp -r --preserve /mnt/16orig/sdb2/..../ /..../)
/mnt/16orig/sdb2/.....   --->   /..../....

b)Replacer.py -t git.txt  (cp -r --preserve /mnt/16orig/sdb1/..../ /..../)
/mnt/16orig/sdb1/.....   --->   /..../....

3)You can get the statements to create origin datafile from backup/history-yyyy-mm-dd.log
