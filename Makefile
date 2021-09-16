#gnu makefile
# This Makefile provides macro control of the microservice core of Whale&Jaguar Platform
# ecosystem. It performs tasks like:
#
#   * Verify dependencies are present
#   * Pre configuration and project bootstrapping
#   * Launching project
#
#
# Exit codes:
#
#   All failures should exit with a detailed code that can be used for
#   troubleshooting. The current exit codes are:
#
#     0: Success!
#   102: Required dependency is not installed.
#

###############################################################################
### Loaded Configuration
### Load configuration from external files. Configuration variables defined in
### later files have precedent and will overwrite those defined in previous
### files. The -include directive ensures that no error is thrown if a file is
### not found, which is the case if config.local.mk does not exist.
###############################################################################
-include config.mk config.local.mk

###############################################################################
### Common Configuration
###############################################################################
HOOK_DIR=bin

###############################################################################
### Tasks
###############################################################################
all: init

###############################################################################
### init-Project
### Initializes a project in development mode.
###############################################################################
define init-template
init-$(1): dependencies network-create prebuild-$(1) build-$(1) start-$(1)
endef
$(foreach p,$(SERVICES),$(eval $(call init-template,$(p))))

.PHONY: init
init: $(foreach p,$(SERVICES),init-$(p))


###############################################################################
### Verify prerequisite software is installed.
###############################################################################
is-not-installed=! (command -v $(1) >/dev/null)

define dependency-template
dependency-$(1):
	@if ( $(call is-not-installed,$(1)) ); \
	then \
	  echo "Dependency" $(1) " not found in path." \
	  && exit 102; \
	else \
	  echo "Dependency" $(1) "found."; \
	fi;
endef
$(foreach pkg,$(REQUIRED_SOFTWARE),$(eval $(call dependency-template,$(pkg))))

.PHONY: dependencies
dependencies: $(foreach pkg,$(REQUIRED_SOFTWARE),dependency-$(pkg))

###############################################################################
### Pre Build Hook
### Invokes the pre-build hook in the child project directory if it exists.
### Invoked before the Docker Compose build.
###############################################################################
define prebuild-template
prebuild-$(1):
	@if [ -e "./$(HOOK_DIR)/pre-build" ]; then \
	  echo "Running pre-build hook script for $(1)." \
	  && "./$(HOOK_DIR)/pre-build"; \
	else \
	  echo "No pre-build hook script for $(1). Skipping."; \
	fi;
endef
$(foreach p,$(SERVICES),$(eval $(call prebuild-template,$(p))))

.PHONY: prebuild
prebuild: $(foreach p,$(SERVICES),prebuild-$(p))


###############################################################################
### Create Docker Networks
### Create all networks defined in the DOCKER_NETWORKS variable.
### Networks provide a way to loosely couple the projects and allow them to
### communicate with each other. We'll use dependencies on external networks
### rather than dependencies on other projects. Networks are lightweight and
### easy to create.
###############################################################################
define network-create-template
network-create-$(1):
	@docker network create "$(1)" || true
endef
$(foreach p,$(DOCKER_NETWORKS),$(eval $(call network-create-template,$(p))))

.PHONY: network-create
network-create: $(foreach p,$(DOCKER_NETWORKS),network-create-$(p))

###############################################################################
### Remove Docker Networks
### Remove all networks defined in the DOCKER_NETWORKS variable.
###############################################################################
define network-remove-template
network-remove-$(1):
	@docker network rm "$(1)" || true
endef
$(foreach p,$(DOCKER_NETWORKS),$(eval $(call network-remove-template,$(p))))

.PHONY: network-remove
network-remove: $(foreach p,$(DOCKER_NETWORKS),network-remove-$(p))


###############################################################################
### Docker Build
### Performs `docker-compose build --no-cache --pull`
### This is a very conservative build strategy to avoid cache related build
### issues.
###############################################################################
define build-template
build-$(1): prebuild-$(1)
	@docker-compose build --no-cache --pull "$(1)"
endef
$(foreach p,$(SERVICES),$(eval $(call build-template,$(p))))

.PHONY: build
build: $(foreach p,$(SERVICES),build-$(p))


###############################################################################
### Start
### Starts services with `docker-compose up -d`
###############################################################################
define start-template
start-$(1):
	@docker-compose pull "$(1)"; docker-compose up -d "$(1)"
endef
$(foreach p,$(SERVICES),$(eval $(call start-template,$(p))))

.PHONY: start
start: $(foreach p,$(SERVICES),start-$(p))

###############################################################################
### Stop
### Stops services with `docker-compose stop`
###############################################################################
define stop-template
stop-$(1):
	@docker-compose stop "$(1)"
endef
$(foreach p,$(SERVICES),$(eval $(call stop-template,$(p))))

.PHONY: stop
stop: $(foreach p,$(SERVICES),stop-$(p))

###############################################################################
### Clean
### Clean services with `docker-compose rm`
### Removes all containers, volumes and local networks.
###############################################################################
.PHONY: clean
clean:
	@docker-compose down -v --rmi local --remove-orphans

###############################################################################
### Dynamically list all targets.
### See: https://stackoverflow.com/a/26339924
###############################################################################
.PHONY: list
list:
	@$(MAKE) -pRrq -f $(MAKEFILE_LIST) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs -n 1
