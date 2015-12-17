# inputs

# source code directory
SRC_DIR=.

# local stuff prefix
PREFIX=villlem.develstack.

# name of volume is inferred from directory name
CACHE_VOLUME=$(PREFIX)$(shell basename ${PWD}).cache
DATA_VOLUME=$(PREFIX)$(shell basename ${PWD}).data

# absolute path of the source directory
SRC_VOLUME=$(shell cd $(SRC_DIR); pwd)

# label for project containers (for cleanups)
PROJECT_LABEL=$(PREFIX)$(shell basename ${PWD})

# base develstack image
DEVELSTACK_IMAGE=villlem/develstack:latest

set-empty-pip.conf:
	@docker run \
		-v $(DATA_VOLUME):/data \
		-l $(PROJECT_LABEL) \
		alpine:latest \
		touch /data/pip.conf
	@echo "new pip.conf"
	@docker run \
	 	-v $(DATA_VOLUME):/data \
	 	-l $(PROJECT_LABEL) \
		alpine:latest \
		cat /data/pip.conf

# write address to extra pypi server to package pip.conf
set-remote-pypi:
	@echo -n "Pypi server url: "
	@{ read pypi_url; echo "[global]\nextra-index-url = $$pypi_url\n\n";} \
	| docker run -i \
		-l $(PROJECT_LABEL) \
		-v $(DATA_VOLUME):/data \
		alpine:latest \
		/bin/sh -c 'cat > /data/pip.conf'
	@echo "new pip.conf"
	@docker run \
		-l $(PROJECT_LABEL) \
	 	-v $(DATA_VOLUME):/data \
		alpine:latest \
		cat /data/pip.conf


# build all images required for tests
# this only needs to be done once per requirements change
build:
	@make -s TASK=build execute-task
	@make -s clean-containers
	@make -s clean-images


# run all tests using tests service from docker-compose.yml
run-tests:
	docker-compose run --rm tests


# clean cache, containers, images and source code directory
clean:
	@make -s TASK=clean execute-task
	-docker rm -v `docker ps -a -f label=$(PROJECT_LABEL) -f status=exited -q`


# clean source code directory (*.egg-info)
clean-src:
	@make -s TASK=clean-src execute-task


# project containers
clean-containers:
	@make -s TASK=clean-containers execute-task
	-docker rm `docker ps -a -f label=$(PROJECT_LABEL) -f status=exited -q`

# clean dangling project images
clean-images:
	@make -s TASK=clean-images execute-task
	-docker rm `docker ps -a -f label=$(PROJECT_LABEL) -f status=exited -q`



# execute some task defined by this devel environment
execute-task:
ifndef TASK
	$(error makefile TASK is undefined)
endif
	@make -s 'CMD=make $(TASK)' execute-cmd


# execute some command on develstack container
execute-cmd:
ifndef CMD
	$(error makefile CMD is undefined)
endif
	docker run -it \
		-e DEVELSTACK_ENV=python-3.5 \
		-e DEVELSTACK_PREFIX=$(PREFIX) \
		-e DEVELSTACK_CACHE_VOLUME=$(CACHE_VOLUME) \
		-e DEVELSTACK_SRC_VOLUME=$(SRC_VOLUME) \
		-v $(DATA_VOLUME):/data/ \
		-v $(SRC_VOLUME):/src \
		-v $(CACHE_VOLUME):/cache \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-l $(PROJECT_LABEL) \
		$(DEVELSTACK_IMAGE) \
		$(CMD)


# print the name of the tester image
tester-latest-image:
	@make -s TASK=tester-latest-image execute-task


# generate dummy docker-compose.yml
docker-compose.yml:
	echo "tests:" > $@
	echo "    entrypoint:" >> $@
	echo "        - <place tester>" >> $@
	echo "        - /src" >> $@
	echo "    image: $(shell make -s tester-latest-image)" >> $@
	echo "    volumes:" >> $@
	echo "        - $(SRC_DIR):/src" >> $@
