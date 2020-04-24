from datetime import datetime

def create_report(dates):
    report={}
    for ldate in dates:
        sdate = datetime.utcfromtimestamp(ldate[1]).strftime('%Y-%m-%d')
        if sdate in report.keys():
            report[sdate]['logs'].append({'time': datetime.utcfromtimestamp(ldate[1]).strftime('%Y-%m-%dT%H:%M:%S'), 'unix': ldate[1]})            
            in_unix = report[sdate]['in']['unix']
            if in_unix > ldate[1]:
                report[sdate]['out'] = report[sdate]['in']
                report[sdate]['in'] = {'time': datetime.utcfromtimestamp(ldate[1]).strftime('%Y-%m-%dT%H:%M:%S'), 'unix': ldate[1]}
                report[sdate]['time_in_hours'] = (report[sdate]['out']['unix'] - report[sdate]['in']['unix']) / 3600.0
            else:
                if 'out' in report[sdate].keys():
                    if in_unix < ldate[1]:
                        report[sdate]['out'] = {'time': datetime.utcfromtimestamp(ldate[1]).strftime('%Y-%m-%dT%H:%M:%S'), 'unix': ldate[1]}
                        report[sdate]['time_in_hours'] = (report[sdate]['out']['unix'] - report[sdate]['in']['unix']) / 3600.0
                else:
                    report[sdate]['out'] = {'time': datetime.utcfromtimestamp(ldate[1]).strftime('%Y-%m-%dT%H:%M:%S'), 'unix': ldate[1]}
                    report[sdate]['time_in_hours'] = (report[sdate]['out']['unix'] - report[sdate]['in']['unix']) / 3600.0
        else:
            report[sdate] = {'in': {'time': datetime.utcfromtimestamp(ldate[1]).strftime('%Y-%m-%dT%H:%M:%S'), 'unix': ldate[1]},'out': {},'logs': [{'time': datetime.utcfromtimestamp(ldate[1]).strftime('%Y-%m-%dT%H:%M:%S'), 'unix': ldate[1]}]}
    return report
