#!/bin/bash
# $Id: $
 
# Pacemaker control script
# Usage: pacemakerctl start|stop|status
 
pacemaker_home=${PACEMAKER_HOME:-/apps/od/pacemaker}
log_dir=/var/log/pacemaker
pacemaker_pid_file="$log_dir/pacemaker.pid"
pacemaker_user=rts
 
# read functions
set -e # temporarily exit on error
#source $pacemaker_home/bin/_lib.sh
set +e
 
pacemaker_start () {
   pace_interval=300
   cap_interval=120
   pace_history_length=3
   cap_history_length=3
   log_level=critical
   debug_flag="-dd"
 
   # verify running as user "rts"
   ensure_sudo_user $pacemaker_user
 
   mv "$log_dir"/pacemaker.out "$log_dir"/pacemaker.out.old
   mv "$log_dir"/pacemaker.err "$log_dir"/pacemaker.err.old
 
   # call pacemaker - daemonize
   # http://stackoverflow.com/questions/3430330/best-way-to-make-a-shell-script-daemon/10908325#10908325
   exec $pacemaker_home/bin/runpm.sh --noArchiving --blackoutPeriodMinutes=7 --envName=prod --rootDir="$pacemaker_home" --logFileDir="$log_dir" --paceRecalcMaxHistoryLength="$pace_history_length" --capRecalcMaxHistoryLength="$cap_history_length" --paceRecalcInterval="$pace_interval" --capRecalcInterval="$cap_interval" --console="$log_level" --limitToPacedCampaigns $debug_flag "$@" 0<&- > "$log_dir"/pacemaker.out 2> "$log_dir"/pacemaker.err &
 
   pacemaker_process_pid=$!
 
   echo "Starting Pacemaker process $pacemaker_process_pid"
 
   # wait for pid file to appear
   wait_for_pid created $pacemaker_process_pid "$pacemaker_pid_file"
 
   if test -s "$pacemaker_pid_file"; then
       pidfile_pid=`cat "$pacemaker_pid_file"`
 
       if [[ "$pidfile_pid" -eq $pacemaker_process_pid ]]; then
 
           if (kill -0 "$pidfile_pid" 2>/dev/null); then
               echo "Pacemaker process $pidfile_pid is running"
 
               disown -h $pacemaker_process_pid
               ps -f -p $pacemaker_process_pid
 
               echo "SUCCESS"
               return 0
           else
               echo "ERROR: Pacemaker process $pidfile_pid is not running"
           fi
 
       else
           echo "ERROR: pidfile pid $pidfile_pid does not match the process $pacemaker_process_pid that i just started"
           echo "perhaps a pacemaker was already running?"
       fi
   fi
 
   sleep 1
   cat "$log_dir"/pacemaker.err
 
   return 1
}
 
 
pacemaker_stop () {
   # verify running as user "rts"
   ensure_sudo_user $pacemaker_user
 
   echo "Checking pid file $pacemaker_pid_file"
 
   if [[ -s "$pacemaker_pid_file" ]]; then
       pidfile_pid=`cat "$pacemaker_pid_file"`
 
       if (kill -0 "$pidfile_pid" 2>/dev/null); then
           echo -n "Stopping PaceMaker: $pidfile_pid from $pacemaker_pid_file"
           kill -INT "$pidfile_pid"
           # pacemaker should remove the pid file when it exits, so wait for it.
           wait_for_pid removed "$pidfile_pid" "$pacemaker_pid_file"; return_value=$?
 
           # just in case:
           if (kill -0 "$pidfile_pid" 2>/dev/null); then
               echo "Process is still running; trying to kill it more forcefully"
               kill -INT "$pidfile_pid"
               kill -TERM "$pidfile_pid"
               rm "$pacemaker_pid_file"
           fi
       else
           echo "Pacemaker process $pidfile_pid is not running"
           #rm "$pacemaker_pid_file"
       fi
 
       return $return_value
   else
       echo "No valid Pacemaker pid file ($pacemaker_pid_file) could be found"
       return 0
   fi
}
 
 
pacemaker_status () {
   # verify running as user "rts" - required for the "kill" to work
   ensure_sudo_user $pacemaker_user
 
   echo "Checking pid file $pacemaker_pid_file"
 
   if [[ -s "$pacemaker_pid_file" ]]; then
       pidfile_pid=`cat "$pacemaker_pid_file"`
 
       if (kill -0 "$pidfile_pid" 2>/dev/null); then
           echo "PaceMaker process $pidfile_pid is running"
           return 0
       else
           echo "Pacemaker process $pidfile_pid is not running"
           return 1
       fi
   else
       echo "No valid Pacemaker pid file ($pacemaker_pid_file) could be found"
       return 1
   fi
}
 
 
pacemaker_clean () {
   # verify running as user "rts" - required for the "kill" to work
   ensure_sudo_user $pacemaker_user
 
   echo "Checking pid file $pacemaker_pid_file"
 
   if [[ -s "$pacemaker_pid_file" ]]; then
       pidfile_pid=`cat "$pacemaker_pid_file"`
 
       if (kill -0 "$pidfile_pid" 2>/dev/null); then
           echo "WARNING: PaceMaker process $pidfile_pid is running"
       else
           echo "Pacemaker process $pidfile_pid is not running"
           echo "Cleaning pid file $pacemaker_pid_file"
       fi
 
       rm -f "$pacemaker_pid_file"
 
   else
       echo "No valid Pacemaker pid file ($pacemaker_pid_file) exists"
   fi
 
   return 0
}
 
 
cmd="$1"
shift
 
case "$cmd" in
   start)
       pacemaker_start "$@"
       exit $?
       ;;
   stop)
       pacemaker_stop
       exit $?
       ;;
   restart)
       $0 stop
       pacemaker_start "$@"
       exit $?
       ;;
   status)
       pacemaker_status
       exit $?
       ;;
   clean)
       pacemaker_clean
       exit $?
       ;;
   *)
       echo "Usage: $0 {start|stop|restart|status|clean} [args]"
       echo 1
esac
 
