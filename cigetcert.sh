#!/bin/bash
unset PYTHONPATH LD_LIBRARY_PATH
exec /usr/bin/python /usr/libexec/cigetcert/cigetcert.pyc "$@"
