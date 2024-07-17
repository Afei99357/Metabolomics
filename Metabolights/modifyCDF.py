import netCDF4 as nc

ds = nc.Dataset("/Users/ericliao/Downloads/MTBLS27_compressed_files/EMILY_SAMPLE03.CDF", mode="w")

a = ds['a_d_sampling_rate']

