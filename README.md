# Car Prices Tool
![main](https://user-images.githubusercontent.com/59567076/113201894-5f6b7a80-926a-11eb-997f-543550f80b07.png)
<br><br>
I decided to create this project to further train my programming skills. My goal was to create a “base” for mockup SaaS (service as a subscription) website.
<br><br>
First, I decided that my “product” will be cars selling related data. I decided to use Scrapy to scrape a lot of data from one of the most popular websites that deals in selling cars from both private people and companies.
<br><br>
After the script was working and saving proper data in a proper way I decided to further optimize this workflow. I bought some proxy IPs and used scripts that will rotate both IPs and user agents to not get me banned. I didn’t want to cause troubles to website servers so I decided to create a Docker container with it and host this on VPS (where I made scraping slower and therefore longer but more server friendly by enabling throttling).
<br><br>
After I had all the data (over 198 000 entries) I created a Django website where I further enhanced my “product” by offering searches through my data with advanced filters and some graphs and charts (thanks Chart.js !). I created both Free and Paid ranks with different amounts of features.
<br><br>
After that, as the most expensive “Tier” I decided to create an API with Django REST and give users the possibility to access database through both URL and CURL requests.
<br><br>
And as a final touch I hosted it on PythonAnywhere where you can view whole website - https://carpricestool.eu.pythonanywhere.com
<br><br>
Cheers!
<br><br>
Some additional screenshots:
<br><br>
![screen_1](https://user-images.githubusercontent.com/59567076/113201900-609ca780-926a-11eb-9fce-09bb91faa26d.png)
![screen_2](https://user-images.githubusercontent.com/59567076/113201901-61cdd480-926a-11eb-8905-08e3cf6fe1b2.png)
![screen_3](https://user-images.githubusercontent.com/59567076/113201902-61cdd480-926a-11eb-81a2-486bcb84a46b.png)
<br><br>
Thank You :-)
