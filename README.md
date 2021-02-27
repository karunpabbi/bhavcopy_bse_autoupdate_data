# bhavcopy_bse_autoupdate_data
BhavCopy andlysis using django , vue , redis 




Containerized solution for Analysing BHav Copy from BSE :

Docker images can be run using below commands:


	sudo docker run  --restart always -d -it --name bahvcopy-dango -v /home/kpabbiofficials/:/home -p 80:8000  pabbikarun/bahvcopy-ready_to_host python3 /home/bhavcopy_forCSV_UPLOAD/manage.py runserver 0.0.0.0:8000


	sudo docker exec -d bahvcopy-dango redis-server


	sudo docker run --restart always -d -it --name bahvcopy-scheduler pabbikarun/bahvcopy-scheduler python3 home/scheduler_to_update_data.py
