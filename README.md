<h1 align="center"><b>The Meeting Sphinx</b></h1>

<p align="center">
    <img src="https://img.shields.io/github/license/aitalshashank2/The-Meeting-Sphinx" />
    <img src="https://img.shields.io/github/issues-pr-closed/aitalshashank2/The-Meeting-Sphinx" />
    <img src="https://img.shields.io/tokei/lines/github/aitalshashank2/The-Meeting-Sphinx" />
    <img src="https://img.shields.io/github/contributors/aitalshashank2/The-Meeting-Sphinx" />
    <img src="https://img.shields.io/docker/cloud/automated/aitalshashank2/the-meeting-sphinx.svg" />
    <img src="https://img.shields.io/docker/cloud/build/aitalshashank2/the-meeting-sphinx.svg" />
</p>

**The Meeting Sphinx** is a platform for hosting secure meetings in which the organizer is notified when any of the viewers starts recording their screen. This platform is perfect for the speakers who are conscious about what they say. Our platform prevents any misuse of the content of the presenter.

## Setup guidelines
- Clone the repository
- Make `django/code/configuration/config.yml` using `django/code/configuration/config-stencil.yml`.

### Development Server
- Build the image using
    ```bash
    docker-compose -f sphinx-build/development.yml build
    ```
- Start the network
    ```bash
    docker-compose -f sphinx-build/development.yml up -d
    ```
- In order to stop the network, run
    ```bash
    docker-compose -f sphinx-build/development.yml down
    ```

### Production Server
- Build the image using
    ```bash
    docker-compose -f sphinx-build/production.yml build
    ```
- Start the network
    ```bash
    docker-compose -f sphinx-build/production.yml up -d
    ```
- In order to stop the network, run
    ```bash
    docker-compose -f sphinx-build/production.yml down
    ```

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change. Please the templates specified while raising an issue.

## Associated Repositories
- [Frontend](https://github.com/ShreyasTheOne/meeting-sphinx-frontend)
- [Docker Hub](https://hub.docker.com/repository/docker/aitalshashank2/the-meeting-sphinx)
