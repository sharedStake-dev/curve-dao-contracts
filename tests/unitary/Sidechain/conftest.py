import pytest
from brownie import ETH_ADDRESS


@pytest.fixture(scope="module")
def anyswap_root_gauge(RootGaugeAnyswap, minter, alice):
    return RootGaugeAnyswap.deploy(minter, alice, ETH_ADDRESS, {"from": alice})


@pytest.fixture(scope="module")
def polygon_root_gauge(RootGaugePolygon, minter, alice):
    return RootGaugePolygon.deploy(minter, alice, {"from": alice})


@pytest.fixture(scope="module")
def xdai_root_gauge(RootGaugeXdai, minter, alice):
    return RootGaugeXdai.deploy(minter, alice, {"from": alice})


@pytest.fixture(scope="module")
def child_chain_streamer(alice, ChildChainStreamer):
    return ChildChainStreamer.deploy(alice, {"from": alice})


@pytest.fixture(scope="module")
def checkpoint_proxy(alice, CheckpointProxy):
    return CheckpointProxy.deploy({"from": alice})


@pytest.fixture(scope="module", params=range(3), ids=["Anyswap", "Polygon", "XDAI"])
def root_gauge(request, anyswap_root_gauge, polygon_root_gauge, xdai_root_gauge):
    if request.param == 0:
        return anyswap_root_gauge
    elif request.param == 1:
        return polygon_root_gauge
    else:
        return xdai_root_gauge
