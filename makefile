build_project: TextDetection.py grouping_letter
	cp TextDetection.py TextDetection.pyx
	python setupTextDetection.py build_ext --inplace
	rm -r *.c *.pyx

grouping_letter: groupingLetter.py
	cp groupingLetter.py groupingLetter.pyx
	python setupGroupingLetter.py build_ext --inplace
	rm -r *.c *.pyx