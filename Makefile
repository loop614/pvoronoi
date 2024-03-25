run:
	docker compose run --rm pvoronoi python3 main.py

clean:
	docker compose down --volumes --rmi=all
