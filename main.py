from sinusParams.views import PlotView
from sinusParams.sinusParams import SinusParamsAdjuster


def main():
    sinus_params_adjuster = SinusParamsAdjuster(
        adjusting_strategy_type="evolutionary",
        similarity_threshold=0.25,
    )

    sinus_adjuster_view = PlotView(sinus_params_adjuster)

    sinus_adjuster_view.display_points()
    sinus_adjuster_view.print_params()
    sinus_adjuster_view.display_points_and_graph()


if __name__ == "__main__":
    main()
