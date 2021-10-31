# from coffea import processor
# from coffea import analysis_tools

import awkward as ak

from typing import Any, Optional
from pydantic import BaseModel


class Mask(BaseModel):
    dataset: str
    year: str
    trigger: Optional[Any] = None
    nmuons: Optional[Any] = None
    muon_id: Optional[Any] = None
    muon_pt: Optional[Any] = None
    tight_muon: Optional[Any] = None
    iso_muon: Optional[Any] = None
    nphotons: Optional[Any] = None
    photon_pt: Optional[Any] = None
    photon_sc_eta: Optional[Any] = None
    photon_electron_veto: Optional[Any] = None
    photon_tight_id: Optional[Any] = None


def trigger_selection(events, year):
    # define HLT trigger path string
    if year == "2016":
        hlt_trigger_name = "Mu17_Photon30_IsoCaloId"
    if year == "2017":
        hlt_trigger_name = "Mu17_Photon30_IsoCaloId"
    if year == "2018":
        hlt_trigger_name = "Mu17_Photon30_IsoCaloId"

    trigger_filter = getattr(events.HLT, hlt_trigger_name) == 1

    return trigger_filter


def muon_selection(events):
    nmuons_filter = ak.num(events.Muon) >= 2  # at least 2 muons
    muon_pt_filter = events.Muon.pt > 3  # minimum muon pt
    muon_id_filter = events.Muon.tightId == 1  # muon id: Tight
    iso_muon_filter = events.Muon.pfRelIso03_all < 0.35  # PF_Isolation < 0.35

    return nmuons_filter, muon_pt_filter, muon_id_filter, iso_muon_filter


def photon_selection(events):
    nphotons_filter = ak.num(events.Photon) >= 1  # at lest one photon
    photon_pt_filter = events.Photon.eCorr * events.Photon.pt > 33  # pt at least 33 GeV
    photon_sc_eta_filter = (events.Photon.isScEtaEB == 1) | (
        events.Photon.isScEtaEE == 1
    )  # is Barrel or Endacap - no "crack photons".
    photon_electron_veto_filter = events.Photon.electronVeto == 1  # electron veto
    photon_tight_id_filter = events.Photon.cutBased == 3  # cut based tight photon

    return (
        nphotons_filter,
        photon_pt_filter,
        photon_sc_eta_filter,
        photon_electron_veto_filter,
        photon_tight_id_filter,
    )