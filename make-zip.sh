#!/bin/sh

find payments -name \*.pyc -exec rm -v {} \;
find payments -name \*~ -exec rm -v {} \;
rm payments.zip
zip -r payments.zip payments
