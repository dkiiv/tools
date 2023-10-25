#!/usr/bin/python

#init, verifies modules are installed, if theyre not it will auto install them
def init():
    try:
        from OpenSSL import crypto
    except ImportError:
        import pip
        pip.main(['install', 'pyOpenSSL'])
init()
from OpenSSL import crypto
import os
import sys

#Variables
TYPE_RSA = crypto.TYPE_RSA
TYPE_DSA = crypto.TYPE_DSA
HOME = os.getenv("HOME")

#Pull these out of scope
key = crypto.PKey()

#Generate the key
def generatekey(cn):
    keypath = "certs/" + cn + "/" + cn + '.key'
    if os.path.exists(keypath):
        print (cn + " Key file exists, skipping.")
    else:
        key.generate_key(TYPE_RSA, 4096)
        f = open(keypath, "wb")
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
        f.close()

#Generate CSR
def generatecsr(cn):
    csrpath = "certs/" + cn + "/" + cn + '.csr'

    c = 'CHANGEME'
    st = 'CHANGEME'
    l = 'CHANGEME'
    o = 'CHANGEME'
    ou = 'CHANGEME'

    #Setting the configuration data for the CSR
    req = crypto.X509Req()
    req.get_subject().CN = cn
    req.get_subject().C = c
    req.get_subject().ST = st
    req.get_subject().L = l
    req.get_subject().O = o
    req.get_subject().OU = ou
    req.set_pubkey(key)
    req.sign(key, "sha256")

    #Check if CSR is already present, skip if so
    if os.path.exists(csrpath):
        print (cn + " CSR File Exists, skipping.")
    else:
        f = open(csrpath, "wb")
        f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req))
        f.close()

#Generate PFX
def generatepfx(cn, out_pfx, private_key_file, certificate_file, intermediates_file, passphrase=None):
    #Set the proper directory
    out_pfx = "certs/" + cn + "/" + out_pfx
    private_key_file = "certs/" + cn + "/" + private_key_file
    certificate_file = "certs/" + cn + "/" + certificate_file
    intermediates_file = "certs/" + cn + "/" + intermediates_file

    #Load the private key
    with open(private_key_file, "rb") as f:
        private_key_data = f.read()
    private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key_data, passphrase)

    #Load the certificate
    with open(certificate_file, 'rb') as f:
        certificate_data = f.read()
    certificate = crypto.load_certificate(crypto.FILETYPE_PEM, certificate_data)

    #Create a PKCS12 object
    p12 = crypto.PKCS12()

    #Set the private key and certificate
    p12.set_privatekey(private_key)
    p12.set_certificate(certificate)

    #Add intermediates/root certificates
    with open(intermediates_file, 'rb') as f:
        intermediates_data = f.read()
    intermediates = crypto.load_certificate(crypto.FILETYPE_PEM, intermediates_data)
    p12.set_ca_certificates([intermediates])

    #Export the PKCS12 data
    p12_data = p12.export(passphrase=passphrase)

    #Write the PKCS12 data to the output PFX file
    with open(out_pfx, 'wb') as pfx_file:
        pfx_file.write(p12_data)
        pfx_file.close()