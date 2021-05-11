## XMODEM sender implementatino

def send(ser, file):
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

