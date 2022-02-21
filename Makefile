VERSION := $(shell sed -n 's/^Version: //p' cigetcert.spec)

cigetcert.html: cigetcert.1
	groff -mandoc -Thtml cigetcert.1 >cigetcert.html

# For koji builds
sources:
	@tar cf - *  --transform="s,^,cigetcert-$(VERSION)/," | gzip --best > cigetcert-$(VERSION).tar.gz

# For copr builds
srpm: sources
	rpmbuild -bs --define '_sourcedir .' --define '_srcrpmdir .' cigetcert.spec
