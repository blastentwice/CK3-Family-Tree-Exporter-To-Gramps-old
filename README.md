# CK3-Family-Tree-Exporter-To-Gramps-Fast-JSON-Version 2.7 (Compatible with CK3 1.4.4 Azure patch)
![alt text](https://github.com/blastentwice/CK3-Family-Tree-Exporter-To-Gramps-Fast-JSON-Version/blob/main/Screenshots/showcase.png?raw=true)

**The Exporter is working as of game version 1.4.4 (Azure) With Normal AND Ironman Save. It can be used for other languages other than english if you tweak the .py file
and create an executable from it yourself**

This version of the exporter utilizes a JSON formatted save file created from scorpdx's CK3 to JSON converter to make exporting family tree data ridiculously fast. A 10 minute session in the older repo here https://github.com/blastentwice/CK3-Family-Tree-Exporter-To-Gramps takes literal seconds with the JSON version. More infomation about the converter can be found at his repo https://github.com/scorpdx/ck3json.

The Exporter is used to extract family tree data into CSV and Gramps-XML format, which can be imported directly into the free open source genealogy software Gramps. With Gramps you can view your family tree offline in many different modes including pedigree and graph view. You then can also convert your Gramps tree into other formats including GEDCOM and pdf.

You can choose to export your family tree with cadet families, effectively extending the tree until you hit a non-dynasty member. With this version, many personal information is included, such as skills,traits,faith,culture,sexual orientation,and cause of death. 

For this JSON version, there is an option to let the exporter automatically import the tree for you while also including faith and traits icons that corresponds to each character. The faith and traits icons in the game file will be converted in pngs which will be made in the directory of the exporter.   


Documentations on how to use Gramps can be found here https://gramps-project.org/wiki/ and the download link for Gramps can be found here https://gramps-project.org/blog/download/.

## Step 1: Setting Up The Exporter  ##

1. Clone the entire repo and extract it somewhere in your computer. Within it, the traits and avatar folder should not be modified because they are necessary to run the program. There is also the ck3.json executable that will be called by the exporter to convert your save into a JSON file.

2. Copy and move your ck3 save file in the same folder as the program. There is no need to extract them as the program will do that automatically if needed.

## Step 2: Setting Up Gramps

3. Download Gramps from https://gramps-project.org/blog/download/ and install it. Once installed, you will be prompted to make a family tree. Opt out of this for now.

4. If not done already, go to Edit->Preferences->General tab and click on the Check for updated addons now button. Choose download all addons to get the most out of Gramps.

5. Close the program for now. If you leave it running on the background it will prevent the exporter from using its features.

## Step 3: Convert Your Save Into A JSON File  ##

7.Run the exporttree.exe file. You will encounter a menu with several options. For the first time you are working with the save you need to pick option 1 to convert your save into a JSON file. This type of file allows us to quickly parse through many lines of text at tremendous speeds.

8. You will be prompted to indicate whether the save is an ironman or normal save. Then, provide the name of your ck3 file (eg. mysave.ck3)

9. Let the program convert your file. It should no longer than 15 seconds to get a JSON file. Hit the enter key when it's done when prompted to return to the main menu

## Step 4: Export Your Family Tree Into A CSV file  ##

10. Pick option 2 to extract family tree information into a CSV format. You will be prompted to provided the name of the JSON as well as the game directory. **"C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game** is the usual directory for steam releases. The exporter needs this directory to utilize the localization files to convert the values or keys into readable English.

11. The process will create a folder called pickle. The pickled files inside are basically savedata for when you choose to run the program again. That way, you will only have
to enter your game directory once and all the game information the exporter needs are loaded instantly from the pickled files. 

12. Input the Dynasty/House of the character and the character's id  that you want to start your tree from when prompted. The character's id can be found by running CK3 in debug mode or by looking in the savefile. Then, decide if you want to include Cadet Members' offspring. Note that the character you choose is where the tree will start from. Extended
families will not be included. If you want everyone in the dynasty, pick the dynasty founder as the base instead.

13. Confirm your input to start the script. The script should run and display the processed characters on the screen so that you can monitor progress. This will finish very
quickly.

14.  A CSV file should be created in the same directory as the script along with the pickled files for faster uses in the future. You can manually import 
this CSV file as is using https://gramps-project.org/wiki/index.php/Gramps_5.1_Wiki_Manual_-_Manage_Family_Trees:_CSV_Import_and_Export. 

15. Proceed to the next option to automatically import Gramps with faith and traits icons for each character. 

## Step 5: Convert Your CSV File Into A Gramps-XML To Include Image Information And Automatically Importing Into Gramps  ##

16. For this step, it is important that Gramps is not running in the background. Otherwise, the program will get an error or hang.

17. You will need to first provide the name of your CSV file and the Gramps directory where the executable is stored. This is usually **C:\Program Files\GrampsAIO64-5.1.3\**.

18. Next, for first time use of the exporter, you will need to enter your game directory. Two folders with faith and traits .png images will be created in your directory.

19. A Gramps-XML file will be created through Gramps command line features. The exporter will work off from this XML by adding links to the images in your directory
and attaching it to every character that has those faiths or traits.

20. The exporter will prompt you if you want to change your family tree name from the default YourDynasty_Tree name. Note that if you already have a tree in Gramps with the same name, it will overwrite it. Be sure to change the tree name if that is the case.

21. The import to Gramps will be done automatically in the background. Simply wait until completion. You may exit the exporter after completing this step. 
  
## Step 6: Run Gramps  ##

22. Start Gramps. The program will now dispaly your tree in the managing family tree pop up that appears when you first start the program. Click on that to open your tree.

23. The program has many features that you can read about in the Gramps wiki https://www.gramps-project.org/wiki. You can use its many charts to view your tree, including
pedigree, fan charts, and graphview. You can use the person tab to view each character's information. You can also play around with the tools that you can you use to personalize
your tree styles and export them into pdf or png form. Lastly, you can export your tree to other formats. The XML format that includes media is especially useful if you're
transferring family tree to another computer or sharing with friends.

24. Once you confirm that the import goes through you can delete your Gramps-XML and CSV file if you wish. You can delete the JSON file as well if you're not using it to extract other dynasties in your save.The JSON file can be used to make family trees with other dynasties in your save. 

## Step 8: Troubleshooting ##
Any errors that may come up are displayed on the exporter window as well as in log file called error.log located in the exporter folder. You may use this information to fix it yourself or post in it the issues or discord server for discussion.

As previously stated, future use of the exporter will use the pickle folder to quickly load all information regarding game information and saves. IF you encounter
any unknown problems, deleting this folder and starting a clean session would usually fix it.

## Future Plans ##
~~There are many innovations that are in the works. The most glaring feature missing is coat of arms, which is difficult to implement because of a lack of a COA editor/creation tool that generates a COA with several numeric values and files.~~ As of version 2.0, the exporter will be exporting coat of arms! 

-Depiction of spousal relation and spouses

-Portraits

A near future implementation is a stats report that include information on top Faiths,Traits, and other data. They can be manually done in Gramps  using the native filter app, but can be hard to navigate through if you don't know what you're looking for.

## Contacts ##

For any questions, concerns, and sharing the love for Crusader Kings 3, you can join the discord server here https://discord.gg/MKFDUNtPFB.


