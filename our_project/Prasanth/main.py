from graph_process import convert_to_networkGraphs
import sys
def debug(*args,**kwargs):
    print(*args,file=sys.stderr,**kwargs)
input_file = sys.argv[1]
debug("Reading input file %s" % input_file) 

nGraphList = convert_to_networkGraphs(input_file)
print(nGraphList)
