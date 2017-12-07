if [[ $# != 3 ]]
  then
    echo "Usage: ./sched_reddit_scrape.sh m|h [interval (m|h)] [python script path]"
    exit
fi
echo "Set cron job, storing in /tmp/reddit_logs.log"
if [[ $1 == "m" ]]
  then
    echo "    every $2 minutes"
    echo "*/$2 * * * * root python $3 >> /tmp/reddit_logs.log" >> /etc/crontab
  else
    echo "    every $2 hours"
    echo "* */$2 * * * root python $3 >> /tmp/reddit_logs.log" >> /etc/crontab
fi
