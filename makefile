clean:
	rm -fr reports/*.log reports/*.xml screenshots/*.png

test:
	behave -k --tags=-wip

reproduce:
	behave -k --tags=-wip --tags=${ticket}

