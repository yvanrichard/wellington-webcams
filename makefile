all: index.html

index.html: build-dashboard.py
	python $<

