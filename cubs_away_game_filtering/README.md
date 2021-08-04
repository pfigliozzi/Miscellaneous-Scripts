# Cubs Away Game Filtering

I live quite close to Wrigley Field in Chicago. Cubs home games are (obviously) a huge draw of people into the city and into my neighborhood that affects parking and traffic, so I like to keep a schedule of Cubs home games in my calendar. The [MLB publishes the schedule online](https://www.mlb.com/cubs/schedule/2021-08) but it includes both the home games and the away games which I add to my Google calendar. Since I am not an avid baseball watcher I only really care about the home games because of the aforementioned reasons. One would think that I can go through and delete the away games but because the calendar is still linked to their calendar, everytime they make a schedule change then Google calendar will re-sync and download _all_ events from the source (including the away games I deleted). Meanwhile, I still want to get shedule updates incase home games get rescheduled. In my experience, the MLB updates the schedule maybe once per day.

So the way I decided to solve this problem is I would use Python to access my Google calendar and delete the away games. Since the MLB can still update the schedule (which undoes my deletions) I thought I can run my process regularly on a schedule so that I can continue to get schedule updates while keeping the away games off my calendar. To run the script regularly, I chose to deploy the script as a Docker container to AWS and setup a scheduled job that will run my Docker container every morning.

# Setup and User Guide:

If you look at the script, you will see that is very much hardcoded to work only with the Cubs game calender. That said, you can always edit the script to fit your use case if you are interested in repurposing it.

## Environment:

The environment to run this script is pretty simple, all you need is Python and the Google api client for Python. You can install these with pip:

```
  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

```

## Google Authentication:

You will need to setup an app on [https://console.cloud.google.com/](https://console.cloud.google.com/) and then you need to generate a credentials file that you can download that the script can source. The following two pages will help you get the `credentials.json` file that is used in the script:

1. [Setup an application on Google cloud](https://developers.google.com/workspace/guides/create-project)
2. [Create the credentials file for the script](https://developers.google.com/workspace/guides/create-credentials)
3. Save the credentials file as `credentials.json` in the same directory as the script. (Note: If you are using version control, do not commit this to your repository, this is a secret.)

## Running the script:

Running the script is as easy as calling:

```
python delete_cubs_away_games.py
```

This should source the credentials file and attempt to login into your Google account. If this is your first time using it, a browser window should pop up for you to authenticate the application and give it permission to see/edit your calendars.

After the first run, the script should generate a `token.pickle` file in the same directory as the script. This allows for the script to work in the future without having to give Google permissions in the browser window for subsequent runs.

## Deploying to AWS (Optional):

If you are interested in deploying the script to AWS you need to have at least run the script once locally and have the `credentials.json` and the `token.pickle` files in the folder with the script.

### Building the Docker Image:

The included Dockerfile can be used to build a Docker image with everything you need to run on a remote server. You can build the Docker image with:

```
docker image build Dockerfile -t delete_away_games
```

The Dockerfile also sets the entry point to run the script on startup (unless you override the entry point when you launch the container). It might be a good idea to run your container and make sure it still works.

### Push Docker Image to AWS ECR:

AWS ECR is a container registry that is part of the AWS ecosystem. If you want to deploy your this script on AWS you will need to upload your image to ECR (although you can retrieve images from Dockerhub as well). [These instructions will go over how to upload an image to ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html)

### Run your container in AWS ECS:

Now that your container is on AWS ECR you can go through the steps to setup your container to run on AWS ECS (Elastic Container Service). This involves setting up a cluster and setting up compute resources required. [These instructions will go over the steps of setting up an ECS cluster with you ECR container](https://aws.amazon.com/getting-started/hands-on/deploy-docker-containers/).

(Note: If you plan on scheduling your container set the __Desired number of instances__ to __0__, otherwise, AWS will continue to attempt to run your Docker container and keep at least one container alive.)

### Schedule your task:

If you followed the above directions, you should have a cluster created that does nothing (because you set number of instances to 0). If you want to schedule you container to run periodically you need to setup a scheduled task in your cluster.

1. Click into your cluster and find the "Scheduled Tasks" tab and click "Create".
2. Fill in the schedule run name.
3. Select a schedule to run your task. I used a cron expression of `cron(0 11 * * ? *)` which runs the job every morning at 6am CST.
4. Set your "Target task definition" to the same task you defined when you setup the cluster.

You should be all set! You can check the logs for you task on AWS Cloudwatch to make sure it is running correctly!

