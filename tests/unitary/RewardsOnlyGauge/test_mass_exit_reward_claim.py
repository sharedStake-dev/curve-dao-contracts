import math

import pytest
from brownie import ZERO_ADDRESS

REWARD = 10 ** 20
WEEK = 7 * 86400


@pytest.fixture(scope="module", autouse=True)
def initial_setup(
    alice,
    accounts,
    chain,
    coin_reward,
    reward_contract,
    token,
    mock_lp_token,
    rewards_only_gauge,
    gauge_controller,
    minter,
):
    # gauge setup
    token.set_minter(minter, {"from": alice})
    gauge_controller.add_type(b"Liquidity", 10 ** 10, {"from": alice})
    gauge_controller.add_gauge(rewards_only_gauge, 0, 0, {"from": alice})

    # deposit into gauge
    mock_lp_token.approve(rewards_only_gauge, 2 ** 256 - 1, {"from": alice})

    for acct in accounts[:10]:
        rewards_only_gauge.deposit(10 ** 18, acct, {"from": alice})

    # add rewards
    sigs = [
        reward_contract.stake.signature[2:],
        reward_contract.withdraw.signature[2:],
        reward_contract.getReward.signature[2:],
    ]
    sigs = f"0x{sigs[0]}{sigs[1]}{sigs[2]}{'00' * 20}"

    rewards_only_gauge.set_rewards(
        reward_contract, sigs, [coin_reward] + [ZERO_ADDRESS] * 7, {"from": alice}
    )

    # fund rewards
    coin_reward._mint_for_testing(REWARD, {"from": reward_contract})
    reward_contract.notifyRewardAmount(REWARD, {"from": alice})

    # sleep half way through the reward period
    chain.sleep(WEEK)


def test_mass_withdraw_claim_rewards(accounts, rewards_only_gauge, coin_reward, mock_lp_token):
    for account in accounts[:10]:
        rewards_only_gauge.withdraw(rewards_only_gauge.balanceOf(account), {"from": account})
        assert rewards_only_gauge.claimed_reward(account, coin_reward) == 0
        assert rewards_only_gauge.claimable_reward_write.call(account, coin_reward) > 0

    for account in accounts[:10]:
        rewards_only_gauge.claim_rewards({"from": account})
        assert math.isclose(coin_reward.balanceOf(account), REWARD / 10)
