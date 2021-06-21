imagename = tiktokfeed_prep
app_imagename = tiktokfeed_app

image:
	docker build -t $(imagename) -f Dockerfile .

image_app:
	docker build -t $(app_imagename) -f Dockerfile_app .

data/chat.db: config/config.yaml
	cp $(shell cd; pwd)/Library/Messages/chat.db data/chat.db

data/initial.json: data/chat.db config/config.yaml
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ $(imagename) run.py acquire --input=data/chat.db --config=config/config.yaml --output=data/initial.json
	rm data/chat.db

data/app.db: data/initial.json config/config.yaml
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ $(imagename) run.py initialize --input=data/initial.json --config=config/config.yaml --output=data/app.db

database: data/app.db

app:
	docker run -p 8000:8000 $(app_imagename)

.PHONY: image image_app database app