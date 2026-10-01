"""Create a PNG report. Uses the 'Agg' backend so it works on servers with no display (CI)."""
import matplotlib

matplotlib.use("Agg")  # must be set before pyplot is imported
import matplotlib.pyplot as plt  # noqa: E402

from .checks import moving_average  # noqa: E402


def plot_report(df, findings, out_path):
    """Plot voltage (left axis) and temperature (right axis) with failures marked."""
    fig, ax_v = plt.subplots(figsize=(10, 5))
    ax_t = ax_v.twinx()  # second y-axis sharing the same x-axis

    ax_v.plot(df["timestamp"], df["voltage"], color="tab:blue", label="voltage")
    ax_v.plot(df["timestamp"], moving_average(df["voltage"]), color="navy",
              linewidth=1, label="voltage (5-sample avg)")
    ax_v.axhline(findings["limits"]["voltage_limit"], color="red", linestyle="--",
                 label="voltage limit")
    ax_t.plot(df["timestamp"], df["temperature"], color="tab:orange", label="temperature")

    m = findings["masks"]
    volt_bad = m["over_voltage"] | m["stuck"]
    ax_v.scatter(df.loc[volt_bad, "timestamp"], df.loc[volt_bad, "voltage"], color="red",
                 zorder=3, label="voltage flagged")
    ax_t.scatter(df.loc[m["runaway"], "timestamp"], df.loc[m["runaway"], "temperature"],
                 color="darkred", marker="x", zorder=3, label="temperature flagged")

    ax_v.set_xlabel("time [s]")
    ax_v.set_ylabel("voltage [V]")
    ax_t.set_ylabel("temperature [deg C]")
    ax_v.set_title(f"Test log analysis - verdict: {findings['verdict']}")
    h1, l1 = ax_v.get_legend_handles_labels()
    h2, l2 = ax_t.get_legend_handles_labels()
    ax_v.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
