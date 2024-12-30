Elasticsearch server crontab -l

35 00 * * * cd /home/gsbu/ml/tools; ./ml_gen_json_by_date.sh
25 01 * * * cd /home/gsbu/ml/tools; ./ml_notify_warning.sh
45 01 * * * cd /home/gsbu/ml/tools; ./ml_unconfirm_filter.sh
25 02 * * * cd /home/gsbu/ml/tools; ./ml_webml_attacked_unconfirm_reindex.sh
