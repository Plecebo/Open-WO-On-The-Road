import csv
from datetime import datetime

# Load data
with open('input/WOData.csv') as f:
    wos = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
with open('input/DailyBlock.csv') as f:
    db = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

bad_behavior = []


def check_violation(open_date, completed_date, pull_in, pull_out):
    if open_date > pull_in or completed_date < pull_out:
        # 5 & 1
        return False
    else:
        return True


def in_violation(vehicle, pull_out, pull_in):
    violations = []
    for wo in wos:
        wo_vehicle = wo['UNIT_NO']
        if wo_vehicle != vehicle:
            continue
        open_date = datetime.strptime(wo['OPEN_DT'], '%Y-%m-%d %H:%M:%S')
        visit_reason = wo['VISIT_REASON']
        wo_number = wo['WO_NO']
        if wo['COMPLETED_DT'] == '':
            completed_date = datetime.now()
        else:
            completed_date = datetime.strptime(wo['COMPLETED_DT'], '%Y-%m-%d %H:%M:%S')

        if check_violation(open_date, completed_date, pull_in, pull_out):
            this_wo = {'WO': wo_number, 'OPEN': open_date, 'COMPLETE': completed_date, 'VISIT_REASON': visit_reason}
            violations.append(this_wo)
    return violations


print("Doing DB")
for db_row in db:
    pull_out = datetime.strptime(db_row['PULL_OUT'], '%Y-%m-%d %H:%M:%S')
    pull_in = datetime.strptime(db_row['PULL_IN'], '%Y-%m-%d %H:%M:%S')
    vehicle = db_row['CURR_VEHICLE_ID']
    service_day = datetime.strptime(db_row['SERVICE_DATE'], '%Y-%m-%d %H:%M:%S').date()
    route = db_row['BLOCK_ROUTE_GROUP_NUM']
    run = db_row['BLOCK_RUN_NUM']
    base = db_row['BASE_ABBREV']
    wo_in_violation = in_violation(vehicle, pull_out, pull_in)
    for wo in wo_in_violation:
        bad_this = dict(SERVICE_DATE=service_day, ROUTE=route, RUN=run, BASE=base, VEHICLE=vehicle, WO_NO=wo['WO'],
                        WO_OPEN=wo['OPEN'], WO_COMPLETE=wo['COMPLETE'], WO_VISIT_REASON=wo['VISIT_REASON'])
        print(bad_this)
        bad_behavior.append(bad_this)

print("Finished doing DB")
with open("output/WOWhileAssigned.csv", 'w') as bad_f:
    print("Writing BadFile")
    fieldnames = ['SERVICE_DATE',
                  'ROUTE',
                  'RUN',
                  'BASE',
                  'VEHICLE',
                  'WO_OPEN',
                  'WO_NO',
                  'WO_VISIT_REASON',
                  'WO_COMPLETE']
    writer = csv.DictWriter(bad_f, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
    writer.writeheader()
    writer.writerows(bad_behavior)
    print("Finished Writing BadFile")
