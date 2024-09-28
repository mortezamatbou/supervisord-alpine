#!/bin/sh

crond

supervisord -c "/etc/supervisor/supervisord.conf"
