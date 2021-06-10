#*****************************************************************************
#* Copyright ©2021. Radiocrafts AS (Radiocrafts).  All Rights Reserved. 
#* Permission to use, copy, modify, and distribute this software and 
#* its documentation, without fee and without a signed licensing 
#* agreement, is hereby granted, provided that the above copyright 
#* notice, this paragraph and the following two paragraphs appear in 
#* all copies, modifications, and distributions.
#* 
#* IN NO EVENT SHALL RADIOCRFTS BE LIABLE TO ANY PARTY FOR DIRECT, 
#* INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING 
#* LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS 
#* DOCUMENTATION, EVEN IF RADIOCRAFTS HAS BEEN ADVISED OF THE 
#* POSSIBILITY OF SUCH DAMAGE. 
#* 
#* RADIOCRAFTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT 
#* NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND 
#* FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING 
#* DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". 
#* RADIOCRAFTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, 
#* UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#****************************************************************************/

# XMODEM sender implementation

def send(ser, file):
    """
    Send a file over XMODEM protocol
    """
    SOH = b'\x01'
    EOT = b'\x04'
    ACK = b'\x06'
    NAK = b'\x15'
    CAN = b'\x18'
    t = 0

    while 1:
        b = ser.read(1)
        if b != NAK:
            t = t + 1
            if t == 60 : return False
        else:
            break

    print ("\rStart transfer:")
    seq = 1
    data = bytearray(file.read(128))
    while data:
        data = data + b'\xFF'*(128 - len(data))

        checksum = 0
        for c in data:
            checksum += c
        checksum %= 256

        seq_8bit = seq & 0xFF

        while 1:
            frame = bytearray()
            frame += SOH
            frame.append(seq_8bit)
            frame.append(255 - seq_8bit)
            frame += data
            frame.append(checksum)

            if (ser.in_waiting > 0):
                print ("remaining input:", ser.read(ser.in_waiting))
            ser.write(frame)
            ser.flush()

            answer = ser.read(1)
            if answer == NAK: 
                print ("N", end='', flush=True)
                continue
            elif answer == ACK: 
                print (".", end='', flush=True)
                break
            
            ## received an unrecognized byte
            print (seq, answer)
            return False

        data = bytearray(file.read(128))
        seq += 1

    ser.write(EOT)
    ser.flush()

    print ("\rEnd transfer")
    return True

