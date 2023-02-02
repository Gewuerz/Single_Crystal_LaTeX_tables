# ----------------------------------------------------------------------------------------------------------------------
# single_crystal_data.py
#
# Creates the single crystal data table
#
# author: Judith Bönnighausen
# Last change: 23.01.2023
# ----------------------------------------------------------------------------------------------------------------------
def make_single_crystal_data_table(cif_file, lxr_converted, sum_converted, save_path):
    """ Function to create the single crystal data table."""
    # set all variables assigned in the cif_file to be "0"
    length_a = "0"
    length_b = "0"
    length_c = "0"
    volume = "0"
    molecular_weight = "0"
    density = "0"
    temperature = "0"
    diffractometer = "0"
    wavelength = "0"
    number_of_reflections = "0"
    structure_factor = "0"
    e_density_max = "0"
    e_density_min = "0"
    number_of_independent_reflections = "0"
    r_no_of_independent_reflections = "0"
    number_of_independent_reflections_i = "0"
    r_no_of_independent_reflections_i = "0"
    data = "0"
    parameter = "0"
    gof = "0"
    extinction_coeff = "0"
    r_factor_i = "0"
    wr_factor_i = "0"
    r_factor_all = "0"
    wr_factor_all = "0"

    # set all variables assigned in the lxr_file to be "0"
    transmission_split = "0"
    absorption_coeff = "0"
    hkl_split = "0"
    two_theta_split = "0"

    # set all variables assigned in the sum_file to be "0"
    crystal_measurements = []
    parameters = []
    detector_distance = "0"
    exposure_time = "0"
    omega_split = "0"
    omega_inc = "0"

    for line in cif_file.readlines():
        # Get all the info from the .cif file, include error message if a value isn't there
        if "_cell_length_a" in line:
            length_a = line.strip("_cell_length_a \n")
        if "_cell_length_b" in line:
            length_b = line.strip("_cell_length_b \n")
        if "_cell_length_c" in line:
            length_c = line.strip("_cell_length_c \n")
        if "_cell_volume" in line:
            volume = line.strip("_cell_volume \n")
        if "_chemical_formula_weight" in line:
            molecular_weight = line.strip("_chemical_formula_weight \n")
        if "_exptl_crystal_density_diffrn" in line:
            density = line.strip("_exptl_crystal_density_diffrn \n")
        if "_diffrn_ambient_temperature  " in line:
            temperature = line.strip("_diffrn_ambient_temperature  \n")
        if "_diffrn_measurement_device_type" in line:
            diffractometer = line.strip("_diffrn_measurement_device_type \n")
            diffractometer = diffractometer.strip("'")
        if "_diffrn_radiation_wavelength" in line:
            wavelength = line.strip("_diffrn_radiation_wavelength \n")
        if "_diffrn_reflns_number" in line:
            number_of_reflections = line.strip("_diffrn_reflns_number \n")
        if "_exptl_crystal_F_000" in line:
            structure_factor = line.strip("_exptl_crystal_F_000 \n")
        if "_refine_diff_density_max" in line:
            e_density_max = line.strip("_refine_diff_density_max \n")
        if "_refine_diff_density_min" in line:
            e_density_min = line.strip("_refine_diff_density_min \n")

        if "_reflns_number_total" in line:
            number_of_independent_reflections = line.strip("_reflns_number_total \n")
        if "_diffrn_reflns_av_R_equivalents" in line:
            r_no_of_independent_reflections = line.strip("_diffrn_reflns_av_R_equivalents \n")
        if "_reflns_number_gt" in line:
            number_of_independent_reflections_i = line.strip("_reflns_number_gt \n")
        if "_diffrn_reflns_av_unetI/netI" in line:
            r_no_of_independent_reflections_i = line.strip("_diffrn_reflns_av_unetI/netI \n")
        if "_refine_ls_number_reflns" in line:
            data = line.strip("_refine_ls_number_reflns \n")
        if "_refine_ls_number_parameters" in line:
            parameter = line.strip("_refine_ls_number_parameters \n")
        if "_refine_ls_goodness_of_fit_gt" in line:
            gof = line.strip("_refine_ls_goodness_of_fit_gt \n")
        if "_refine_ls_extinction_coef" in line:
            extinction_coeff = line.strip("_refine_ls_extinction_coef \n")
        if "_refine_ls_R_factor_gt" in line:
            r_factor_i = line.strip("_refine_ls_R_factor_gt \n")
        if "_refine_ls_wR_factor_gt" in line:
            wr_factor_i = line.strip("_refine_ls_wR_factor_gt \n")
        if "_refine_ls_R_factor_all" in line:
            r_factor_all = line.strip("_refine_ls_R_factor_all \n")
        if "_refine_ls_goodness_of_fit_ref" in line:
            wr_factor_all = line.strip("_refine_ls_goodness_of_fit_ref \n")
        elif line.startswith("# 11."):
            break

    with open(lxr_converted, "r") as file_object:
        lines_lxr = file_object.readlines()

    for line in lines_lxr:
        #  Search for min/max transmission and absorption coefficient
        if "Min and max Transmission" in line:
            transmission_split = line.strip("Min and max Transmission : \n").split(",")
            # transmission_split = transmission.split(",")
        if "Absorption Coefficient" in line:
            absorption_coeff = line.strip("Absorption Coefficient   : \n")
            absorption_coeff = absorption_coeff.strip("mm^⁻1")
        if "Minimum and maximum H,K,L" in line:
            try:
                hkl_all = line.strip("Minimum and maximum H,K,L  : \n").split(
                    "   ")  # splits into positive and negative hkl
                hkl_split = hkl_all[0].split(",") + hkl_all[1].split(",")
            except IndexError:
                print("There was a problem reading your lxr-file: No h,k,l found.")
        if "Minimum and maximum 2Theta" in line:
            two_theta_all = line.strip("Minimum and maximum 2Theta : \n")
            two_theta_split = two_theta_all.split(",")
        elif "The 100 'strongest'" in line:
            break

    with open(sum_converted, "r") as file_object:
        lines_sum = file_object.readlines()

    for line in lines_sum:
        if "Size, radius:" in line:
            try:
                # Get the size of the crystal, convert it to a float, then to nm
                crystal_measurements = line.strip("Size, radius: \n").split("x")
                # crystal_split = crystal_measurements.split("x")
                crystal_measurements[0] = str(float(crystal_measurements[0]) * 100.0)
                crystal_measurements[1] = str(float(crystal_measurements[1]) * 100.0)
                # Get rid of the units and the empty radius part
                crystal_split = crystal_measurements[2].split(",")
                crystal_split[0] = crystal_split[0].strip("mm3")
                crystal_measurements[2] = str(float(crystal_split[0]) * 100.0)
            except ValueError:
                print("The crystal sizes could not be read correctly.")
            except IndexError:
                print("There was a problem reading your sum-file: No crystal size found.")
        if "Detector distance" in line:
            detector_distance = line.strip("Detector distance [mm] : \n")
        if "Parameters:" in line:
            parameters = line.strip("Parameters:            A, B, EMS:").split(" ")
        if "Exposure time" in line and exposure_time == "0":
            exposure_time = line.strip("Exposure time [min]  : \n")
        if "Omega range" in line:
            # Get the Omega range, split the two numbers, as they need to be in a \numrange in the table
            omega_range = line.strip("Omega range: \n")
            omega_split = omega_range.split("-")
        if "Omega increment" in line:
            omega_inc = line.strip("Omega increment: \n")
            omega_inc = omega_inc.strip("( osc. )")
        elif "Building reciprocal space" in line:
            break

    with open(save_path, "a") as table_object:
        # Write all the data into a .tex file in a tabular-environment
        table_object.write(
            r"%This is the beginning of the single crystal data table." + "\n"
            r"\begin{tabular}{lc}" + "\n"
            r"\toprule" + "\n"
            r"Gitterparameter ~/~\si{\pico\meter} &   $a =$ \num{" + length_a + r"}\\" + "\n"
            r"   & $b =$ \num{" + length_b + r"} \\" + "\n"
            r"   & $c =$ \num{" + length_c + r"}\\ " + " \n"
            r"Volumen~/~\si{\nano\meter\cubed} & \num{" + volume + r"}\\" + "\n"
            r"Molare Masse~/~\si{\gram\per\mole}	& \num{" + molecular_weight + r"} \\" + "\n"
            r"Kristallgröße~/~\si{\micro\meter\cubed} & $" +
            crystal_measurements[0] + r" \times " + crystal_measurements[1] + r" \times" + crystal_measurements[2]
            + r"$ \\" + "\n"  # sum-file                                                   
            r"Berechnete Dichte ~/~\si{\gram\per\centi\meter\cubed}	&\num{" + density + r"} \\" + "\n"
            r"Diffraktometer & " + diffractometer + r"\\" + "\n"
            r"Wellenlänge~/~ \si{\angstrom} 	&\num{" + wavelength + r"} \\" + "\n"
            r"Detektorabstand~/~\si{\milli\meter} & \num{" + detector_distance + r"} \\" + "\n"  # sum-file
            r"Messzeit ~/~\si{\minute} & \num{" + exposure_time + r"} \\" + "\n"  # sum-file
            r"Temperature ~/~\si{\kelvin} & \num{" + temperature + r"} \\" + "\n"
            r"$\omega$-Bereich; Inkrement~/~\si{\degree} &\numrange{" + omega_split[0] + "}{" + omega_split[1] + r"},"
            r"\num{" + omega_inc + r"};\\" + "\n"  # sum-file
            r"Integr. Param.~/~A; B; EMS & \num{" + parameters[0] + r"}; \num{" + parameters[1] + r"}; \num{"
            + parameters[2] + r"} \\" + "\n"  # sum-file
            r"Transmission ~(max / min) & \num{" + transmission_split[1] + r"} / \num{" +
            transmission_split[0] + r"} \\" + "\n"
            r"Absorptionskoeffizient~/~mm$^{-1}$	& \num{" + absorption_coeff + r"} \\" + "\n"
            r"$hkl$-Bereich & \numrange{" + hkl_split[0] + "}{" + hkl_split[3] + r"}; \numrange{" + hkl_split[1]
            + "}{" + hkl_split[4] + r"}; \numrange{" + hkl_split[2] + "}{" + hkl_split[5] + r"}\\" + "\n"  # lxr-file
            r"$\theta$-Bereich~/~$^{\circ}$ &\numrange{" + two_theta_split[0] + "}{" + two_theta_split[1] + r"}\\"
            + "\n"  # lxr-file
            r"$F(000)$ &\num{" + structure_factor + r"} \\" + "\n"
            r"Anzahl Reflexe	&\num{" + number_of_reflections + r"} \\" + "\n"
            r"Unabhängige Reflexe ~/~$R_{int}$ & \num{" + number_of_independent_reflections + r"} / \num{"
            + r_no_of_independent_reflections + r"} \\" + "\n"
            r"Reflexe mit $I \geq 3\sigma(I)$ ~/~$R_\sigma$ & \num{" + number_of_independent_reflections_i
            + r"} / \num{" + r_no_of_independent_reflections_i + r"}\\" + "\n"
            r"Daten / Parameter &\num{" + data + r"} / \num{" + parameter + r"} \\" + "\n"
            r"\textit{Goodness-of-fit} ~/~ $F^{2}$  & \num{" + gof + r"} \\" + "\n"
            r"$R$-Werte [$I \geq 3\sigma(I)$] &$R_structure_data = \num{" + r_factor_i + r"}$ \\" + "\n"
            r"&$wR2 = \num{" + wr_factor_i + r"}$ \\" + "\n"
            r"$R$-Werte (alle Daten) & $R_structure_data = \num{" + r_factor_all + r"}$ \\" + "\n"
            r"&$wR2 = \num{" + wr_factor_all + r"}$ \\" + "\n"
            r"Extinktionskoeffizient	& \num{" + extinction_coeff + r"} \\" + "\n"
            r"Restelektronendichten~/~\si{\elementarycharge\per\cubic\angstrom} & \num{" + e_density_min + r"} / \num{"
            + e_density_max + r"}\\" + "\n"
            r"\bottomrule"
            r"\end{tabular}"
        )
        message = save_path.split("/")[-1] + " erzeugt."
        return message
