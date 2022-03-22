# Official Python 3 Docker image.
FROM python:3

WORKDIR /car_prices_tool_scraping
 
# Copy the file from the local host to the filesystem of the container at the working directory.
COPY car_prices_tool_scraping/car_prices_tool_scrapy/requirements.txt ./
 
# Install requirements.txt.
RUN pip3 install --no-cache-dir -r requirements.txt
 
# Copy the project source code from the local host to the filesystem of the container at the working directory.
COPY car_prices_tool_scraping .

# CMD [ "python", "spiders/run_CARS_PL_source_1.py" ]