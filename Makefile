TARGET_DIR ?= target/debug

test: test-unit test-integration

test-integration:
	CSV2HTML_COMMAND="$(TARGET_DIR)/csv2html" python3 tests/test_csv2html.py

test-unit:
	cargo test

PHONY: test test-integration test-unit
