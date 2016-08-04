SELECT u.unit_no,
  U.Using_Dept_No,
  W.Wo_No,
  W.Open_Dt,
  W.Completed_Dt, 
  W.Status, 
  trunc(w.open_dt) as OpenDate, 
  W.Visit_Reason
FROM View_Udc_Main u,
  View_O_Wo w
WHERE u.class2 ='REV'
AND u.unit_id  = w.unit_id
AND W.Open_Dt >= to_date('06/06/2016', 'MM/DD/YYYY')
and not w.status = 'X'