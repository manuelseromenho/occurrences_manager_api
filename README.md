# Occurrences Manager Api exercise


#### API Rest that enables the possibility of managing an urban area occurrences.

    #Build docker container
	docker-compose build
	
	#Up docker, first db then api
	docker-compose up db
	docker-compose up api
	
	#Run the migrations
	docker-compose exec api python manage.py migrate
	
	#Load initial data (base occurrence categories)
	docker-compose exec api python manage.py loaddata initial
	
	#Create first admin user
	docker-compose exec api python manage.py initadmin
	
