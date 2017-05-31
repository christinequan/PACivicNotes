from tika import parser
import pprint

parsedPDF = parser.from_file("Transcripts/August 15, 2016.pdf")
pprint.pprint(parsedPDF["metadata"])
# pprint.pprint(parsedPDF["content"])
