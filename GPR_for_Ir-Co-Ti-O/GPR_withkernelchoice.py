#%%
# GP_PIPELINE_withkernelchoice.py
# Code used in publication: 'Gaussian Process Regression-Enhanced Screening of Ir-Co-Ti Mixed-Oxide Thin-Film Electrocatalyst Libraries for Acidic Oxygen Evolution'
# Published in: 
# DOI:
# Authors of the publication: Joanna M. Przybysz, Felix Thelen, Florian Lourens, Ken Jenewein, Alfred Ludwig, Serhiy Cherevko
# Zenodo DOI (data and code): https://doi.org/10.5281/zenodo.19001670
# The input file 'HT_summary_XXX.txt' contains columns with Co, Ir and Ti content for each measurement area, in terms of atomic % (excluding oxygen content), and columns with overpotential and dissolution of each element. The targets (overpotential and dissolution) are extracted from a high-throughput experiental dataset. 
# The file 'EDX_xxx.csv' contains data from collaborators, with compositions of each measurement area. The compositions were determined by energy-dispersive X-ray spectroscopy (EDX). Not all of these areas were measured with SFC-ICP-MS, hence the Gaussian Process predictions. 
# For each material library, room temperature or 500°C, the filepaths for PATH_DATA and PATH_COMP_EDX have to be changed accordingly. The csv export lines should be changed as well, so that the exports are not overwritten (last two lines of the script). 
# To predict on 1 atomic % composition spread, paste the path to the respective composition file (Spread1at%_Ir_Co_Ti.csv) in PATH_COMP_EDX.

import os
import numpy as np
import pandas as pd
import torch

from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import r2_score, mean_squared_error
from gpytorch.kernels import MaternKernel, ScaleKernel, LinearKernel, AdditiveKernel
from botorch.models import SingleTaskGP, ModelListGP
from botorch.models.transforms import Normalize, Standardize
from botorch.fit import fit_gpytorch_mll
from gpytorch.mlls import ExactMarginalLogLikelihood

#%%
# Configuration
# ---------------------------
DEVICE = torch.device("cpu")
DTYPE = torch.double
RNG_SEED = 109
torch.manual_seed(RNG_SEED)
np.random.seed(RNG_SEED)

# User variables 
features = ["Co%", "Ir%", "Ti%"]
targets = ["Overpotential", "Dissolution_Ir193 (S001)", "Dissolution_Co59 (S001)", "Dissolution_Ti47 (S001)"]

# Data location 
# HT summary file (tab-delimited) that contains both compositions (elements, atomic %, not considering oxygen content) and measured properties(targets)
PATH_DATA = r"C:\...\HT_summary_RTemp.txt"
# Composition search spaces (csv with Co, Ir, Ti in percent)
PATH_COMP_EDX = r"C:\...\EDX_RTemp.csv"         
#%%
# Repeated-CV seeds 
# ---------------------------
# Motivation: The dataset is small, so metrics can vary notably across different
# CV shuffles / model initializations. To obtain a *stable* estimate of training
# performance, we average CV R2 across multiple seeds and also report the std.
# NOTE: We keep the *test split* fixed (RNG_SEED above) and never tune using test.
SEED_LIST = [7312, 1845, 9627, 4079, 5893, 221, 7684, 115, 9401, 3546]

#%%
# Load data
# ---------------------------
# Load measured HT(high-throughput) data (contains compositions and properties)
# Some rows might be metadata in the file; adjust skiprows as needed.
ht_df = pd.read_table(PATH_DATA, sep="\t", skiprows=[1])
# Ensure required columns exist
missing_cols = [c for c in features + targets if c not in ht_df.columns]
if missing_cols:
    raise ValueError(f"Missing columns in HT data: {missing_cols}")

X = ht_df[features].to_numpy()
Y = ht_df[targets].to_numpy()
#%%
# Train/Test split
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=RNG_SEED
)

X_train_t = torch.tensor(X_train, dtype=DTYPE, device=DEVICE)
y_train_t = torch.tensor(y_train, dtype=DTYPE, device=DEVICE)
X_test_t  = torch.tensor(X_test,  dtype=DTYPE, device=DEVICE)
y_test_t  = torch.tensor(y_test,  dtype=DTYPE, device=DEVICE)

def build_covar(nu=0.5, add_linear=False):
    """Return a new covariance module each call."""
    base = MaternKernel(nu=nu)
    if add_linear:
        return ScaleKernel(AdditiveKernel(base, LinearKernel()))
    return ScaleKernel(base)

def fit_model_list_with_kernel_params(X_t, Y_t, nu=1.5, add_linear=False):
    """Build a fresh covar per target using the provided params."""
    d = X_t.shape[1]
    models = []
    for i in range(Y_t.shape[1]):
        covar_module = build_covar(nu=nu, add_linear=add_linear)  # new instance
        gp = SingleTaskGP(
            X_t, Y_t[:, i:i+1],
            input_transform=Normalize(d),
            outcome_transform=Standardize(1),
            covar_module=covar_module,
        )
        mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
        fit_gpytorch_mll(mll)
        models.append(gp)
    return ModelListGP(*models)

def cv_score_kernel(X_t, Y_t, nu, add_linear, seeds, n_splits=5):
    """
    Return:
    - overall mean±std CV R2 (averaged across targets)
    - per-target mean±std CV R2
    """

    overall_scores = []
    target_scores = []

    for s in seeds:
        torch.manual_seed(s)
        np.random.seed(s)

        kf = KFold(
            n_splits=n_splits,
            shuffle=True,
            random_state=s
        )

        fold_target_scores = []

        for tr, va in kf.split(X_t):

            model = fit_model_list_with_kernel_params(
                X_t[tr],
                Y_t[tr],
                nu=nu,
                add_linear=add_linear
            )

            model.eval()

            with torch.no_grad():
                post = model.posterior(X_t[va])
                mean = post.mean

            # R2 per target
            r2s = [
                r2_score(
                    Y_t[va, j].cpu().numpy(),
                    mean[:, j].cpu().numpy()
                )
                for j in range(Y_t.shape[1])
            ]

            fold_target_scores.append(r2s)

            # average R2 across targets for this fold
            overall_scores.append(np.mean(r2s))

        # average folds for each target for this seed
        target_scores.append(
            np.mean(fold_target_scores, axis=0)
        )

    target_scores = np.array(target_scores)

    return {
        "overall_mean": float(np.mean(overall_scores)),
        "overall_std": float(np.std(overall_scores, ddof=1)),
        "target_mean": np.mean(target_scores, axis=0),
        "target_std": np.std(target_scores, axis=0, ddof=1)
    }

# Candidate kernels 
CANDIDATES = [
    {"nu": 0.5, "add_linear": False},
    {"nu": 1.5, "add_linear": False},
    {"nu": 2.5, "add_linear": False},
    {"nu": 1.5, "add_linear": True},   # Matérn + linear trend
]

# Example selection on the training set only
results = []
for cand in CANDIDATES:
    cv_results = cv_score_kernel(
        X_train_t,
        y_train_t,
        cand["nu"],
        cand["add_linear"],
        SEED_LIST,
        n_splits=5
    )

    results.append((cand, cv_results))

# pick best candidate by mean CV; if the same, choose by lower std and preferably no linear term (simplicity)
results.sort(
    key=lambda x: (
        -x[1]["overall_mean"],
        x[1]["overall_std"],
        x[0]["add_linear"],
    )
)

best_candidate, best_cv = results[0]

# Cross-validation report
cv_results_df = pd.DataFrame(
    [
        {
            "Kernel": (
                f"Matérn ν={candidate['nu']}"
                + (" + Linear" if candidate["add_linear"] else "")
            ),
            "nu": candidate["nu"],
            "Linear": candidate["add_linear"],
            "CV R2 mean": cv["overall_mean"],
            "CV R2 std": cv["overall_std"],
        }
        for candidate, cv in results
    ]
)

print("\nCross-validation performance:")
print(
    cv_results_df.to_string(
        index=False,
        formatters={
            "CV R2 mean": "{:.3f}".format,
            "CV R2 std": "{:.3f}".format,
        },
    )
)

selected_kernel_name = (
    f"Matérn ν={best_candidate['nu']}"
    + (" + Linear" if best_candidate["add_linear"] else "")
)

print(f"\nSelected kernel: {selected_kernel_name}")
print(
    f"Overall CV R2: "
    f"{best_cv['overall_mean']:.3f} ± "
    f"{best_cv['overall_std']:.3f}"
)

selected_cv_df = pd.DataFrame(
    {
        "Property": targets,
        "CV R2 mean": best_cv["target_mean"],
        "CV R2 std": best_cv["target_std"],
    }
)

print("\nSelected-kernel per-target CV performance:")
print(
    selected_cv_df.to_string(
        index=False,
        formatters={
            "CV R2 mean": "{:.3f}".format,
            "CV R2 std": "{:.3f}".format,
        },
    )
)

# Final model and test report
final_model = fit_model_list_with_kernel_params(
    X_train_t,
    y_train_t,
    nu=best_candidate["nu"],
    add_linear=best_candidate["add_linear"],
)
final_model.eval()

with torch.no_grad():
    test_posterior = final_model.posterior(X_test_t)
    test_mean = test_posterior.mean

y_test_np = y_test_t.cpu().numpy()
test_mean_np = test_mean.cpu().numpy()

test_r2 = [
    r2_score(y_test_np[:, j], test_mean_np[:, j])
    for j in range(y_test_np.shape[1])
]

test_rmse = [
    np.sqrt(
        mean_squared_error(
            y_test_np[:, j],
            test_mean_np[:, j],
        )
    )
    for j in range(y_test_np.shape[1])
]

test_ranges = np.ptp(y_test_np, axis=0)

test_nrmse = [
    rmse / value_range if value_range > 0 else np.nan
    for rmse, value_range in zip(test_rmse, test_ranges)
]

test_results_df = pd.DataFrame(
    {
        "Property": targets,
        "Test R2": test_r2,
        "Test RMSE": test_rmse,
        "Test nRMSE (%)": np.asarray(test_nrmse) * 100,
    }
)

print("\nHeld-out test-set performance:")
print(
    test_results_df.to_string(
        index=False,
        formatters={
            "Test R2": "{:.3f}".format,
            "Test RMSE": "{:.3g}".format,
            "Test nRMSE (%)": "{:.2f}".format,
        },
    )
)


# Learned model parameters
parameter_rows = []

for target, gp in zip(targets, final_model.models):
    if best_candidate["add_linear"]:
        matern_kernel = gp.covar_module.base_kernel.kernels[0]
    else:
        matern_kernel = gp.covar_module.base_kernel

    lengthscale = (
        matern_kernel.lengthscale
        .detach()
        .cpu()
        .numpy()
        .reshape(-1)
    )

    parameter_rows.append(
        {
            "Property": target,
            "Noise variance": gp.likelihood.noise.item(),
            "Output scale": gp.covar_module.outputscale.item(),
            "Matérn lengthscale": np.array2string(
                lengthscale,
                precision=3,
                separator=", ",
            ),
            "Mean constant": gp.mean_module.constant.item(),
        }
    )

model_parameters_df = pd.DataFrame(parameter_rows)

print("\nLearned final-model parameters:")
print(
    model_parameters_df.to_string(
        index=False,
        formatters={
            "Noise variance": "{:.3g}".format,
            "Output scale": "{:.3g}".format,
            "Mean constant": "{:.3g}".format,
        },
    )
)


#%%
# Build composition space to predict, and optionally exclude measured compositions

comp_frames = []
if os.path.exists(PATH_COMP_EDX):
    df1 = pd.read_csv(PATH_COMP_EDX)
    # normalize headers to known names if needed
    # Expecting columns Ir, Co, Ti as percent
    comp_frames.append(df1[["Ir", "Co", "Ti"]].rename(columns={"Ir": "Ir%", "Co": "Co%", "Ti": "Ti%"}))

#%%
if not comp_frames:
    print("No composition search spaces found; skipping prediction on composition space.")
else:
    comp_space_total = pd.concat(comp_frames, ignore_index=True)
    comp_space_total = comp_space_total[["Co%", "Ir%", "Ti%"]]  # order columns as in training
    # Option to exclude measured compositions.
    ht_comps = ht_df[features]
    comp_space_topredict = comp_space_total#[~comp_space_total.apply(tuple, 1).isin(ht_comps.apply(tuple, 1))].copy()      # unhash this and the line below is you want to exclude the experimental dataset from predictions.
    print("Comp space sizes: total =", len(comp_space_total))#, " | to predict =", len(comp_space_topredict))

    # Predict on comp_space_topredict using raw percent inputs; model applies its input_transform
    X_comp = torch.tensor(comp_space_topredict.to_numpy(), dtype=DTYPE, device=DEVICE)
    with torch.no_grad():
        post_comp = final_model.posterior(X_comp)
        mean_comp = post_comp.mean.cpu().numpy()
        std_comp  = post_comp.variance.sqrt().cpu().numpy()

    pred_cols = targets
    std_cols  = [f"{p}_std" for p in targets]
    preds_df = pd.DataFrame(mean_comp, columns=pred_cols)
    stds_df  = pd.DataFrame(std_comp,  columns=std_cols)
    out_df = pd.concat([comp_space_topredict.reset_index(drop=True), preds_df, stds_df], axis=1)
    out_df.to_csv("DataandPredsRTemp.csv", index=False)            #If the experimental data was removed from compositions to predict, you might want to change the file naming. 
    print("Wrote predictions to DataandPredsRTemp.csv")

# %%
