from main import main
import sys 
import asyncio

if __name__ = '__main__':
    if (len(sys.argv) < 3):
        print("usage: python -m package_name url search_text endpoint")
        sys.exit(1)
    url = sys.arvg[1]
    stxt = sys.argv[2]
    endpoint = sys.argv[3]
    
    asyncio.run(main(url, stxt, endpoint))