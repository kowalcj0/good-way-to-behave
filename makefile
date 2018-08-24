clean:
	rm -fr reports/*.log reports/*.xml screenshots/*.png

tests:
	behave -k --tags=-wip --tags=-fixme

reproduce:
	behave -k --tags=-wip --tags=${ticket}

