# As Scrapy runs on Python, I choose the official Python 3 Docker image.
FROM python:3

# WORKDIR /
 
# Copy the file from the local host to the filesystem of the container at the working directory.
COPY car_prices_tool_scrapy/requirements.txt ./
 
# Install Scrapy specified in requirements.txt.
RUN pip3 install --no-cache-dir -r requirements.txt
 
# Copy the project source code from the local host to the filesystem of the container at the working directory.
COPY car_prices_tool_scrapy .
 
CMD [ "python", "spiders/run_CARS_PL_otomoto.py" ]