# dc-zoom-meeting-logger

Log zoom meetings to a various outputs. starting with google sheets

https://github.com/whojarr/dc-zoom-meeting-logger/

Contact: David Hunter <dhunter@digitalcreation.co.nz>

Copyright (C) 2021 Digital Creation Ltd 

For license information, see LICENSE

<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

### Built With

This project used the serverless framework along with yarn and poetry.

* [Serverless](https://www.serverless.com/)
* [Yarn](https://yarnpkg.com/)
* [Poerty](https://python-poetry.org/)
* [AWS CLI](https://aws.amazon.com/cli/)

<!-- GETTING STARTED -->
## Getting Started

You will requie an AWS Account, Zoom Account and Google Account.

See the docs in docs/README.md for setup

### Prerequisites

Install all the required node and python packages.

* AWS CLI
  ```sh
  aws --version
  ```
* yarn
  ```sh
  yarn --version
  ```
* poetry
  ```sh
  poetry --version
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
2. Install the node packages
   ```sh
   yarn install
   ```
3. Install the python packages
   ```sh
   poetry install
   ```
4. update the serverless.yml domain details
5. add the required AWS parameter store values

   /dc-zoom-meeting-logger/{stage}/ZOOM_VARIFICATION_TOKEN

   /dc-zoom-meeting-logger/{stage}/GOOGLE_AUTH_JSON

6. add the credentials required in AWS Paramter Store
   ```sh
   sls create_domain -s {stage}
   ```
   
7. sls deploy (to deploy to your default aws account)
   ```sh
   sls deploy -s {stage}
   ```
