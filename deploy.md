# Deploy steps (Cloud Shell, free)
gcloud projects create YOUR_PROJECT_ID && gcloud config set project YOUR_PROJECT_ID
gcloud services enable appengine.googleapis.com storage.googleapis.com
gcloud app create --region=asia-south1
gsutil mb -l asia-south1 -b on gs://YOUR_PROJECT_ID-photoshare   # private, uniform access
gcloud storage buckets update gs://YOUR_PROJECT_ID-photoshare --public-access-prevention
# edit BUCKET_NAME in app.yaml, then:
gcloud app deploy
gcloud app browse
./loadtest.sh https://YOUR_PROJECT_ID.appspot.com     # verify autoscaling
