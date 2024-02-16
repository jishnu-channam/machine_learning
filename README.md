## Start Machine Learning project.

### Software and account Requirement.

1. [Github Account](https://github.com)
2. [Heroku Account](https://dashboard.heroku.com/login)
3. [VS Code IDE](https://code.visualstudio.com/download)
4. [GIT cli](https://git-scm.com/downloads)
5. [GIT Documentation](https://git-scm.com/docs/gittutorial)


Creating conda environment

```
conda create -p venv python ==3.7 -y
```

```
pip install -r requirements.txt
```

To add files to git

```
git add .
```
OR 
```
git add <file_name>
```

NOTE: To ignore file or file from git, we can write the name of file/folder in .gitignore file

TO check the git status 
```
git status
```
To check all version maintained by git
```
git log
```
To create version/commit all changes by git
```
git commit -m "message"
```
TO send versions/changes to github
```
git push origin main
```
To check remote url
```
git remove -v
```
TO setup CI/CD pipeline in heroku we need 3 information

1. HEROKU_EMAIL = jintuch@gmail.com
2. HEROKU_API_KEY = 7be44d0b-a969-45b3-b384-ee3c8ede4f93
3. HEROKU_APP_NAME = ml-regression-jishnu 

BUILD DOCKER IMAGE
```
docker build -t <image_name>:<tagname> .
```
Note: Image name for docker must be lowercase
To list docker image
```
docker images
```
To run docker images
```
docker run -p 5000:5000 -e PORT=5000 e1be24a91543
```
To check running container in Docker
```
docker ps
```
To stop docker container
```
docker stop <container_id>
```