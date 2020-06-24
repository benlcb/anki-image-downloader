import sqlite3
from google_images_search import GoogleImagesSearch
import os
import json
import zipfile
import shutil

PATH_TO_ZIP = "/home/richard/Downloads/test/with_picture.apkg"
OUTPATH = "/home/richard/Downloads/test/testoutput.apkg"
DECKPATH = ""
SEP = '\x1f'
GCS_DEVELOPER_KEY = os.getenv('GCS_DEVELOPER_KEY')
GCS_CX = os.getenv('GCS_CX')

# define search params:
_search_params = {
    'q': '',
    'num': 1,
    'safe': 'off',
    'fileType': 'jpg',
    'imgSize': 'LARGE',
}

# Unzip APKG file
workdir, zipname = os.path.split(PATH_TO_ZIP)
DECKPATH = workdir + '/tmp/'
os.mkdir(DECKPATH)
zip_ref = zipfile.ZipFile(PATH_TO_ZIP, 'r')
zip_ref.extractall(DECKPATH)
zip_ref.close()

# Load JSON File mapping picture names to files
json_file = open(DECKPATH + "media")
picnames = json.load(json_file)
curr_pic_num = max({int(s) for s in picnames.keys()}) + 1

# Load SQL Database containing cards
con = sqlite3.connect(DECKPATH + 'collection.anki2')#, isolation_level=None)
c = con.cursor()
c.execute('SELECT id,flds,sfld FROM notes')

# Iterate over Cards adding pictures
for s in c.fetchall():
    # Fetch fields
    id = s[0]
    (flds_first, flds_second) = s[1].split(SEP)
    sfld = s[2]

    #Check if image is already present
    if '.jpg' in s[1] or '.png' in s[1]:
        s = c.fetchone()
        continue

    # Get image from google images
    _search_params['q'] = flds_second
    gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)
    gis.search(search_params=_search_params, path_to_dir=DECKPATH)
    (image,) = gis.results()

    # Rename picture
    os.rename(image.path, DECKPATH + str(curr_pic_num))
    picname = flds_second + ".jpg"

    # Push image to database
    t = (flds_first + '\x1f' + flds_second + '<div><img src=\"' + picname + '\"><br></div>', id,)
    c.execute('UPDATE notes SET flds = ? WHERE id = ?', t)

    # Update JSON
    picnames[str(curr_pic_num)] = picname

    # Increment counter
    curr_pic_num += 1


# Close SQL Lite database
con.commit()
con.close()

# Write changes to JSON file
json_file.close()
json_file = open(DECKPATH + "media", 'w')
json.dump(picnames, json_file)
json_file.close()

# Create .APKG
zipObj = zipfile.ZipFile(OUTPATH, 'w')
for folderName, subfolders, filenames in os.walk(DECKPATH):
   for filename in filenames:
       filePath = os.path.join(folderName, filename)
       zipObj.write(filePath, os.path.basename(filePath))
zipObj.close()

# Delete tmp folder
shutil.rmtree(DECKPATH)






