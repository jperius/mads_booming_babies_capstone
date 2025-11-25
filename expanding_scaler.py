import pandas as pd
import numpy as np


def global_expanding_standard_scaler_by_date(
    df,
    date_col,
    merge_cols=None,
    min_periods=0,
    stats=None,
    return_stats=False,
):
    """
    Expanding z-score scaling by unique date (allows multiple data points per date).

    Two modes:

    - Fit + transform (stats is None):
        * Computes expanding means/stds over the provided df.
        * Returns scaled df, and optionally the stats dict if return_stats=True.

    - Transform-only (stats is not None):
        * Uses previously computed stats (from a training set) and
          applies them to df without recomputing.

    merge_cols is a list of columns that are not scaled. They're called this because
    they're merged back to the columns with the date_col.
    """
    if merge_cols is None:
        merge_cols = []

    merge_cols = [c for c in merge_cols if c != date_col]

    df = df.sort_values(date_col)
    original_index = df.index

    if stats is None:
        feature_cols = [col for col in df.columns
                        if col != date_col and col not in merge_cols]

        means_map = {}
        stds_map = {}

        unique_dates = df[date_col].drop_duplicates().sort_values().to_numpy()
        for i, current_date in enumerate(unique_dates):
            if i < min_periods:
                continue

            past_data = df[df[date_col] <=
                           current_date][feature_cols].to_numpy()
            if past_data.shape[0] == 0:
                continue

            if past_data.ndim == 1:
                if len(feature_cols) == 1:
                    past_data = past_data.reshape(-1, 1)
                else:
                    raise ValueError(
                        f"Expected {len(feature_cols)} features but got 1D array on {current_date}"
                    )

            if past_data.shape[1] != len(feature_cols):
                raise ValueError(
                    f"Feature count mismatch at {current_date}: expected {len(feature_cols)} and got {past_data.shape[1]}. Check for duplicates."
                )

            means = np.mean(past_data, axis=0)
            stds = np.std(past_data, axis=0, ddof=0)
            means_map[current_date] = means
            stds_map[current_date] = np.where(stds == 0, 1e-8, stds)

        unique_dates_fitted = np.array(sorted(means_map.keys()))

        scaled_array = np.full((len(df), len(feature_cols)), np.nan)

        # map from date to row indices in this df
        date_to_index = {d: np.where(df[date_col] == d)[0]
                         for d in unique_dates}

        for current_date in unique_dates:
            if current_date not in means_map:
                continue
            idx = date_to_index[current_date]
            X = df.iloc[idx][feature_cols].to_numpy()
            scaled = (X - means_map[current_date]) / stds_map[current_date]
            scaled_array[idx, :] = scaled

        scaled_df = pd.DataFrame(
            scaled_array, columns=feature_cols, index=original_index)
        scaled_df[[date_col] + merge_cols] = df[[date_col] + merge_cols]
        scaled_df = scaled_df.dropna(subset=feature_cols, how="all", axis=0)

        stats_out = {
            "feature_cols": feature_cols,
            "means_map": means_map,
            "stds_map": stds_map,
            "unique_dates": unique_dates_fitted,
            "date_col": date_col,
            "min_periods": min_periods,
        }

        if return_stats:
            return scaled_df, stats_out
        else:
            return scaled_df

    else:
        feature_cols = stats["feature_cols"]
        means_map = stats["means_map"]
        stds_map = stats["stds_map"]
        unique_dates_fitted = np.array(stats["unique_dates"])

        if stats["date_col"] != date_col:
            raise ValueError(
                f"date_col mismatch between stats ('{stats['date_col']}') and argument ('{date_col}')"
            )

        # we only scale the feature_cols; merge_cols + date_col are passed through
        scaled_array = np.full((len(df), len(feature_cols)), np.nan)

        # dates we need to scale for the new df
        new_dates = df[date_col].drop_duplicates().sort_values().to_numpy()
        date_to_index = {d: np.where(df[date_col] == d)[0] for d in new_dates}

        for current_date in new_dates:
            # find the most recent date in the fitted stats that is <= current_date
            # if none, we leave those rows as NaN (or you can choose some other behavior)
            pos = np.searchsorted(unique_dates_fitted,
                                  current_date, side="right") - 1
            if pos < 0:
                # no past stats available for this date
                continue

            ref_date = unique_dates_fitted[pos]
            means = means_map[ref_date]
            stds = stds_map[ref_date]

            idx = date_to_index[current_date]
            X = df.iloc[idx][feature_cols].to_numpy()
            scaled = (X - means) / stds
            scaled_array[idx, :] = scaled

        scaled_df = pd.DataFrame(
            scaled_array, columns=feature_cols, index=original_index)
        scaled_df[[date_col] + merge_cols] = df[[date_col] + merge_cols]
        scaled_df = scaled_df.dropna(subset=feature_cols, how="all", axis=0)

        return scaled_df
