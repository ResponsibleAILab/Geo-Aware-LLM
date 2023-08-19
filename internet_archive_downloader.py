import os
import sys

if len(sys.argv) < 3:
    raise Exception('Usage: "python internet_archive_downloader.py [YEAR] [MONTH_NUMBER]"')

# Test if axel is installed, discard output
ret_val = os.system('axel --help 1>/dev/null')

if ret_val != 0:
    raise Exception('axel package not found on system, please install axel')

try:
    year = int(sys.argv[1])
except:
    raise Exception('Invalid year specified')

try:
    month = int(sys.argv[2])
except:
    raise Exception('Invalid month specified')

if month < 1 or month > 12:
    raise Exception('Invalid month number specified must be 1-12')

if year < 2012 or year > 2022:
    raise Exception('Invalid year specified, year must be 2012-2022')

month = str(month)
year = str(year)
if len(month) == 1:
    month = f'0{month}'

file_name = f'twitter_archive_{year}_{month}.tar'
if not os.path.exists('downloads'):
    os.mkdir('downloads')

if os.path.exists(f'downloads/{file_name}'):
    raise Exception(f'Error: file {file_name} already exists')

url = f'https://archive.org/download/archiveteam-twitter-stream-{year}-{month}/archiveteam-twitter-stream-{year}-{month}.tar'
print(f'Downloading: {url}')
os.system(f'axel -a -n 10 {url} --output=downloads/{file_name}')