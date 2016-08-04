SELECT Db.Service_Date,
  B.Base_Abbrev,
  Db.Block_Route_Group_Num, 
  Db.Block_Run_Num,
  Db.Block_Miles,
  Db.Curr_Vehicle_Id,
  Db.Daily_Block_Status,
  Db.Sched_Pull_In_Time,
  Db.Sched_Pull_Out_Time,
  Db.Vehicle_Type_Code,
  trunc(db.service_date) as Service_Day, 
  db.service_date + Db.Sched_Pull_Out_Time/1440 as Pull_Out, 
  db.service_date + Db.Sched_Pull_In_Time/1440 as Pull_In
FROM daily_block db, base b
where db.base_id = b.Base_Id