import csv
import urllib.request
import time

def download_img(url, file_name):
    file_name = clean_name(file_name)
    try:
        urllib.request.urlretrieve(url, f"./output/{file_name}.jpg")
        print(f"Wrote {file_name} to file")
    except OSError as e:
        print (f"Error downloading image {file_name}.jpg")

def get_data(img_id):
    with open("objects.csv", encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            if i[0] == "objectid":
                continue
            if i[0] == img_id:
                title = i[4]
                date = i[5]
                artist = i[14]
                medium = i[9]
                file_name = f"{artist} -- {title} ({date}), {medium}"
                return file_name
        csv_file.close()

def clean_name(file_name):
    forbidden_chars = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
    for i in forbidden_chars:
        if i in file_name:
            if i == ":":
                file_name = file_name.replace(i, "-")
            elif i == "?":
                file_name = file_name.replace(i, "unknown")
            elif i == "\"":
                file_name = file_name.replace(i, "'")
            elif i == "/":
                file_name = file_name.replace(i, "-")
            else:
                file_name = file_name.replace(i, "#")
    return file_name

def warn():
    print("WARNING: This will attempt to download ALL images in the entire NGA archive totaling over 137,000 files")
    time.sleep(1)
    print("Downloading will begin in 3 seconds")
    time.sleep(1)
    print("If you would like to cancel this operation press Ctrl + C at any time")
    time.sleep(2)
    print("Beginning download...")
    dl_all()

def dl_all():
    with open("published_images.csv", encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            if i[0] == "uuid":
                continue
            base_url = i[1]
            add = "/full/full/0/default.jpg"
            url = base_url + add
            file_name = get_data(i[10])
            download_img(url, file_name)
        csv_file.close()

def dl_by_format():
    art_format = input("Enter the format of the art you would like to download. Valid formats are: painting, drawing, print, photograph sculpture, volume\n")
    valid_formats = ["painting", "drawing", "sculpture", "print", "volume", "photograph"]
    if art_format not in valid_formats:
        print("Error: Format is invalid.")
        dl_by_format()
    img_list = []
    with open("objects.csv", encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            if i[0] == "objectid":
                continue
            if i[19] == art_format:
                img_list.append(i[0])
        print(f"Successfully found all all ids of format '{art_format}', beginning download.")
        get_imgs_from_id(img_list)
        csv_file.close()

def dl_artist():
    artist = input("Enter the name of the artist you would like to download. FORMAT: First Last\n")
    img_list = []
    with open("objects.csv", encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            if i[0] == "objectid":
                continue
            if i[14] == artist:
                img_list.append(i[0])
        if len(img_list) == 0:
            print(f"Hmm, it seems artist's name is either spelled incorrectly or the artist does not exist. No images of artist name {artist} found...")
            print("Please know that some artist names are not correctly encoded in the database. For example Paul Cézanne is stored as Paul CÃ©zanne")
        print(img_list)
        get_imgs_from_id(img_list)
        csv_file.close()

def get_imgs_from_id(img_ids):
    with open("published_images.csv", encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            if i[0] == "uuid":
                continue
            if i[10] in img_ids:
                base_url = i[1]
                add = "/full/full/0/default.jpg"
                url = base_url + add
                file_name = get_data(i[10])
                download_img(url, file_name)
        csv_file.close()
    print("Done.")

def main():
    mode = input("Enter a dl mode. g = download all, a = download by artist name, f = download by format\n")
    if mode == "g":
        warn()
    elif mode == "a":
        dl_artist()
    elif mode == "f":
        dl_by_format()

if __name__ == "__main__":
    main()