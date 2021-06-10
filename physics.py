#   File containg physcis related stuff

#   Energy windows related to specific isotopes
windows = {
  'Ra223': [(73,108), # Emissions at 81.1keV (15.2%), 83.8keV (25.1%) and 94.9keV (11.5%)
            (130,169),# Emissions at 144keV (3%) and 154keV (6%)
            (242,298),# Emission at 269.5keV (13.9%) and 271.2keV from Rn-219 daughter nucleus
            (316,386)# Emission at 351.1keV from Bi-211 daughter nucleus
            #(360,440)# Emission at 401.8keV from Rn-219 and at 404.9 from Pb-211 daughter nuclei
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
