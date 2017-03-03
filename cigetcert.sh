#!/bin/bash
unset LD_LIBRARY_PATH
exec /usr/bin/python -E /usr/libexec/cigetcert/cigetcert.pyc "$@"
