# create the required submission tarball
# warning: everything in this area is TEMPORARILY created from sources elsewhere
# with the exception of the README file (which is part of the submission!)
# for more info on submission requirements, see: http://www.icfpcontest.org/

# directory in which to dump stuff for the .tar.gz
TARDIR := ./tmp/
TARFILE := cd-lb-kg.tar.gz

# path to root, relative to the temporary tarball root
RELTOPDIR := ../

$(TARFILE):
	@# everything must be in this directory prior to creating
	@# a tarball so that relative .tar.gz paths are correct;
	@# but NONE of the files or directories here should be the
	@# originals...they should all be copied from somewhere else
	mkdir $(TARDIR)
	mkdir $(TARDIR)/src
	@echo
	@echo "-> copying source files to temporary space..."
	cp -a $(RELTOPDIR)/{engines,pygame} $(TARDIR)/src/
	mkdir $(TARDIR)/src/submit/
	cp $(RELTOPDIR)/submit/Makefile $(TARDIR)/src/submit/
	#cp $(RELTOPDIR)/install $(TARDIR) # FIXME: update this when actual executable is done
	touch $(TARDIR)/install
	#cp $(RELTOPDIR)/run     $(TARDIR) # FIXME: update this when actual executable is done
	touch $(TARDIR)/run
	cp $(RELTOPDIR)/submit/README $(TARDIR)
	chmod +x $(TARDIR)/{install,run}
	@echo
	@echo "-> creating tarball..."
	cd $(TARDIR) && tar zcf $(notdir $@) README install run src/ # these 4 parts required by: http://www.icfpcontest.org/
	mv $(TARDIR)/$(notdir $@) $@
	@echo
	@echo "-> submission contains:"
	@tar ztf $@ # sanity check
	@echo
	@echo "-> done; be sure to upload $(TARFILE) with this form:"
	@echo "   https://spreadsheets.google.com/spreadsheet/viewform?formkey=dDRFOXgxQ3g2M3I3X1VTV3FBREdULWc6MQ"

.PHONY: clean
clean:
	-rm -Rf $(TARDIR) $(TARFILE)
