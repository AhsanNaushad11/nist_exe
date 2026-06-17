CC = g++
GCCFLAGS = -c -Wall
ROOTDIR = .
SRCDIR = $(ROOTDIR)/src
OBJDIR = $(ROOTDIR)/obj
VPATH  = src:obj:include

OBJ = $(OBJDIR)/assess.o $(OBJDIR)/frequency.o $(OBJDIR)/blockFrequency.o \
      $(OBJDIR)/cusum.o $(OBJDIR)/runs.o $(OBJDIR)/longestRunOfOnes.o \
      $(OBJDIR)/serial.o $(OBJDIR)/rank.o $(OBJDIR)/discreteFourierTransform.o \
      $(OBJDIR)/nonOverlappingTemplateMatchings.o \
      $(OBJDIR)/overlappingTemplateMatchings.o $(OBJDIR)/universal.o \
      $(OBJDIR)/approximateEntropy.o $(OBJDIR)/randomExcursions.o \
      $(OBJDIR)/randomExcursionsVariant.o $(OBJDIR)/linearComplexity.o \
      $(OBJDIR)/dfft.o $(OBJDIR)/cephes.o $(OBJDIR)/matrix.o \
      $(OBJDIR)/utilities.o $(OBJDIR)/generators.o $(OBJDIR)/genutils.o

assess.dll: $(OBJ)
	$(CC) -shared -o $@ $(OBJ) -lm

$(OBJDIR)/assess.o: $(SRCDIR)/assess.cpp defs.h decls.h utilities.h
	$(CC) -o $@ -c $(SRCDIR)/assess.cpp

$(OBJDIR)/frequency.o: $(SRCDIR)/frequency.cpp defs.h externs.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/frequency.cpp

$(OBJDIR)/blockFrequency.o: $(SRCDIR)/blockFrequency.cpp defs.h externs.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/blockFrequency.cpp

$(OBJDIR)/cusum.o: $(SRCDIR)/cusum.cpp defs.h externs.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/cusum.cpp

$(OBJDIR)/runs.o: $(SRCDIR)/runs.cpp defs.h externs.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/runs.cpp

$(OBJDIR)/longestRunOfOnes.o: $(SRCDIR)/longestRunOfOnes.cpp defs.h externs.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/longestRunOfOnes.cpp

$(OBJDIR)/rank.o: $(SRCDIR)/rank.cpp defs.h externs.h matrix.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/rank.cpp

$(OBJDIR)/discreteFourierTransform.o: $(SRCDIR)/discreteFourierTransform.cpp \
        defs.h externs.h utilities.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/discreteFourierTransform.cpp

$(OBJDIR)/nonOverlappingTemplateMatchings.o: \
        $(SRCDIR)/nonOverlappingTemplateMatchings.cpp defs.h externs.h utilities.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/nonOverlappingTemplateMatchings.cpp

$(OBJDIR)/overlappingTemplateMatchings.o: \
        $(SRCDIR)/overlappingTemplateMatchings.cpp defs.h externs.h utilities.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/overlappingTemplateMatchings.cpp

$(OBJDIR)/universal.o: $(SRCDIR)/universal.cpp defs.h externs.h utilities.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/universal.cpp

$(OBJDIR)/approximateEntropy.o: $(SRCDIR)/approximateEntropy.cpp defs.h externs.h utilities.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/approximateEntropy.cpp

$(OBJDIR)/randomExcursions.o: $(SRCDIR)/randomExcursions.cpp defs.h externs.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/randomExcursions.cpp

$(OBJDIR)/randomExcursionsVariant.o: $(SRCDIR)/randomExcursionsVariant.cpp defs.h externs.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/randomExcursionsVariant.cpp

$(OBJDIR)/serial.o: $(SRCDIR)/serial.cpp defs.h externs.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/serial.cpp

$(OBJDIR)/linearComplexity.o: $(SRCDIR)/linearComplexity.cpp defs.h externs.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/linearComplexity.cpp

$(OBJDIR)/dfft.o: $(SRCDIR)/dfft.cpp
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/dfft.cpp

$(OBJDIR)/matrix.o: $(SRCDIR)/matrix.cpp defs.h externs.h utilities.h matrix.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/matrix.cpp

$(OBJDIR)/genutils.o: $(SRCDIR)/genutils.cpp config.h genutils.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/genutils.cpp

$(OBJDIR)/cephes.o: $(SRCDIR)/cephes.cpp cephes.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/cephes.cpp

$(OBJDIR)/utilities.o: $(SRCDIR)/utilities.cpp defs.h externs.h utilities.h config.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/utilities.cpp

$(OBJDIR)/generators.o: $(SRCDIR)/generators.cpp defs.h externs.h utilities.h \
        config.h generators.h
	$(CC) -o $@ $(GCCFLAGS) $(SRCDIR)/generators.cpp

clean:
	rm -f assess $(OBJDIR)/*.o

rebuild: clean assess
