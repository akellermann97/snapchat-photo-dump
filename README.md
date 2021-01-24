# Snapchat-Photo-Dump
Script to add EXIF data back to snapchat memories.

## How it works
When you request all your data from snapchat, in the files snapchat returns
is a json called memories.json. Using that file, you can download every single 
one of your snpachat memories since snapchat started saving them (around 2016 
if your account is that old). I wanted to download them for archival purposes
and there were two problems

1. You have to download them link by link, they don't include all the photos in the
data return by default

2. The photos returned are completely stripped of EXIF data. Ideally I would like them
to have geolocation and datetime information. I couldn't quickly find a way to get geolocation
data, but the date time info is right there in memories.json. 

All you need to do is POST the URL in the memories.json request properly, follow the AWS link where
the photo is hosted (only hosted for 7 days after you make the data request), then manually add the datetime
back into the photo using EXIF tags. 

## Problems
The package I used requires you to make a new JPEG rather than writing EXIF to one that already exists. I didn't write
code to delete the original image, so you'll have to do that manually. 

Timezone information is incorrect. In the software I use to catalog photos, it means that while the photos are taken in UTC
they are not displayed back in the correct timezone (all of these photos for me were taken in UTC-5)