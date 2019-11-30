import pickle


def main():
    with open("./chat.txt") as f:
        lines = f.readlines()

    grandpa_mess = []
    tmp_message = ""
    flag = 0
    for line in lines:
        try:
            # append the date. Format: 2***/00/00 DATE
            if flag == 0 and isinstance(int(line[:4]), int) and line[4] == "/" and isinstance(int(line[5:7]), int) and isinstance(int(line[8:10]), int):
                grandpa_mess.append(line)
                continue
        except:
            pass

        try:
            # starting message from grandpa
            if isinstance(int(line[:2]), int) and line[2] == ':' and isinstance(int(line[3:5]), int) and '\t' in line \
                    and line.split('\t')[1] == '祖父':
                if flag == 1:
                    grandpa_mess.append(tmp_message)
                    tmp_message = line
                else:
                    flag = 1
                    tmp_message = line
            elif isinstance(int(line[:2]), int) and line[2] == ':' and isinstance(int(line[3:5]), int) and len(tmp_message) > 0 and flag == 1:
                grandpa_mess.append(tmp_message)
                flag = 0
        except ValueError:
            if flag == 1:
                tmp_message += line

    # print(len(grandpa_mess))
    # print(grandpa_mess)
    with open("./grandpa_message.txt", mode='w') as f:
        f.writelines(grandpa_mess)


def clean():
    grandpa_mess = []
    with open("./grandpa_message.txt") as f:
        lines = f.readlines()
    for line in lines:
        try:
            if line[-5:-1] == "data" or line[0] == "\"":
                grandpa_mess.append("#"+line)
            elif len(line) < 2:
                continue
            else:
                grandpa_mess.append(line)
        except ValueError:
            if len(line) > 2:
                grandpa_mess.append(line)

    with open("./grandpa_message.txt", mode='w') as f:
        f.writelines(grandpa_mess)


# a function to test for response
def test():
    with open("./grandpa_message.txt") as f:
        lines = f.readlines()
    grandpa_res = []
    tmp_dict = {
        "date": None,
        "text": {}
    }
    tmp_message = ""
    date_flag = 0
    text_flag = 0
    for line in lines:
        try:
            if isinstance(int(line[:4]), int) and line[4] == "/" and isinstance(int(line[5:7]), int) and \
                    isinstance(int(line[8:10]), int):
                if tmp_dict["date"] is not None:
                    grandpa_res.append(tmp_dict)
                    tmp_dict = {
                        "date": None,
                        "text": {}
                    }
                tmp_dict["date"] = line.strip()
                text_flag = 0
                continue
        except:
            pass
        try:
            if line[0] == "#":
                continue
            elif isinstance(int(line[:2]), int) and line[2] == ':' and isinstance(int(line[3:5]), int) and '\t' in \
                    line and line.split('\t')[1] == '祖父':
                time_text = line.split("\t")[0]
                tmp_dict["text"][time_text] = line.split("祖父")[1]
                text_flag = 1
        except ValueError:
            if text_flag == 1 and line[0] != "#":
                tmp_dict["text"][time_text] += line
    print("length: {}".format(len(grandpa_res)))
    # remove unnecessary characters
    for idx, res in enumerate(grandpa_res):
        for k, v in res['text'].items():
            tmp_text = v
            if tmp_text[:1] == "\t":
                tmp_text = tmp_text.split("\t")[1]
            if "\"" in tmp_text:
                tmp_text.replace("\"", "")
            if tmp_text[-1:] == "\n":
                tmp_text = tmp_text[:-2]
            grandpa_res[idx]['text'][k] = tmp_text
    print(grandpa_res)
    with open("./grandpa.pickle", "wb") as f:
        pickle.dump(grandpa_res, f)


def test2():
    import response
    print(response.random_text())


if __name__ == '__main__':
    test2()
    # clean()
