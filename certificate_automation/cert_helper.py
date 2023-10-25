#!/usr/bin/python

# Ensure there are no whitespaces in the feed CSV file, they will generate errors

# Instructions:
# Run the first time to generate CSR + private key for all entries in the target CSV
# Run a second time after placing certificate, and intermediates/root certificates into the device's directory to generate a PFX

import csv
import os
import openSSL_gen

openSSL_gen.init()
with open("device_certs.csv", "r") as file:
    names = csv.reader(file)
    for row in names:
        path = f"certs\{row[0]}"
        commonName = row[0]
        present = os.path.exists(path)
        if not present:
            os.makedirs(path)
            try:
                openSSL_gen.generatekey(commonName)
                openSSL_gen.generatecsr(commonName)
            except Exception as e:
                print(commonName + " encountered an error: " + repr(e))
        else:
            cert = commonName.replace(".", "_")
            if (os.path.exists(path + "\\" + cert + "_cert.cer") and
            os.path.exists(path + "\\" + cert + "_interm.cer")):
                try: 
                    openSSL_gen.generatepfx(commonName, commonName + ".pfx", commonName + ".key",
                                            cert + "_cert.cer", cert + "_interm.cer")
                except Exception as e:
                    print(commonName + " PFX generatation encountered an error: " + repr(e))
            else:
                print(commonName + " missing files for PFX generation")
    print("Done")