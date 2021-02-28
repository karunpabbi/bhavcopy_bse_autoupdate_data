# bhavcopy_bse_autoupdate_data

TASKS PERFORMED :
- Downloads the equity bhavcopy zip from the above page every day at 18:00 IST for the current date.
- Extracts and parses the CSV file in it.
- Writes the records into Redis with appropriate data structures (Fields: code, name, open, high, low, close).
- Renders a simple VueJS frontend with a search box that allows the stored entries to be searched by name and renders a table of results and optionally downloads the results as CSV. Make this page look nice!
- The search needs to be performed on the backend using Redis.




Containerized solution for Analysing BHav Copy from BSE :

Docker images can be run using below commands:


	sudo docker run  --restart always -d -it --name bahvcopy-dango -v /home/kpabbiofficials/:/home -p 80:8000  pabbikarun/bahvcopy-ready_to_host python3 /home/bhavcopy_forCSV_UPLOAD/manage.py runserver 0.0.0.0:8000


	sudo docker exec -d bahvcopy-dango redis-server


	sudo docker run --restart always -d -it --name bahvcopy-scheduler pabbikarun/bahvcopy-scheduler python3 home/scheduler_to_update_data.py
