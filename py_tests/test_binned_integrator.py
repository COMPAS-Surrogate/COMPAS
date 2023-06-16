from compas_python_utils.cosmic_integration.binned_cosmic_integrator.cosmological_model import CosmologicalModel
from compas_python_utils.cosmic_integration.binned_cosmic_integrator.bbh_population import BBHPopulation
from compas_python_utils.cosmic_integration.binned_cosmic_integrator.snr_grid import SNRGrid
from compas_python_utils.cosmic_integration.binned_cosmic_integrator.conversions import *
from compas_python_utils.cosmic_integration.binned_cosmic_integrator import DetectionMatrix
import numpy as np
import os
import glob


def test_cosmological_models(test_archive_dir):
    model = CosmologicalModel()
    assert model.dPdlogZ.shape == (len(model.redshift), len(model.metallicities))
    fig = model.plot()
    fn = os.path.join(test_archive_dir, "cosmological_model_plot.png")
    fig.savefig(fn)
    assert os.path.exists(fn)


def test_bbh_population(example_compas_output_path):
    population = BBHPopulation(example_compas_output_path)
    assert population.n_bbh == 2
    assert population.n_systems == 2
    assert population.mass_evolved_per_binary > 0

def test_SNR_grid(test_archive_dir):
    snr_grid = SNRGrid()
    fig = snr_grid.plot()
    fig.show()
    fn = os.path.join(test_archive_dir, "snr_grid_plot.png")
    fig.savefig(fn)
    assert os.path.exists(fn)

def test_conversions():
    m1, m2 = 10, 3
    chirp_mass = m1_m2_to_chirp_mass(m1, m2)
    eta = m1_m2_to_eta(m1, m2)
    mtot = chirp_mass_eta_to_total_mass(chirp_mass, eta)
    assert np.isclose(mtot, m1 + m2)
    m1_new, m2_new = chirp_mass_eta_to_m1_m2(chirp_mass, eta)
    assert np.isclose(m1_new, m1)
    assert np.isclose(m2_new, m2)

def test_binned_cosmic_integration(example_compas_output_path,  test_archive_dir,):
    example_compas_output_path = "/Users/avaj0001/Documents/projects/compas_dev/quasir_compass_blocks/data/COMPAS_Output.h5"
    test_archive_dir = 'out_plots'
    detection_matrix = DetectionMatrix.from_compas_output(example_compas_output_path, outdir=test_archive_dir, save_plots=True)
    assert detection_matrix.rate_matrix.shape == (len(detection_matrix.chirp_mass_bins), len(detection_matrix.redshift_bins))
    detection_matrix.save()
    det_matrix_fn = glob.glob(f'{test_archive_dir}/*.h5')[0]
    det_matrix_2 = DetectionMatrix.from_h5(det_matrix_fn)
    assert np.allclose(detection_matrix.rate_matrix, det_matrix_2.rate_matrix)

    det_matrix_2.bin_data()
    fig = det_matrix_2.plot()
    fig.show()





