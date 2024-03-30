run:
	docker compose run pvoronoi python3 main.py

time:
	docker compose run pvoronoi time python3 main.py

clean:
	docker compose down --volumes --rmi=all
