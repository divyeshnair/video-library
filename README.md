# video-library
Video library is project developed to scrape youtube videos.
This project has been developed in python Flask. the database used is
Sqlite.

* Steps to run this project
    * Local machine 
      * Install sqlite - https://www.sqlite.org/download.html
      * Create a new database with database name as - "video_library"
      * Create the database in the database folder of this repository
      * Install the requirements for this project by running the command - pip
        install -r requirements.txt
      * Export environment variable for youtube api credentials. The command
        for that is - export YOUTUBE_KEYS = '[]'. example - 
        export YOUTUBE_KEYS = '["123avbvgbg"]'
      * Apply the database changes by running the command - python manager.py db upgrade
      * Start the server by running the command - python manage.py server
    
    * Docker
      * The docker folder has a docker file in it. Build the docker image by running
        the following command - 
        
      * Apply the database changes by running this command-
        docker run -e YOUTUBE_KEYS='[(enter-your-keys)]' 
        -v <your-host-machine-database-path>:/video-library/database 
        video-library:1.0.0 python manage.py db upgrade
        
      * Start the server by running the command - 
        docker run -e YOUTUBE_KEYS='[(enter-your-keys)]' 
        -v <your-host-machine-database-path>:/video-library/database 
        video-library:1.0.0 python manage.py server --host=0.0.0.0
        
* APIs

1. - endpoint - videos
   - method - GET
   - params - 
        1. page_number - integer
        2. records_per_page - integer
    
    
2. - endpoint - videos/search 
   - method - POST 
   - json - 
        1. search_query - string
 
        