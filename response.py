import pickle
import random


def random_text():
    with open('grandpa.pickle', 'rb') as f:
        grandpa_list = pickle.load(f)
    one_day = random.choice(grandpa_list)
    message = ""
    message += one_day['date'] + "\n"
    for k, v in one_day['text'].items():
        message += k + ": " + v + "\n"
    # print(message)
    return message


def one_word():
    with open('grandpa.pickle', 'rb') as f:
        grandpa_list = pickle.load(f)
    one_day = random.choice(grandpa_list)
    message = ""
    message += one_day['date'] + "\n"
    flag = False
    while not flag:
        one_day = random.choice(grandpa_list)
        message = one_day['date'] + "\n"
        res = [v for k, v in one_day['text'].items() if "一言" in v]
        if len(res) > 0:
            message += res[0]
            flag = True


if __name__ == '__main__':
    random_text()
