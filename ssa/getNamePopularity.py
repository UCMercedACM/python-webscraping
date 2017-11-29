import matplotlib.pyplot as plt
import zipfile
import urllib
import sys
import os

# Make sure user provided enough args
if len(sys.argv) < 3:
	print "Usage: python {} Name Gender State"
	exit();

# Parse inputs - first is name, second is gender
if sys.argv[2].lower() != "m" and sys.argv[2].lower() != "f":
	print "Social security gender listed only as M or F";
	exit();

name = sys.argv[1];
gender = sys.argv[2];
stateLabel = sys.argv[3];

# Choose what file to get, and where to put it
zipFileName = "ssaData.zip"
dataDirectory = os.path.join(os.getcwd(),"data");
ssaDataZipLocation = os.path.join(dataDirectory, zipFileName);

# Create data directory if it doesn't exist
if not os.path.exists(dataDirectory):
	os.makedirs(dataDirectory)

# Check if we already have the file
if not os.path.isfile(ssaDataZipLocation):
	# If not, download it
	print "Downloading..."
	urllib.urlretrieve ("https://www.ssa.gov/oact/babynames/state/namesbystate.zip", ssaDataZipLocation);

	# File is in zip format, so unzip it to use contents
	print "Unzipping..."
	zip = zipfile.ZipFile(ssaDataZipLocation)
	zip.extractall(dataDirectory)

	print "Done!"

else:
	print "We already have our data!"

# At this point, we have a directory of files, one for each year. let's list them
dirContents = os.listdir(dataDirectory)
# print dirContents

# Get name of the file we want
try:
	desiredFile = next((f for f in dirContents if stateLabel.lower() in f.lower()));
except StopIteration:
	print "Couldn't find state", stateLabel;
	exit();

fileToOpen = os.path.join(dataDirectory, desiredFile);
print "Opening", fileToOpen

# Read data from file
with open(fileToOpen, "r") as myFile:
	dataLines = myFile.readlines();
	print len(dataLines)

# Step through data, store year and number of people
years = [];
counts = [];
for line in dataLines:
	entry = line.split(",");
	# CA,F,1910,Florence,93
	if entry[1].lower()==gender.lower() and entry[3].lower()==name.lower():
		years.append(int(entry[2]));
		counts.append(int(entry[4]));


if len(counts) > 0:
	plt.plot(years, counts, "o-")
	plt.ylabel('# People')
	plt.xlabel('Year')
	plt.title("People born with name "+name);
	plt.show()

else:
	print "Sorry, nobody by that name on record :("
