.PHONY: demos bump-upload

demos:
	rm -rf reprep_demos_out
	reprep_demos

bump-upload:
	$(MAKE) bump
	$(MAKE) upload
