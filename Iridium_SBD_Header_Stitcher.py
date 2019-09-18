# Recursively stitches all sbd files in subdirectories into one csv file

import os

fp = open('SBD_headers_stitched.csv', 'wb')
print('Stitching sbd .txt file headers into SBD_headers_stitched.csv')

for root, dirs, files in os.walk("."):
    if len(files) > 0:
        # if root != ".": # Only check sub-directories
        if root == ".":  # Only check this directory
            for filename in files:
                if filename[-4:] == '.txt':
                    longfilename = os.path.join(root, filename)
                    rxtime = filename[0:8] + ' ' + filename[9:17] + ','
                    print('Processing', longfilename)
                    fp.write(rxtime.encode("utf-8"))
                    fr = open(longfilename, 'r')
                    for line in fr:
                        words = line.split()
                        if len(words) >= 2:
                            if words[0] == "MOMSN:":
                                # Mobile Originated Message Sequence Number
                                fp.write((words[1]+',').encode("utf-8"))
                            if words[0] == "MTMSN:":
                                # Mobile Terminated Message Sequence Number
                                fp.write((words[1]+',').encode("utf-8"))
                        if len(words) >= 8:
                            if (words[0] == "Time") and (words[2] == "Session"):
                                fp.write((words[4]+' ').encode("utf-8"))  # Session Day
                                fp.write((words[5]+' ').encode("utf-8"))  # Session Month
                                fp.write((words[6]+' ').encode("utf-8"))  # Session Date
                                fp.write((words[8]+' ').encode("utf-8"))  # Session Year
                                fp.write((words[7]+',').encode("utf-8"))  # Session Time
                        if len(words) >= 12:
                            # Possibly redundant?
                            if (words[9] == "Session") and (words[10] == "Status:"):
                                fp.write((words[11]+',').encode("utf-8"))  # Session Status
                        if len(words) >= 8:
                            if (words[0] == "Unit") and (words[1] == "Location:"):
                                fp.write((words[4]+',').encode("utf-8"))  # Lat
                                fp.write((words[7]+',').encode("utf-8"))  # Lon
                        if len(words) >= 3:
                            if (words[0] == "CEPradius"):
                                fp.write((words[2] + ",").encode("utf-8")) # CEPradius
                    fp.write('\r\n'.encode("utf-8"))
                    fr.close()

fp.close()
