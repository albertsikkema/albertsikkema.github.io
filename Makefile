.PHONY: run install clean

BUNDLE := $(HOME)/.rbenv/shims/bundle

# Run local development server
run:
	$(BUNDLE) exec jekyll serve

# Install dependencies
install:
	$(BUNDLE) install

# Clean generated files
clean:
	$(BUNDLE) exec jekyll clean
