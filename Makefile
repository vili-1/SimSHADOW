PYTHON ?= python

.PHONY: quick full verify package clean

quick:
	@$(PYTHON) -c "import os; req=['results','logs','figures']; missing=[d for d in req if not os.path.isdir(d)]; print('Required directories present' if not missing else f'Missing: {missing}'); files=['results/table1_identification.txt']; miss=[f for f in files if not os.path.exists(f)]; print('Key artifacts present' if not miss else f'Artifacts missing: {miss}')" && echo "Quick verification complete"

full:
	$(PYTHON) run_simshadow.py

verify:
	@$(PYTHON) verify.py

figures:
	$(PYTHON) gen_figures.py

package:
	@mkdir -p ../..
	@echo "Creating manifest"
	@{ find . -type f; } | sed 's|^./||' | sort > ../../dist/MANIFEST.txt
	@tar -czf ../../dist/simshadow-1.0.0.tar.gz -T ../../dist/MANIFEST.txt
	@shasum -a 256 ../../dist/simshadow-1.0.0.tar.gz > ../../dist/SHA256SUMS
	@echo "Package written to dist/"

clean:
	rm -f ../../dist/MANIFEST.txt ../../dist/SHA256SUMS ../../dist/simshadow-1.0.0.tar.gz
