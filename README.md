# CK3-Family-Tree-Exporter-To-Gramps-Fast-JSON-Version


**The Exporter is working as of game version 1.3.1 (Corvus) With Normal AND Ironman Save. It can be used for other languages other than english if you tweak the .py file
and create an executable from it yourself**

This version of the exporter utilizes a JSON formatted save file created from scorpdx's CK3 to JSON converter to make exporting family tree data ridiculously fast. A 10 minute session in the older repo here https://github.com/blastentwice/CK3-Family-Tree-Exporter-To-Gramps takes literal seconds with the JSON version. More infomation about the converter can be found at his repo https://github.com/scorpdx/ck3json.

The Exporter is used to extract family tree data into CSV and Gramps-XML format, which can be imported directly into the free open source genealogy software Gramps. With Gramps you can view your family tree offline in many different modes including pedigree and graph view. You then can also convert your Gramps tree into other formats including GEDCOM and pdf.

You can choose to export your family tree with cadet families, effectively extending the tree until you hit a non-dynasty member. With this version, many personal information is included, such as skills,traits,faith,culture,sexual orientation,and cause of death. I plan to add events,stories for all alive individuals in the future! 

For this JSON version, there is an option to let the exporter automatically import the tree for you while also including faith and traits icons that corresponds to each character. The faith and traits icons in the game file will be converted in pngs which will be made in the directory of the exporter.   


Documentations on how to use Gramps can be found here https://gramps-project.org/wiki/ and the download link for Gramps can be found here https://gramps-project.org/blog/download/.

## Step 1: Setting Up The Exporter  ##

1. Clone the entire repo and extract it somewhere in your computer. Within it, the traits and avatar folder should not be modified because they are necessary to run the program. There is also the ck3.json executable that will be called by the exporter to convert your save into a JSON file.

2. Copy and move your ck3 save file in the same folder as the program. There is no need to extract them as the program will do that automatically if needed.

## Step 2: Setting up Gramps

3. Download Gramps from https://gramps-project.org/blog/download/. Once installed, if not prompted automatically, go to Edit->Preferences->General tab and click on  the Check for updated addons now button. Choose download all addons to get the most out of Gramps.

4. Close the program for now. If you leave it running on the background it will prevent the exporter from using its features.

## Step 2: Convert your save into a JSON file  ##

5.Run the exporttree.exe file. You will encounter a menu with several options. For the first time you are working with the save you need to pick option 1 to convert your save into a JSON file. This type of file allows us to quickly parse through many lines of text at tremendous speeds.

6. You will be prompted to indicate whether the save is an ironman or normal save. Then, provide the name of your ck3 file (eg. mysave.ck3)

7. Let the program convert your file. It should no longer than 15 seconds to get a JSON file. Hit the enter key when it's done when prompted to return to the main menu

## Step 3: Export your family tree into an CSV file  ##

8. Pick option 2 to extract family tree information into a CSV format. You will be prompted to provided the name of the JSON as well as the game directory. **"C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game** is the usual directory for steam releases. The exported needs this directory to utilize the localization files to convert the values or keys into readable English.

9. The process will create a folder called pickle. The pickles files inside are basically savedata for when you choose to run the program again. that way, you will only have
to enter your game directory once and all the game information the exporter needs are loaded instantly from the pickle files. This will significantly shorten run time for future use.

10.Input the Dynasty/House of the character and the character's id  that you want to start your tree from when prompted. The character's id can be found by running CK3 in debug mode or by looking in the savefile. Then, decide if you want to include Cadet Members' offspring. Note that the character you choose is where the tree will start from. Extended
families will not be included. If you want everyone in the dynasty, pick the dynasty founder as the base instead.

11. Confirm your input to start the script. The script should run and display the processed characters on the screen so that you can monitor the progress. This will finish very
quickly.

12.  A CSV file should have been created in the same directory as the script along with the pickle information for faster uses in the future. You can manually import 
this CSV file as is using https://gramps-project.org/wiki/index.php/Gramps_5.1_Wiki_Manual_-_Manage_Family_Trees:_CSV_Import_and_Export. 

13. Proceed to the next option to automatically import Gramps with faith and traits icons for each character. 

## Step 4: Convert your CSV file into a Gramps-XML to include image information and automatically importing into Gramps  ##

14. For this step, it is important that Gramps is not running in the background. Otherwise, the program will get an error or hang.

15. You will need to first provide the name of your CSV file and the Gramps directory where the executable is stored. This is usually **C:\Program Files\GrampsAIO64-5.1.3\**.

16. Next, for first time use, you will need to enter your game directory again. Two folders with  faith and traits png images will be created in your directory.

17. A Gramps-XML file will be created by using the Gramps command line features. The exporter will work off from this XML by adding links to the images in your directory
and attaching it to every character that has those faiths or traits.

17. The program will prompt you if you want to change your family tree name from the default YourDynasty_Tree name. Note that if you already have a tree in Gramps with the same name, it will overwrite it. Be sure to change the tree name if that is the case.

18. The import to Gramps will be done automatically using the command


17. Download and install Gramps from the link above. After installation, replace importcsv.py script in **C:\Program Files\GrampsAIO64-5.1.3\gramps\plugins\importer** 
with the one in the respotitory. This will allow you to keep the program from changing the gender of LGBQ+ persons that are parents when you import the csv into Gramps. This step can be skipped, but you must go to Edit->Preferences->Display and change "Surname guessing" parameter to "None" within Gramps after everytime you create a new tree.

7. After you launch the program it will prompt you to make a family tree. Click new to make the tree and load it.

8. Go to Edit->Preferences->General tab and click on the the Check for updated addons now button. You can choose to download all the modules or simply download Graph View which is used to view the family tree. 

9. Got to Edit->Preferences->Display tab to change Name format to display the title of the characters.

10. Go to Family Trees->Import and select your csv file. The program will load up the file into its database. From here, you can play around with the program. there are extensive documentation regarding its tools that you can read on your own here https://gramps-project.org/wiki. 

11. To look at the tree CK3 style,go to the Charts tab and select the button up top that looks like two parallel lines labeled Graph View. Documentation for the program can be found here https://www.gramps-project.org/wiki/index.php/Graph_View.

12. OPTIONAL: Export your Gramps tree as a GEDCOM file by going to Family Tree->Export. 
