BUILD_USER ?= $(USER)
USER_TEMP ?= /tmp/$(BUILD_USER)
PROJECT_TEMP ?= $(USER_TEMP)/cargo/csv2html
TARGET ?= x86_64-unknown-linux-musl
BUILD_OPTS ?= --target $(TARGET)
BUILD_OPTS_WITH_DIR ?= $(BUILD_OPTS) --target-dir $(PROJECT_TEMP)

dev: temp-dir
	# A workaround for https://github.com/rust-lang/rust/issues/46981
	find Cargo.* src/ tests/ | entr -r sh -c 'cargo check $(BUILD_OPTS_WITH_DIR) < /dev/null'

debug: temp-dir
	cargo build $(BUILD_OPTS_WITH_DIR)

install:
	install $(PROJECT_TEMP)/$(TARGET)/release/csv2html /usr/local/bin
	strip /usr/local/bin/csv2html

release: temp-dir
	cargo build $(BUILD_OPTS_WITH_DIR) --release

temp-dir:
	@-mkdir -m 0700 $(USER_TEMP)/ 2> /dev/null
	@-mkdir -p $(PROJECT_TEMP)/ 2> /dev/null

test: test-unit test-integration

test-integration: debug
	CSV2HTML_COMMAND="$(PROJECT_TEMP)/$(TARGET)/debug/csv2html" python3 tests/test_csv2html.py

test-unit:
	cargo test $(BUILD_OPTS_WITH_DIR)

uninstall:
	rm /usr/local/bin/csv2html

PHONY: dev install release temp-dir test test-integration test-unit uninstall
