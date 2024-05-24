CSV2HTML_COMMAND ?= target/debug/csv2html

all: test

debug:
	cargo build

release: release-linux release-windows

release-linux:
	cargo build --release --target x86_64-unknown-linux-musl
	cp target/x86_64-unknown-linux-musl/release/csv2html csv2html-linux-x86_64
	strip csv2html-linux-x86_64

release-windows:
	cargo build --release --target i686-pc-windows-gnu
	cp target/i686-pc-windows-gnu/release/csv2html.exe csv2html-win32.exe
	strip csv2html-win32.exe

test: debug test-unit test-integration

test-integration:
	CSV2HTML_COMMAND="$(CSV2HTML_COMMAND)" cargo test -- --ignored

test-unit:
	cargo test

PHONY: all debug release release-linux release-windows test test-integration test-unit
