# Recursively stitches all sbd files into one csv file
# Reads Iridium Session Times from SBD_headers_stitched.csv
# Needs at least two sbd files to work properly

import os
import numpy as np
import struct

try:
    momsns = np.loadtxt('SBD_headers_stitched.csv',
                        delimiter=',', unpack=True, usecols=(1,))
    session_times = np.genfromtxt(
        'SBD_headers_stitched.csv', delimiter=',', unpack=True, usecols=(3,), dtype='str')
except:
    raise Exception('Could not process SBD_headers_stitched.csv!')

fp = open('SBD_stitched.csv', 'wb')
csv_header = str("rxtime, session_time, msn, msg_id, flight_state, flight_substate, timestamp, lat, long, gnss_alt, gnss_time, pressure_alt, bat_voltage, ign1_con, ign1_fired, ign2_con, ign2_fired, ign3_con, ign3_fired, ign_hp_con, ign_hp_fired\r\n");  
fp.write(csv_header.encode("utf-8"))
print('Stitching sbd files into SBD_stitched.csv')
# print 'Using momsns:'
# print momsns
# print 'Using session_times:'
# print session_times

for root, dirs, files in os.walk("."):
    if len(files) > 0:
        # if root != ".": # Only check sub-directories
        if root == ".":  # Only check this directory
            for filename in files:
                if filename[-4:] == '.sbd':
                    longfilename = os.path.join(root, filename)
                    msn = longfilename[-10:-4] + ','
                    rxtime = filename[0:8] + ' ' + filename[9:17] + ','
                    msnum = float(longfilename[-10:-4])
                    session_time = ''
                    for index, seqnum in enumerate(momsns):
                        if seqnum == msnum:
                            session_time = session_times[index] + ','
                    if session_time != '':
                        print('Appending', longfilename)
                        fp.write(rxtime.encode("utf-8"))
                        fp.write(session_time.encode("utf-8"))
                        fp.write(msn.encode("utf-8"))
                        fr = open(longfilename, 'rb')
                        binary_data = fr.read()                        
                        
                        msg_id = str((binary_data[0] & 0x0F)) + ","
                        flight_state = str((binary_data[0] & 0xC0) >> 6) + ","
                        flight_substate = str((binary_data[0] & 0x30) >> 4) + ","
                        timestamp = str(int.from_bytes(binary_data[1:5], "little")) + ","
                        lat = str(struct.unpack("f", binary_data[5:9])[0]) + ","
                        lon = str(struct.unpack("f", binary_data[9:13])[0]) + ","
                        gnss_altitude = str(struct.unpack("f", binary_data[13:17])[0]) + ","
                        gnss_time_tmp = struct.unpack("I", binary_data[17:21])[0]
                        gnss_time_hr = gnss_time_tmp//3600
                        gnss_time_min = (gnss_time_tmp - gnss_time_hr*3600)//60
                        gnss_time_sec = gnss_time_tmp%60
                        gnss_time = str(gnss_time_hr) + ":" + str(gnss_time_min) + ":" + str(gnss_time_sec) + ","
                        pressure_altitude = str(struct.unpack("f", binary_data[21:25])[0]) + ","
                        battery_voltage = str(struct.unpack("f", binary_data[25:29])[0]) + ","
                
                        igniter_status = str(binary_data[29]) + ","

                        igniter_1_fired = str((binary_data[29] & 0x08) >> 3) + ","
                        igniter_2_fired = str((binary_data[29] & 0x04) >> 2) + ","
                        igniter_3_fired = str((binary_data[29] & 0x02) >> 1) + ","
                        igniter_hpower_fired = str(binary_data[29] & 0x01) + ","

                        igniter_1_connected = str((binary_data[29] & 0x80) >> 7) + ","
                        igniter_2_connected = str((binary_data[29] & 0x40) >> 6) + ","
                        igniter_3_connected = str((binary_data[29] & 0x20) >> 5) + ","
                        igniter_hpower_connected = str((binary_data[29] & 0x10) >> 4) + ","
                        
                        fp.write(msg_id.encode("utf-8"))
                        fp.write(flight_state.encode("utf-8"))
                        fp.write(flight_substate.encode("utf-8"))
                        fp.write(timestamp.encode("utf-8"))
                        fp.write(lat.encode("utf-8"))
                        fp.write(lon.encode("utf-8"))
                        fp.write(gnss_altitude.encode("utf-8"))
                        fp.write(gnss_time.encode("utf-8"))
                        fp.write(pressure_altitude.encode("utf-8"))
                        fp.write(battery_voltage.encode("utf-8"))                       

                        fp.write(igniter_1_connected.encode("utf-8"))
                        fp.write(igniter_1_fired.encode("utf-8"))
                        fp.write(igniter_2_connected.encode("utf-8"))
                        fp.write(igniter_2_fired.encode("utf-8"))
                        fp.write(igniter_3_connected.encode("utf-8"))
                        fp.write(igniter_3_fired.encode("utf-8"))
                        fp.write(igniter_hpower_connected.encode("utf-8"))
                        fp.write(igniter_hpower_fired.encode("utf-8"))
                        
                        fp.write('\r\n'.encode("utf-8"))
                            
                    else:
                        print('Skipping', longfilename,
                              '(Could not match momsn)')
                    fr.close()

fp.close()
