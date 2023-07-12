#! /bin/sh

cargo build --release
cp target/release/csv2html csv2html-linux-x86_64
strip csv2html-linux-x86_64

cargo build --release --target i686-pc-windows-gnu
cp target/i686-pc-windows-gnu/release/csv2html.exe csv2html-win32.exe
strip csv2html-win32.exe
