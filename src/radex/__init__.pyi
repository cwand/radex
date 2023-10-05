from collections import defaultdict
from typing import DefaultDict
import numpy as np
import numpy.typing as npt
from datetime import date
import pydicom


# --- UTILS.PY ---

def list_choose(descText: str, quest: str, options: list[str]) -> int: ...

def list_yn(descText: str, quest: str) -> bool: ...

def yyyymmdd2date(date_string: str) -> date: ...


# --- FILE_HANDLER ---

class FileHandler:

    fp: str
    filemap: DefaultDict[str, list[str]]

    def __init__(self, data_fp: str | None = ...): ...

    def discover(self): ...

    def descriptions(self) -> list[str]: ...

    def files(self, descr: str) -> list[str]: ...


# --- SPECTRUM.PY ---

class Spectrum:

    rate_by_kev: npt.NDArray[np.float64]
    count_time: float
    mdate: date | None

    def __init__(self, rate_by_kev: npt.NDArray[np.float64], count_time: float,
                 mdate: date | None = ...):  ...

    def print_to_file(self, file_name: str): ...

    def window_rate(self, window: tuple[int, int]) -> float: ...


def load_spectrum_from_file(file_name: str) -> Spectrum: ...

def add_spectrum(spec1: Spectrum, spec2: Spectrum) -> Spectrum: ...

def subtract_spectrum(spec1: Spectrum, spec2: Spectrum) -> Spectrum: ...


# --- SPECTRUM_PLOTTER.PY ---

class SpectrumPlotter:

    bkg: Spectrum
    spec: Spectrum
    name: str

    def __init__(self, background: Spectrum | None, spectrum: Spectrum): ...

    def set_title(self, title: str): ...

    def plot(self): ...


# --- SPECTRUM_ANALYSIS_MODEL.PY ---

class SpectrumAnalysisResult:

    def __init__(self, detected: bool, net_signal: float, conf: float): ...

    detected: bool
    net_signal: float
    conf: float


class SpectrumAnalysisModel:
    alpha: float  # Acceptable risk of type I errors (false positive)
    beta: float  # Acceptable risk of type II errors (false negative)
    gamma: float  # Confidence interval size (1-gamma) of true signal

    background: Spectrum  # Background spectrum to apply
    spectrum: Spectrum  # Gross spectrum to analyse
    windows: list[tuple[int, int]]  # The relevant windows from where counts should be extracted

    sens: float  # Sensitivity [cps/Bq]
    dsens: float  # Statistical uncertainty on the sensitivity

    def __init__(self, background: Spectrum, windows: list[tuple[int, int]] | None = ...): ...

    def _check_spectrum_not_none(self): ...

    def set_spectrum(self, spectrum: Spectrum): ...

    def __bkg_window_counts(self) -> float: ...

    def __spc_window_counts(self) -> float: ...

    def __net_window_counts(self) -> float: ...

    def critical_level(self) -> float: ...

    def detection_limit(self) -> float: ...

    def set_sensitivity(self, sens: float, dsens: float): ...

    def analyse_spectrum(self) -> SpectrumAnalysisResult: ...


# --- PHYSICS.PY ---

class Radium223:

    windows: list[tuple[int, int]]
    half_life: float
    acc_act: float

    def __init__(self): ...

def decay(activity_i: float, activity_f: float, half_life: float) -> float: ...

# --- KNOWN_SOURCES.PY ---

def sensitivity() -> tuple[float, float]: ...

def write_calibration(spectrum: Spectrum, activity: str, uncertainty_act: str, name: str) -> str:
    ...


# --- EXTRACT_DICOM_SPECTRUM.PY ---

def _findspec(dataset: pydicom.FileDataset, indent: int, specstr: str) -> str | None: ...

def extract_spectrum(file_name: str) -> Spectrum: ...

def extract_sum(filenames: list[str]) -> Spectrum: ...


# --- RADIUMLOG.PY ---

def write_log(mdate: date, sername: str, mda: float, sens: float, act: float, days: float,
              disp_date: date): ...