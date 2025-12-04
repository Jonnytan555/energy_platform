def boiloff_loss_mmbtu(days: float, bor_rate: float = 0.001, volume_m3: float = 170000):
    """
    Computes total LNG boil-off loss in MMBtu.

    Parameters:
        days: number of voyage days
        bor_rate: boil-off rate (0.1%/day default)
        volume_m3: LNG tank volume in cubic meters

    Using an energy density of 22.5 MMBtu per ton-equivalent LNG.
    """
    energy_density_mmbtu = 22.5

    total_loss = bor_rate * days * volume_m3 * energy_density_mmbtu
    return total_loss
