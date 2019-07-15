  fname         = 'obs_epoch_001.nc';
  ObsTypeString = 'SOIL_MOISTURE';
  ObsCopyString = 'observations';
  CopyString    = 'observations';
  QCString      = 'Data QC';
  region        = [0 360 -90 90 -Inf Inf];
  global obsmat;
  link_obs(fname, ObsTypeString, ObsCopyString, CopyString, QCString, region)