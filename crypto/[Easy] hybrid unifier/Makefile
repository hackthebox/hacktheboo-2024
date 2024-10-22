default:
ifdef name
	@mkdir -p release/crypto_$(name); \
	mkdir -p release/crypto_$(name)/challenge; \
	cp -r challenge/application release/crypto_$(name)/challenge/application; \
	cp challenge/README.pdf release/crypto_$(name)/challenge; \
	echo "HTB{fake_flag_for_testing}" > release/crypto_$(name)/flag.txt; \
	cp build-docker.sh Dockerfile release/crypto_$(name);

	@cd release; \
	 	zip -9 -r ./crypto_$(name).zip ./crypto_$(name); \
		unzip -l ./crypto_$(name).zip;
		
	@echo [+] Challenge was built successfully.
else
	@echo [-] Please define the challenge name. For example, \"make name=cool_chall_name\"
endif

flag:
	@echo [+] Flag : $$(python3 -c 'print(open("flag.txt").read())')

solver:
	@echo [+] Running solver...
	@./build-docker.sh
	@sleep 2
	@python3 htb/solver.py
	@find ./ -name "*.sage.py" -type f -delete

test: clean default flag solver

clean:
	@rm -rf release/*
	@find . -name "*.sage.py" -type f -delete
	@echo [+] Challenge release deleted successfully.
