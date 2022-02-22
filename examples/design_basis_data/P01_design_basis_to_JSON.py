"""
"""

import json


data_filepath = "P01.json"
check_JSON = True  # read JSON file to check data

P01 = {
    "Do": 0.660,
    "WT": 0.0214,
    "ρ_pipe":  7850.0,
    "coat": [(0.0003, 1450.), (0.0038, 960.), (0.045, 2250.)],
    "length": 12.2,
    "ρ_content": 215.0,
    "ρ_seawater": 1027.0,
    "g": 9.81
}




with open(data_filepath, 'w') as _fh:
    json.dump(P01, _fh)

# check JSON file
if check_JSON:
    #del P01
    with open(data_filepath, 'r') as _fh:
        P01_json = json.load(_fh)
    print(f"P01 == P01_json : {P01 == P01_json}")


# P01 = {
#     "alpha_U": 1.0,
#     "D": 0.6176,
#     "g": 9.81,
#     "gamma_inc": 1.1,
#     "h_ref": 30.,
#     "h_l": -340.,
#     "material": "CMn",
#     "p_d": 240e5, 
#     "rho_cont": 275.,
#     "rho_water": 1027.,
#     "rho_t": 1027.,
#     "SC": "medium",
#     "SMYS": 450.e6,
#     "SMTS": 535.e6,
#     "t": 0.0212,
#     "t_corr": 0.0005,
#     "t_fab": 0.001,
#     "T": 60,
# }

# if args.case.lower() in ["scalar", "error"]:
#     Do = 0.660
#     WT = 0.0214
#     coating_layers = [(0.0003, 1450.), (0.0038, 960.), (0.045, 2250.)]
# elif args.case.lower()=="array":
#     Do = np.array([0.660, 0.6656])
#     WT = np.array([0.0214, 0.0242])
#     # coating_layers = [ (np.array([0.0003, 0.0003]), np.array([1450., 1450.])), 
#     #     (np.array([0.0038, 0.0038]), np.array([960., 960.]) ), 
#     #     (np.array([0.045, 0.045]), np.array([2250., 1900.]) )]
#     coating_layers = [ (0.0003, 1450.), (0.0038, 960. ), 
#         (0.045, np.array([2250., 1900.]) )]
# length = 12.2
# pipe_ρ = 7850.    
# seawater_ρ = 1027.0
# gas_ρ = 215.0
# g = 9.81
