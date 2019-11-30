def main():
    with open("./chat.txt") as f:
        lines = f.readlines()

    grandpa_mess = []
    tmp_message = ""
    flag = 0
    for line in lines:
        try:
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


if __name__ == '__main__':
    main()
