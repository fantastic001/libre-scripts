
from translit import cir_to_lat 
import sys
if __name__ == "__main__":
    f = open(sys.argv[1], "r")
    print(cir_to_lat(f.read()))
    f.close()
