# Libraries
import urllib.request, requests
from bs4 import BeautifulSoup as BS
from collections import defaultdict
import matplotlib.pyplot as plt

# Fetch the html file
url = 'https://www.google.com/googlebooks/uspto-patents-grants-text.html'
response = urllib.request.urlopen(url)
html_doc = response.read()

# Parse the html file
html_parsed = BS(html_doc, 'html.parser')

# Format the parsed html file (optional)
#html_pretty = html_parsed.prettify()
#html_pretty

# Find all the ZIP files in the page
anchors = html_parsed.find_all('a', href=True)
zip_files = [l.get('href') for l in anchors if 'zip' and 'grant_full_text' in l.get('href')]

# Separate the ZIP files by year
years = defaultdict(list)
for year in range(1976,2016):
    for link in zip_files:
        if str(year) in link:
            years[year].append(link)

# Find the size of the ZIP files by year
years_size = defaultdict(int)
for k in years:
    years_size[k] = len(years[k])

# Plot the size of the ZIP files by year
plt.tick_params(size = 12)
plt.title('Gráfico 1 - Número de patentes registradas - Estados Unidos, 1976-2015')
plt.plot(range(len(years_size)), list(years_size.values()))
plt.xticks(range(len(years_size)), list(years_size.keys()))
plt.gca().margins(x=0.0005)
plt.gcf().canvas.draw()
tl = plt.gca().get_xticklabels()
maxsize = max([t.get_window_extent().width for t in tl])
m = 0.2 # inch margin
s = maxsize/plt.gcf().dpi*40+2*m
margin = m/plt.gcf().get_size_inches()[0]

plt.gcf().subplots_adjust(left=margin, right=1.-margin)
plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

plt.show()

# Download the zip files
def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)