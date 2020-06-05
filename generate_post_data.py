import post_data_pb2, sys, os

def bin2base64(bin_string):
    base64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    split = ["00" + bin_string[i:i + 6] for i in range(0, len(bin_string), 6)]
    # print(split)
    result = ""
    for b in split:
        if len(b) == 6:
            b += "00"
            result += base64_alphabet[int(b, 2)]
            result += "="
        elif len(b) == 4:
            b += "0000"
            result += base64_alphabet[int(b, 2)]
            result += "=="
        else:
            result += base64_alphabet[int(b, 2)]
    # print(result)
    return result

def run(DST=os.getcwd() + "/post_data_base64.out", PB_DST = os.getcwd() + "/post_data.pb", write=False):
    #write = False
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: python", sys.argv[0], "<USER_ID>") # , "(<OUTPUT_FILE_PATH>)")
        sys.exit(-1)

    if len(sys.argv) > 1:
        USER_ID = sys.argv[1]
        if len(sys.argv) == 3:
            write = True
            if os.path.isfile(sys.argv[2]):
                DST = sys.argv[2]
            else:
                #print("Invalid path. Will write to:", DST)
                pass
    else:
        USER_ID = "G:195671346"

    userdata = post_data_pb2.userdata()
    userdata.user_id = USER_ID
    userdata.f1 = 0
    userdata.f2 = 1

    data = userdata.SerializeToString()

    if write:
        print("Wrote brotobuf post data to:", PB_DST)
        f = open(PB_DST, "wb")
        f.write(data)
        f.close()

    data = ''.join(bin(x)[2:].zfill(8) for x in list(data))
    POST_data = bin2base64(data)

    if write:
        print("Wrote brotobuf base64 post data to:", DST)
        f = open(DST, "w")
        f.write(POST_data)
        f.close()

    return POST_data

if __name__ == '__main__':
    run(write=True)