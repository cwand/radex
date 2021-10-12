#   File containg physcis related stuff

#   Energy windows related to specific isotopes
windows = {
	'Ra223': [(76,89), # Emissions at 81.1keV (15.2%), 83.8keV (25.1%)
						(133,165),# Emissions at 144keV (3%) and 154keV (6%)
						(255,283),# Emission at 269.5keV (13.9%) and 271.2keV from Rn-219 daughter nucleus
						(322,366),# Emission at 324 and 338keV, and 351.1keV from Bi-211 daughter nucleus
						(383,422)# Emission at 401.8keV from Rn-219 and at 404.9 from Pb-211 daughter nuclei
						]
}

# Half life of specific isotopes (days)
half_life = {
	'Ra223': 11.4
}

# Acceptable activity (Bq)
acc_act = {
	'Ra223': 300
}
