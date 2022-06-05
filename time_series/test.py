from hmmlearn.hmm import GaussianHMM

from loaders import DataLoader

df = DataLoader.load('ibm', sampling='1W', year_start=2000)

hmm_model = GaussianHMM(n_components=2, covariance_type="full", n_iter=1000)
hmm_model.fit(df['ln_Close'].to_numpy().reshape(-1, 1))
print("Model Score:", hmm_model.score(df['ln_Close'].to_numpy().reshape(-1, 1)))

