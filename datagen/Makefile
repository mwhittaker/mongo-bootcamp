DB = bootcamp

all: zips

zips.json:
	wget http://media.mongodb.org/zips.json

zips: zips.json
	mongoimport --db $(DB) --collection zips --drop zips.json

clean:
	rm -f *.json
	rm -f *.gz
