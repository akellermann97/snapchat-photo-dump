from datetime import datetime
import json
import requests
import time
from PIL import Image
from exif import Image as EImage
from exif import DATETIME_STR_FORMAT
from io import BytesIO

"""
Notes from using CURL before building the Python script.
If you use curl, the command would be something like: 

`curl -d "
uid=[data]&
mid=[data]&
ts=[data]&
proxy=[true|false]&
sig=[data]" 
-X POST https://app.snapchat.com/dmd/memories`

You can find these long URLS in the memories.html snapchat gives you
when you request your information. When you POST this URL it gives you a AWS based url, 
where you can finally download the image. There's no EXIF data included. The snapchat app
goes have DATE/TIME/GPS information (or at least up to the city the picture was taken), 
but unfortunately, I was only able to figure out how to add back the DATE/TIME information.

PITFALLS:
The Date/Time information this script adds back to the JPEG is off. I don't know exactly why. 
One possible reason: I don't correctly copy the fact that all these timestamps are in UTC, when I was taking
them at UTC-5
Or Snapchat just stores incorrect time values, but it's probably the timezone issue. Either way, it's enough for 
me to just have the GENERAL time that the picture was taken, so it shows up more or less appropriately in photo cataloging
software at the right time.
"""


def main():
    # Open JSON file
    # Parser JSON

    headers = {"Content-type": "application/x-www-form-urlencoded"}
    fd = open("memories_history.json")
    memories = json.load(fd)
    for x in memories["Saved Media"]:
        if x["Media Type"] == "PHOTO":
            url = x["Download Link"]
            split_url = url.split("?")
            r = requests.post(
                split_url[0],
                headers=headers,
                data=split_url[1],
            )
            if r.status_code == 200:
                # 200 means that we got HTTP success
                aws_resp = requests.get(r.text)
                aws_url = r.text.split("?")
                print(aws_url[0])
                last_occur = aws_url[0].rfind("/", 0) + 1
                print(last_occur)
                filename = aws_url[0][last_occur:]
                i = Image.open(BytesIO(aws_resp.content))
                i = i.save(filename, quality="keep")
                time.sleep(1)
                # Prepare the datetime info
                date_datetime = datetime.strptime(x["Date"], "%Y-%m-%d %H:%M:%S %Z")
                with open(filename, "rb") as image_file_thing:

                    image_file = EImage(image_file_thing)
                    image_file.datetime_original = date_datetime.strftime(
                        DATETIME_STR_FORMAT
                    )
                    image_file.datetime_scanned = date_datetime.strftime(
                        DATETIME_STR_FORMAT
                    )
                    image_file.datetime_digitized = date_datetime.strftime(
                        DATETIME_STR_FORMAT
                    )

                    with open("{}_akk.jpg".format(filename), "wb") as new_image_file:
                        new_image_file.write(image_file.get_file())

            else:
                print(r.status_code)
                exit()

    fd.close()


"""
You cannot just download photos using the URL directly. Instead, snapchat
uses this horrible system to dynamically generate a URL where you can find
your pictures. 

Here is the javascript that they use to download the pictures

            function downloadMemories(url) {
                var parts = url.split("?");
                var xhttp = new XMLHttpRequest();
                xhttp.open("POST", parts[0], true);
                xhttp.onreadystatechange = function() {
                    if (xhttp.readyState == 4 && xhttp.status == 200) {
                        var a = document.createElement("a");
                        a.href = xhttp.responseText;
                        a.style.display = "none";
                        document.body.appendChild(a);
                        a.click();
                        document.getElementById("mem-info-bar").innerText = "";
                    } else if (xhttp.readyState == 4 && xhttp.status >= 400) {
                        document.getElementById("mem-info-bar").innerText = "Oops!                 Something went wrong. Status " + xhttp.status
                    }
                };
                xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                xhttp.send(parts[1]);
            }
"""

if __name__ == "__main__":
    main()