build_project: TextDetection.py
	cp TextDetection.py TextDetection.pyx
	python setupTextDetection.py build_ext --inplace
	rm -r *.c