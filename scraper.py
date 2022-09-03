import csv
import urllib.request

# THIS IS A WIP AND DOES NOT WORK YET

def download_img(url, file_name):
    try:
        # MAKE IT NOT OVERRIDE FILES OF SAME NAME
        urllib.request.urlretrieve(url, f"./output/{file_name}.jpg")
        print(f"Wrote {file_name} to file")
    except OSError as e:
        print("!!")
        download_img(url, clean_name(file_name))

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
                file_name = f"{artist} -- {title} ({date})"
                return file_name

def clean_name(file_name):
    # DOESNT WORK. JUST TITLES FILE "NONE.JPG" FOR SOME REASON.
    forbidden_chars = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
    for char in file_name:
        if char in forbidden_chars:
            if char == "?":
                char = "unknown"
            else:
                char = "#"

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