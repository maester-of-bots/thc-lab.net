import OpenSSL


def convert_ssl_certificate(input_file, output_file, output_format):
    with open(input_file, 'rb') as f:
        certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())

    if output_format == 'PEM':
        certificate_data = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)
    elif output_format == 'DER':
        certificate_data = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_ASN1, certificate)
    elif output_format == 'PFX':
        p12 = OpenSSL.crypto.PKCS12()
        p12.set_certificate(certificate)
        p12_data = p12.export()
        with open(output_file, 'wb') as f:
            f.write(p12_data)
        return

    with open(output_file, 'wb') as f:
        f.write(certificate_data)

    print(f"Certificate converted to {output_format} format and saved to {output_file}")


input_file = 'certificate.pem'
output_file = 'converted_certificate.pem'
output_format = 'DER'
convert_ssl_certificate(input_file, output_file, output_format)
