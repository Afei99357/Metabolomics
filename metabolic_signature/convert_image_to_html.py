import base64

encoded = base64.b64encode(open("/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000058_new/results/48_hours.png", "rb").read()).decode('ascii')

encoded = 'data:image/png;base64,{}'.format(encoded)

print(encoded)