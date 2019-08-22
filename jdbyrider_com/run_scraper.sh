base_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $base_path
domain=${PWD##*/}
scraper_name=${domain}-scraper
docker build -t $scraper_name --no-cache .
rm -rf apify_docker_storage
docker run -e "GOOGLE_API_KEY" -e "APIFY_LOCAL_STORAGE_DIR"="apify_storage" -e "APIFY_TOKEN=''" -v ${base_path}/apify_docker_storage:/apify_storage ${scraper_name}:latest
