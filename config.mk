###############################################################################
### Whale&Jaguar Platform Configuration
###
### This file defines configuration used in the Makefile.
### You may add and/or override these values with your own custom configuration
### in `config.local.mk`.
###
### Please see GNU Makes multi-line variable documentation for more info.
### https://www.gnu.org/software/make/manual/html_node/Multi_002dLine.html
###############################################################################


# List of tools that must be installed.
# A simple check to determine the tool is available. No version check, etc.
define REQUIRED_SOFTWARE
docker \
docker-compose \
git
endef

# Defined here are the project configuration
define SERVICES
identity-app
endef

# List of user defined networks that should be created.
define DOCKER_NETWORKS
whaleandjaguar.localhost
endef
