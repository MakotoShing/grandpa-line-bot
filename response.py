import pickle
import random
from PIL import Image, ImageDraw, ImageFont
import os


def random_text():
    with open('grandpa.pickle', 'rb') as f:
        grandpa_list = pickle.load(f)
    one_day = random.choice(grandpa_list)
    message = ""
    message += one_day['date'] + "\n"
    for k, v in one_day['text'].items():
        message += k + ": " + v + "\n"
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
    message = message.replace("\"", "")
    return message


# send images
# https://qiita.com/tamago324/items/4df361fd6ac5b51a8a07
def date_the_image(src: str, desc: str, size=800) -> None:
    # 開く
    im = Image.open(src)

    # 800 x Height の比率にする
    if im.width > size:
        proportion = size / im.width
        im = im.resize((int(im.width * proportion), int(im.height * proportion)))
    im.save("./static/image.jpeg")


def update_ids():
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive

    # OAuth認証を行う
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)

    drive_folder_id = "10rl0NFWtlAkL0kMzCvTZNuzYM_Mj-E5j"

    file_list = drive.ListFile().GetList()
    id_list = []
    for f in file_list:
        if f['title'][-3:] in ['jpg', 'png']:
            id_list.append(f['id'])
    with open("./image_ids.pickle", "wb") as f:
        pickle.dump(id_list, f)


def upload_image(path, filename):
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive

    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)

    # im = Image.open(path)
    # size = 800
    # if im.width > size:
    #     proportion = size / im.width
    #     im = im.resize((int(im.width * proportion), int(im.height * proportion)))
    # os.remove(path)
    # im.save(path)

    f = drive.CreateFile({'title': filename, 'mimeType': 'image/jpeg'})
    f.SetContentFile(path)
    f.Upload()
    # update_ids()
    # remove image
    os.remove(path)


def random_id():
    with open('image_ids.pickle', 'rb') as f:
        image_ids = pickle.load(f)
    image_id = random.choice(image_ids)
    return image_id
