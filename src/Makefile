CC       = gcc
MYCFLAGS = -O3 -Wall

all: lang tail partinfo

partinfo: partinfo.c
	$(CC) $(MYCFLAGS) $^ -o $@ -lparted

tail:
	pyuic4 GraphicalTailForm.ui > GraphicalTailForm.py

lang :
	pylupdate4 Installer.pro

clean :
	rm -f GraphicalTailForm.py

